#!/usr/bin/env python3
"""deck_audit.py - a static audit for a Bison Fund deck file.

Usage:
    python3 deck_audit.py DECK.html [--stage plain|harness] [--json]

Stage defaults to auto-detect: "harness" when the file contains "cx-bar" or
"mock-screen", otherwise "plain".

The audit is a static read of the file. In the plain stage it checks that there
is a deck at all and how many slides it has, the slide structure, footers, the
title slide, eyebrows, the shipped chart markup, leftover template syntax, and
the mechanical copy rules. In the harness stage
it adds the four canvas rules, the three parts of Download PDF, region
annotation, and the dark-slide print layer.

It does NOT render anything. Overflow, scrollHeight, note collisions, and the
measured pixel height of a bar depend on layout and stay with the browser pass
in references/deck-build-checklist.md. This script reads the shipped markup and
stylesheet instead, so a bar height is judged by its declared value against the
declared chart height, not by its rendered size.

Findings print as "<file>:<line>: <severity> <message>", blockers versus
warnings, followed by a summary line. --json emits
{file, stage, findings:[{line, severity, message}], counts, slides}.

Exit 0 when clean, 1 when there is any finding, 2 when the file cannot be read.
Python 3 standard library only.
"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser

VOID_ELEMENTS = frozenset([
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
])

# The common finance acronyms the package bans in rendered copy, with the
# spelled-out form used in the finding message.
BANNED_ACRONYMS = [
    ("YoY", "year over year"),
    ("FCF", "free cash flow"),
    ("WACC", "discount rate"),
    ("MAPC", "monthly active consumers"),
    ("ARR", "annual recurring revenue"),
    ("TAM", "total addressable market"),
    ("CAGR", "compound annual growth rate"),
    ("mNAV", "net asset value multiple"),
    ("AV", "autonomous vehicle"),
    ("GB", "gross bookings"),
]

# A helper call inside a plain (non-f) string renders as literal source.
TEMPLATE_MARKERS = ("{card(", "{bar(", "%s", "{{")

EM_DASH = "\u2014"
MIDDLE_DOT = "\u00b7"
MIN_BAR_PX = 20.0
# How far a bar's height share may drift from its label's share of the chart
# maximum before the audit calls it a wrong height rather than rounding.
BAR_SCALE_TOLERANCE = 0.15
DEFAULT_CHART_HEIGHT_PX = 230.0
# The deck standard: a full-arc deck under 25 slides is under-built.
MIN_SLIDES = 25

HARNESS_MARKERS = ("cx-bar", "mock-screen")


class Node(object):
    """A minimal HTML element node with the line it starts on."""

    __slots__ = ("tag", "attrs", "line", "parent", "children", "texts")

    def __init__(self, tag, attrs, line, parent):
        self.tag = tag
        self.attrs = attrs
        self.line = line
        self.parent = parent
        self.children = []
        self.texts = []  # list of (text, line)

    def classes(self):
        return (self.attrs.get("class") or "").split()

    def has_class(self, name):
        return name in self.classes()


class DeckParser(HTMLParser):
    """Build a light DOM. Comments, doctype, and declarations are ignored."""

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.root = Node("#document", {}, 1, None)
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs), self.getpos()[0], self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID_ELEMENTS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        node = Node(tag, dict(attrs), self.getpos()[0], self.stack[-1])
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        if data.strip():
            self.stack[-1].texts.append((data, self.getpos()[0]))


def iter_descendants(node):
    """Depth first, pre-order, which is document order."""
    for child in node.children:
        yield child
        for deeper in iter_descendants(child):
            yield deeper


def find_all(node, predicate):
    return [n for n in iter_descendants(node) if predicate(n)]


def segments(node, include_code=True):
    """Return (text, line) pairs for every text run in the subtree.

    include_code=False leaves out the contents of <script> and <style>, which is
    what the copy rules want: a script inside a slide is not something a reader
    sees on the slide.
    """
    out = []
    if not include_code and node.tag in ("script", "style"):
        return out
    for text, line in node.texts:
        out.append((text, line))
    for child in node.children:
        out.extend(segments(child, include_code))
    return out


def text_of(node):
    return " ".join("".join(text for text, _line in segments(node)).split())


def first_desc(node, cls):
    for n in iter_descendants(node):
        if n.has_class(cls):
            return n
    return None


def css_rules(css):
    """Return (selector, body) pairs. Rules inside @media are flattened out."""
    rules = []
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        sel = " ".join(m.group(1).split())
        rules.append((sel, m.group(2)))
    return rules


def _squash(value):
    return re.sub(r"\s+", "", value)


def rule_targets(selector, name):
    for part in selector.split(","):
        if part.strip() == name:
            return True
    return False


def has_rule(rules, name, prop):
    want = _squash(prop)
    for selector, body in rules:
        if rule_targets(selector, name) and want in _squash(body):
            return True
    return False


def number_in(text):
    m = re.search(r"-?\d[\d,]*(?:\.\d+)?", text or "")
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


class Audit(object):
    def __init__(self, path, html, stage):
        self.path = path
        self.html = html
        self.stage = stage
        self.findings = []
        parser = DeckParser()
        parser.feed(html)
        parser.close()
        self.root = parser.root
        self.style_text = "\n".join(
            text_of(n) for n in find_all(self.root, lambda x: x.tag == "style")
        )
        self.script_text = "\n".join(
            text_of(n) for n in find_all(self.root, lambda x: x.tag == "script")
        )
        self.slides = find_all(
            self.root, lambda n: n.tag == "section" and n.has_class("slide")
        )

    # -- reporting ---------------------------------------------------------
    def add(self, severity, line, message):
        self.findings.append(
            {"line": int(line), "severity": severity, "message": message}
        )

    def blocker(self, line, message):
        self.add("blocker", line, message)

    def warning(self, line, message):
        self.add("warning", line, message)

    # -- plain stage -------------------------------------------------------
    def check_structure(self):
        for node in find_all(self.root, lambda n: n.has_class("slide")):
            if node.tag != "section":
                self.blocker(
                    node.line,
                    "slide is a <%s>, not a <section class=\"slide\">" % node.tag,
                )
        for slide in self.slides:
            if not slide.children:
                self.blocker(slide.line, "empty slide, no content and no .foot")
                continue
            last = slide.children[-1]
            if not last.has_class("foot"):
                self.blocker(slide.line, "slide does not end with a .foot")
            foot = last if last.has_class("foot") else first_desc(slide, "foot")
            if foot is None:
                continue
            if first_desc(foot, "pageno") is None:
                self.blocker(foot.line, ".foot has no .pageno page number")

    def check_footers(self):
        total_slides = len(self.slides)
        if total_slides == 0:
            return
        for index, slide in enumerate(self.slides, start=1):
            pageno = first_desc(slide, "pageno")
            if pageno is None:
                continue
            text = text_of(pageno)
            m = re.search(r"(\d+)\s*/\s*(\d+)", text)
            if not m:
                self.blocker(
                    pageno.line, "footer page number is not 'NN / TOTAL': %r" % text
                )
                continue
            shown, total = int(m.group(1)), int(m.group(2))
            if total != total_slides:
                self.blocker(
                    pageno.line,
                    "footer shows %02d / %02d but the file has %d slides"
                    % (shown, total, total_slides),
                )
            if shown != index:
                self.blocker(
                    pageno.line,
                    "footer page number %02d is out of document order, expected %02d"
                    % (shown, index),
                )

    def check_title_slide(self):
        if not self.slides:
            return
        first = self.slides[0]
        titles = [n for n in iter_descendants(first) if n.tag in ("h1", "h2")]
        if len(titles) > 1:
            self.blocker(
                titles[0].line,
                "title slide carries %d title elements, expected exactly one" % len(titles),
            )
        elif len(titles) == 0:
            self.warning(first.line, "title slide carries no title element")

    def check_eyebrows(self):
        for index, slide in enumerate(self.slides):
            eyebrow = first_desc(slide, "eyebrow")
            if eyebrow is None:
                continue
            if index == 0:
                self.blocker(eyebrow.line, "eyebrow on the title slide")
            title_node = first_desc(slide, "title")
            if title_node is None:
                for n in iter_descendants(slide):
                    if n.tag in ("h1", "h2"):
                        title_node = n
                        break
            if title_node is not None:
                eyebrow_text = text_of(eyebrow).lower()
                title_text = text_of(title_node).lower()
                if eyebrow_text and eyebrow_text == title_text:
                    self.blocker(
                        eyebrow.line,
                        "eyebrow repeats the slide title verbatim: %r" % text_of(eyebrow),
                    )

    def chart_height_px(self):
        for selector, body in css_rules(self.style_text):
            if rule_targets(selector, ".chart"):
                m = re.search(r"height\s*:\s*([0-9.]+)px", body)
                if m:
                    return float(m.group(1))
        return DEFAULT_CHART_HEIGHT_PX

    def check_charts(self):
        chart_px = self.chart_height_px()
        for slide in self.slides:
            for chart in find_all(slide, lambda n: n.has_class("chart")):
                self.check_chart(chart, chart_px)
            for svg in find_all(slide, lambda n: n.tag == "svg"):
                if svg.has_class("print-bg"):
                    continue
                style = svg.attrs.get("style") or ""
                if "max-width" not in style:
                    self.warning(
                        svg.line,
                        "inline SVG chart has no max-width cap, it scales to the card and overflows",
                    )

    def check_chart(self, chart, chart_px):
        bars = [n for n in iter_descendants(chart) if n.has_class("bar")]
        if bars:
            columns = [(bar, first_desc(bar, "col")) for bar in bars]
        else:
            columns = [
                (col, col)
                for col in iter_descendants(chart)
                if col.has_class("col")
            ]
        series = []
        for bar, col in columns:
            lab = first_desc(bar, "lab")
            if lab is None or not text_of(lab):
                self.warning(
                    (col or bar).line,
                    "chart column has no labeled value (no .lab text)",
                )
            if col is None:
                self.warning(bar.line, "chart column has no .col element")
                continue
            style = col.attrs.get("style") or ""
            m = re.search(r"height\s*:\s*([0-9.]+)\s*(px|%)?", style)
            if not m:
                self.warning(col.line, "chart column has no height")
                continue
            value = float(m.group(1))
            unit = m.group(2) or "%"
            if unit == "px":
                height_px = value
            else:
                height_px = value / 100.0 * chart_px
            if height_px < MIN_BAR_PX:
                self.warning(
                    col.line,
                    "bar height is under about %dpx equivalent (declared %s%s), too small to read"
                    % (int(MIN_BAR_PX), m.group(1), unit),
                )
            lab_value = number_in(text_of(lab)) if lab is not None else None
            series.append((height_px, lab_value))
        self.check_chart_order(chart, series)
        self.check_chart_scale(chart, series)

    def check_chart_order(self, chart, series):
        prev = None
        for height_px, value in series:
            if prev is not None and value is not None and prev[1] is not None:
                dh = height_px - prev[0]
                dv = value - prev[1]
                if dh * dv < 0:
                    self.warning(
                        chart.line,
                        "bar heights contradict the labeled values: heights and values move in opposite order",
                    )
                    return
            prev = (height_px, value)

    def check_chart_scale(self, chart, series):
        """A bar's height share should track its label's share of the chart maximum.

        The order check catches a chart that runs backwards. This catches the more
        common mistake: the bars were eyeballed, so a value that is twice another is
        not drawn at twice the height.
        """
        pairs = [(height_px, value) for height_px, value in series if value is not None]
        if len(pairs) < 2:
            return
        height_max = max(height_px for height_px, _value in pairs)
        value_max = max(value for _height_px, value in pairs)
        if height_max <= 0 or value_max <= 0:
            return
        for height_px, value in pairs:
            if value < 0:
                continue
            drift = abs(height_px / height_max - value / value_max)
            if drift > BAR_SCALE_TOLERANCE:
                self.warning(
                    chart.line,
                    "bar height does not match its labeled value: %.0f%% of the tallest bar "
                    "for %s of the largest value (%.0f%% of the chart maximum expected)"
                    % (100.0 * height_px / height_max, "{:,.4g}".format(value),
                       100.0 * value / value_max),
                )
                return

    def check_template_syntax(self):
        for slide in self.slides:
            for text, line in segments(slide, include_code=False):
                for marker in TEMPLATE_MARKERS:
                    if marker in text:
                        self.blocker(
                            line,
                            "leftover template syntax %r rendered into slide copy" % marker,
                        )

    def check_copy(self):
        for slide in self.slides:
            for text, line in segments(slide, include_code=False):
                if EM_DASH in text:
                    self.blocker(line, "em dash in slide copy")
                if MIDDLE_DOT in text:
                    self.blocker(line, "middle dot in slide copy")
                for acronym, spelled in BANNED_ACRONYMS:
                    pattern = r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(acronym)
                    if re.search(pattern, text):
                        self.warning(
                            line,
                            "acronym in slide copy: %r, write it out as %r"
                            % (acronym, spelled),
                        )

    # -- harness stage -----------------------------------------------------
    def check_canvas_rules(self):
        rules = css_rules(self.style_text)
        required = [
            ("#cx-stage", "display:flex",
             "#cx-stage must set display:flex"),
            (".mock-screen", "display:none",
             ".mock-screen must set display:none"),
            (".mock-screen.cx-active", "display:flex",
             ".mock-screen.cx-active must set display:flex"),
            ("body", "overflow:hidden",
             "body must set overflow:hidden"),
        ]
        for name, prop, message in required:
            if not has_rule(rules, name, prop):
                self.blocker(1, "canvas rule missing: %s" % message)

    def check_pdf(self):
        if not any(
            n.tag == "button" and n.attrs.get("id") == "cx-pdf"
            for n in iter_descendants(self.root)
        ):
            self.blocker(1, "Download PDF missing its button, <button id=\"cx-pdf\">")
        rules = css_rules(self.style_text)
        if "@media print" not in self.style_text:
            self.blocker(1, "Download PDF missing its print stylesheet, @media print")
        page_rule = False
        for selector, body in rules:
            if selector.startswith("@page") and "size:" in _squash(body):
                page_rule = True
                break
        if not page_rule:
            self.blocker(1, "Download PDF missing @page sizing inside the print block")
        if "window.print(" not in self.script_text:
            self.blocker(1, "Download PDF missing its click handler, no window.print() call")

    def check_regions(self):
        for slide in self.slides:
            if not slide.attrs.get("data-region"):
                self.warning(slide.line, "slide has no data-region attribute")
        for screen in find_all(self.root, lambda n: n.has_class("mock-screen")):
            if not screen.attrs.get("data-screen"):
                self.warning(screen.line, "mock-screen has no data-screen attribute")

    def check_dark_print(self):
        dark_slides = [s for s in self.slides if s.has_class("dark")]
        for slide in dark_slides:
            layer = None
            for svg in find_all(slide, lambda n: n.tag == "svg"):
                if svg.has_class("print-bg"):
                    layer = svg
                    break
            if layer is None:
                self.blocker(
                    slide.line,
                    "dark slide has no print background layer (.print-bg SVG)",
                )
        if not dark_slides:
            return
        rules = css_rules(self.style_text)
        if not has_rule(rules, ".print-bg", "display:block"):
            self.blocker(
                1,
                "dark slides present but no @media print rule for .print-bg",
            )

    # -- driver ------------------------------------------------------------
    def check_slide_count(self):
        count = len(self.slides)
        if count == 0:
            self.blocker(1, "the file has no <section class=\"slide\">, so there is no deck to audit")
        elif count < MIN_SLIDES:
            self.warning(
                1,
                "the deck has %d slide%s; the standard calls a full-arc deck under %d slides "
                "under-built" % (count, "" if count == 1 else "s", MIN_SLIDES),
            )

    def run(self):
        self.check_slide_count()
        self.check_structure()
        self.check_footers()
        self.check_title_slide()
        self.check_eyebrows()
        self.check_charts()
        self.check_template_syntax()
        self.check_copy()
        if self.stage == "harness":
            self.check_canvas_rules()
            self.check_pdf()
            self.check_regions()
            self.check_dark_print()
        return self.findings


def detect_stage(html):
    for marker in HARNESS_MARKERS:
        if marker in html:
            return "harness"
    return "plain"


def audit_text(html, path, stage=None):
    if stage is None:
        stage = detect_stage(html)
    audit = Audit(path, html, stage)
    findings = audit.run()
    findings.sort(key=lambda f: (f["line"], 0 if f["severity"] == "blocker" else 1, f["message"]))
    counts = {
        "blocker": sum(1 for f in findings if f["severity"] == "blocker"),
        "warning": sum(1 for f in findings if f["severity"] == "warning"),
    }
    return {
        "file": path,
        "stage": stage,
        "findings": findings,
        "counts": counts,
        "slides": len(audit.slides),
    }


def audit_file(path, stage=None):
    with open(path, "r", encoding="utf-8") as handle:
        html = handle.read()
    return audit_text(html, path, stage)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Static audit of a Bison Fund deck against the deck standard. "
            "It reads the file, it does not render it: overflow, note collisions, and "
            "measured bar pixels depend on layout and stay with the browser pass in "
            "references/deck-build-checklist.md."
        ),
        epilog=(
            "Findings print as '<file>:<line>: <severity> <message>', then a summary line. "
            "Exit 0 when clean, 1 when there is any finding. The audit is a static read of "
            "the file; layout-dependent problems are the browser pass in "
            "references/deck-build-checklist.md, not this script."
        ),
    )
    parser.add_argument("deck", help="path to the deck html file")
    parser.add_argument(
        "--stage",
        choices=["plain", "harness"],
        default=None,
        help="audit stage; defaults to auto-detect from the file contents",
    )
    parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="emit {file, stage, findings, counts} as json",
    )
    args = parser.parse_args(argv)

    try:
        result = audit_file(args.deck, args.stage)
    except IOError as exc:
        sys.stderr.write("deck_audit: cannot read %s: %s\n" % (args.deck, exc))
        return 2

    if args.as_json:
        print(json.dumps(result, indent=2))
    else:
        for finding in result["findings"]:
            print(
                "%s:%d: %s %s"
                % (result["file"], finding["line"], finding["severity"], finding["message"])
            )
        counts = result["counts"]
        total = counts["blocker"] + counts["warning"]
        if total == 0:
            print(
                "%s: clean (stage %s, %d slides)"
                % (result["file"], result["stage"], result["slides"])
            )
        else:
            print(
                "%s: %d findings (%d blockers, %d warnings), stage %s, %d slides"
                % (
                    result["file"],
                    total,
                    counts["blocker"],
                    counts["warning"],
                    result["stage"],
                    result["slides"],
                )
            )

    return 1 if result["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
