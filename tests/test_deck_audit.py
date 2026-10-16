"""Tests for skills/deck-build/scripts/deck_audit.py.

The two required tests run the audit against the real shipped templates:

  (a) templates/deck-skeleton.html in plain mode. The shipped skeleton audits
      clean: 41 slides, correct footers, one title element on the title slide,
      no eyebrow problems, no leftover template syntax, and no acronym in the
      rendered copy.

  (b) a harness-stage deck assembled in a temp directory by taking
      templates/commentable-deck-harness.html and inserting two slides from
      deck-skeleton.html into a mock-screen with a data-region and a
      data-screen. This one must audit clean.

The remaining tests exercise the detectors against the same real skeleton with
a single mutation applied, so no markup is invented from nothing.

Run with: python3 -m unittest discover -s tests -v
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "skills", "deck-build", "scripts")
TEMPLATES = os.path.join(REPO_ROOT, "skills", "deck-build", "templates")
SKELETON = os.path.join(TEMPLATES, "deck-skeleton.html")
HARNESS = os.path.join(TEMPLATES, "commentable-deck-harness.html")
AUDIT = os.path.join(SCRIPTS_DIR, "deck_audit.py")

if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import deck_audit  # noqa: E402

HARNESS_SLIDE_MARKER = (
    '<!-- your slides here, each <section class="slide" data-region="sNN.slug"> ... </section> -->'
)
EM_DASH = "\u2014"
MIDDLE_DOT = "\u00b7"


def read(path):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def skeleton_slides():
    """Real slide blocks from the shipped skeleton, body only."""
    body = read(SKELETON).split("<body>", 1)[1]
    return re.findall(r'^<section class="slide[^"]*">.*?^</section>', body, re.S | re.M)


def renumber_footer(slide_html, number, total):
    return re.sub(
        r'(<span class="pageno">)[^<]*(</span>)',
        lambda m: m.group(1) + "%02d / %02d" % (number, total) + m.group(2),
        slide_html,
    )


def assemble_harness_deck():
    """Build a harness-stage deck: the shipped harness plus two real slides."""
    harness = read(HARNESS)
    slides = skeleton_slides()
    # indexes 1 and 2 are light Overview slides with a single title and no chart.
    first = slides[1].replace(
        '<section class="slide">',
        '<section class="slide" data-region="s01.executive-summary">',
        1,
    )
    second = slides[2].replace(
        '<section class="slide">',
        '<section class="slide" data-region="s02.what-the-market-says">',
        1,
    )
    first = renumber_footer(first, 1, 2)
    second = renumber_footer(second, 2, 2)
    assert HARNESS_SLIDE_MARKER in harness, "harness placeholder marker not found"
    return harness.replace(HARNESS_SLIDE_MARKER, first + "\n" + second)


def run_cli(path, *args):
    proc = subprocess.run(
        [sys.executable, AUDIT, path] + list(args),
        capture_output=True,
        text=True,
    )
    return proc


class PlainSkeletonTests(unittest.TestCase):
    """(a) The shipped skeleton, plain stage."""

    @classmethod
    def setUpClass(cls):
        cls.result = deck_audit.audit_file(SKELETON, stage="plain")

    def test_slide_count_is_41(self):
        # 41 slides, so the shipped "NN / 41" footers can be judged against it.
        self.assertEqual(self.result["slides"], 41)

    def test_no_structural_blockers(self):
        blockers = [f for f in self.result["findings"] if f["severity"] == "blocker"]
        self.assertEqual(
            blockers, [], "shipped skeleton has structural blockers: %r" % blockers
        )

    def test_footer_checks_genuinely_satisfied(self):
        # Nothing about footers, the title slide, or eyebrows is flagged.
        for key in ("footer", ".foot", "title slide", "eyebrow"):
            hits = [
                f
                for f in self.result["findings"]
                if key in f["message"] and f["severity"] == "blocker"
            ]
            self.assertEqual(hits, [], "unexpected %s finding: %r" % (key, hits))

    def test_skeleton_is_clean(self):
        self.assertEqual(
            self.result["findings"], [], "shipped skeleton findings: %r" % self.result["findings"]
        )

    def test_cli_exit_is_0_when_clean(self):
        proc = run_cli(SKELETON)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("clean", proc.stdout)
        self.assertIn("stage plain", proc.stdout)

    def test_cli_json_shape(self):
        import json

        proc = run_cli(SKELETON, "--json")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["file"], SKELETON)
        self.assertEqual(data["stage"], "plain")
        self.assertEqual(data["counts"]["blocker"], 0)
        self.assertEqual(data["slides"], 41)
        self.assertIsInstance(data["findings"], list)


class HarnessDeckTests(unittest.TestCase):
    """(b) A harness-stage deck assembled from the shipped templates."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="deck-audit-")
        self.addCleanup(shutil.rmtree, self.tmp)
        self.path = os.path.join(self.tmp, "deck.html")
        with open(self.path, "w", encoding="utf-8") as handle:
            handle.write(assemble_harness_deck())

    def test_stage_auto_detects_harness(self):
        self.assertEqual(deck_audit.detect_stage(read(self.path)), "harness")

    def test_assembled_deck_audits_clean(self):
        result = deck_audit.audit_file(self.path)
        self.assertEqual(result["stage"], "harness")
        self.assertEqual(result["slides"], 2)
        self.assertEqual(result["findings"], [], "unexpected findings: %r" % result["findings"])

    def test_cli_exit_is_0_when_clean(self):
        proc = run_cli(self.path)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("clean", proc.stdout)
        self.assertIn("stage harness", proc.stdout)

    def test_harness_chrome_copy_is_not_slide_copy(self):
        # Slide copy rules must scope to text inside .slide elements. Insert a
        # dash and a middle dot into the harness chrome (the bar brand label,
        # which sits outside every slide) and confirm the copy checks stay quiet.
        marker = '<span class="cx-brand">'
        raw = read(HARNESS)
        self.assertIn(marker, raw)
        mutated = raw.replace(marker, marker + EM_DASH + MIDDLE_DOT, 1)
        self.assertGreater(mutated.count(EM_DASH), 0)
        self.assertGreater(mutated.count(MIDDLE_DOT), 0)
        result = deck_audit.audit_text(mutated, HARNESS, stage="harness")
        for finding in result["findings"]:
            self.assertNotIn("em dash", finding["message"], finding)
            self.assertNotIn("middle dot", finding["message"], finding)


class DetectorTests(unittest.TestCase):
    """Single mutations of the real skeleton, so no fixture is invented."""

    def audit_mutated(self, old, new, stage="plain"):
        html = read(SKELETON).replace(old, new)
        self.assertNotEqual(html, read(SKELETON), "mutation %r did not apply" % old)
        return deck_audit.audit_text(html, "mutated.html", stage=stage)

    def blockers(self, result):
        return [f["message"] for f in result["findings"] if f["severity"] == "blocker"]

    def test_footer_total_mismatch(self):
        result = self.audit_mutated("01 / 41", "01 / 24")
        hits = [m for m in self.blockers(result) if "has 41 slides" in m]
        self.assertTrue(hits, self.blockers(result))

    def test_footer_sequence_mismatch(self):
        result = self.audit_mutated('<span class="pageno">03 / 41</span>',
                                    '<span class="pageno">07 / 41</span>')
        hits = [m for m in self.blockers(result) if "document order" in m]
        self.assertTrue(hits, self.blockers(result))

    def test_em_dash_in_slide_copy(self):
        result = self.audit_mutated(
            '<h2 class="title">Sources</h2>',
            '<h2 class="title">Sources %s note</h2>' % EM_DASH,
        )
        hits = [m for m in self.blockers(result) if "em dash" in m]
        self.assertTrue(hits, self.blockers(result))

    def test_middle_dot_in_slide_copy(self):
        result = self.audit_mutated(
            '<h2 class="title">Sources</h2>',
            '<h2 class="title">Sources %s notes</h2>' % MIDDLE_DOT,
        )
        hits = [m for m in self.blockers(result) if "middle dot" in m]
        self.assertTrue(hits, self.blockers(result))

    def test_leftover_template_syntax(self):
        result = self.audit_mutated(
            '<h2 class="title">Sources</h2>',
            '<h2 class="title">{card(x)}</h2>',
        )
        hits = [m for m in self.blockers(result) if "leftover template syntax" in m]
        self.assertTrue(hits, self.blockers(result))

    def test_acronym_in_slide_copy_is_a_warning(self):
        # The shipped skeleton spells out free cash flow, so the detector is
        # exercised by putting the acronym back in a slide title.
        result = self.audit_mutated(
            '<h2 class="title">Sources</h2>',
            '<h2 class="title">FCF walk</h2>',
        )
        warnings = [
            f["message"]
            for f in result["findings"]
            if f["severity"] == "warning" and "acronym in slide copy" in f["message"]
        ]
        self.assertTrue(any("'FCF'" in m for m in warnings), result["findings"])

    def test_tiny_and_unlabeled_bar(self):
        result = self.audit_mutated(
            '<div class="lab">[v]</div><div class="col" style="height:40%;background:var(--chart-1)"></div>',
            '<div class="col" style="height:2%;background:var(--chart-1)"></div>',
        )
        messages = [f["message"] for f in result["findings"]]
        self.assertTrue(any("no labeled value" in m for m in messages), messages)
        self.assertTrue(any("under about" in m for m in messages), messages)

    def test_bar_height_order_contradiction(self):
        html = read(SKELETON)
        # Heights ascend 3, 7 while values descend 7, 3 in one chart.
        old = (
            '<div class="bar"><div class="lab">[v]</div><div class="col" style="height:40%;background:var(--chart-1)"></div><div class="cat">[yr]</div></div>\n'
            '  <div class="bar"><div class="lab">[v]</div><div class="col" style="height:60%;background:var(--chart-1)"></div><div class="cat">[yr]</div></div>'
        )
        new = old.replace('[v]', '3', 1).replace('[v]', '7', 1)
        # first bar value 3, second bar value 7, heights 40 then 60: consistent.
        consistent = deck_audit.audit_text(html.replace(old, new), "m.html", stage="plain")
        self.assertFalse(any("contradict" in f["message"] for f in consistent["findings"]),
                         consistent["findings"])
        swapped = old.replace('[v]', '7', 1).replace('[v]', '3', 1)
        contradicted = deck_audit.audit_text(html.replace(old, swapped), "m.html", stage="plain")
        self.assertTrue(any("contradict" in f["message"] for f in contradicted["findings"]),
                        contradicted["findings"])

    def test_missing_canvas_rule_is_flagged(self):
        html = read(SKELETON)
        result = deck_audit.audit_text(html, "m.html", stage="harness")
        hits = [f for f in result["findings"] if "canvas rule missing" in f["message"]]
        self.assertTrue(hits, result["findings"])

    def test_harness_print_pdf_parts_present(self):
        result = deck_audit.audit_text(read(HARNESS), HARNESS, stage="harness")
        for token in ("Download PDF missing its button", "window.print"):
            self.assertFalse(
                any(token in f["message"] for f in result["findings"]),
                result["findings"],
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
