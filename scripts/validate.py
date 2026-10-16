#!/usr/bin/env python3
"""Validate the bison-fund-investment-analysis skill package.

Six checks run over the repository tree:

1. frontmatter: every skills/*/SKILL.md opens with a --- line that carries a
   non-empty name and a non-empty description.
2. name: the frontmatter name equals the directory name that holds the file.
3. citation: every backticked path under references/, templates/, or scripts/
   resolves inside the skill that cites it, or inside a skill the citing line
   names, or it is an error.
4. route: every skill named in a route table of the hub SKILL.md exists as a
   directory under skills/.
5. reachable: no directory under skills/ is an orphan. Each one must be named
   by the hub, or by another skill the hub reaches.
6. charset: no em dash (U+2014) and no middle dot (U+00B7) in
   skills/deck-build/templates/*.html and *.css.

Standard library only. No third-party imports, no network access. Python 3.9
and 3.11 both run this file. The repository root is found from this file's own
path, so the script works from any working directory.

Exit 0 when clean, 1 when any finding exists. --json prints the findings as a
JSON list of {path, check, message}.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EM_DASH = "\u2014"
MIDDLE_DOT = "\u00b7"

HUB_NAME = "bison-fund-investment-analysis"
PATH_PREFIXES = ("references/", "templates/", "scripts/")

BACKTICK = re.compile(r"`([^`]+)`")
SKILL_TOKEN = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)+$")

CHECKS = ("frontmatter", "name", "citation", "route", "reachable", "charset")


def repo_root():
    """Return the repository root, from this file's own location."""
    return Path(__file__).resolve().parent.parent


def _read(path):
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _relative(path, root):
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _finding(path, check, message):
    return {"path": path, "check": check, "message": message}


def skill_dirs(root):
    """Every directory under skills/, sorted by name."""
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return []
    return sorted(p.name for p in skills_dir.iterdir() if p.is_dir())


def parse_frontmatter(text):
    """Parse the leading --- block into a dict.

    Returns (data, error). data is None when the block cannot be read at all;
    error is None when it parsed. Quoted and unquoted values both work.
    """
    lines = text.splitlines()
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i >= len(lines):
        return None, "file is empty"
    if lines[i].strip() != "---":
        return None, "no leading --- frontmatter line"
    i += 1
    data = {}
    while i < len(lines):
        raw = lines[i].strip()
        if raw == "---":
            return data, None
        i += 1
        if raw == "" or raw.startswith("#"):
            continue
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        data[key.strip()] = _unquote(value.strip())
    return None, "frontmatter has no closing --- line"


def _unquote(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
        return value[1:-1]
    return value


def _names_in_line(line, skills):
    """Skill names a line names, by backticked token or by plain word."""
    named = set()
    for match in BACKTICK.finditer(line):
        token = match.group(1).strip()
        if token in skills:
            named.add(token)
    for name in skills:
        pattern = r"(?<![a-z0-9-])" + re.escape(name) + r"(?![a-z0-9-])"
        if re.search(pattern, line):
            named.add(name)
    return named


def check_frontmatter_and_names(root, skills):
    findings = []
    for name in skills:
        skill_md = root / "skills" / name / "SKILL.md"
        rel = _relative(skill_md, root)
        if not skill_md.is_file():
            findings.append(_finding(rel, "frontmatter", "no SKILL.md in this skill directory"))
            continue
        text = _read(skill_md)
        data, error = parse_frontmatter(text)
        if error is not None or data is None:
            findings.append(_finding(rel, "frontmatter", "unreadable frontmatter: %s" % (error or "unknown")))
            continue
        declared = data.get("name", "")
        if not declared:
            findings.append(_finding(rel, "frontmatter", "frontmatter has no non-empty name"))
        if not data.get("description", ""):
            findings.append(_finding(rel, "frontmatter", "frontmatter has no non-empty description"))
        if declared and declared != name:
            findings.append(
                _finding(rel, "name", "frontmatter name '%s' does not match directory '%s'" % (declared, name))
            )
    return findings


def check_citations(root, skills):
    findings = []
    skills_dir = root / "skills"
    for md in sorted(skills_dir.rglob("*.md")):
        parts = md.relative_to(skills_dir).parts
        if len(parts) < 2:
            continue
        owner = parts[0]
        for lineno, line in enumerate(_read(md).splitlines(), 1):
            for match in BACKTICK.finditer(line):
                token = match.group(1).strip()
                if not token.startswith(PATH_PREFIXES):
                    continue
                rel = _relative(md, root)
                if (skills_dir / owner / token).exists():
                    continue
                named = sorted(_names_in_line(line, skills))
                resolved = [s for s in named if (skills_dir / s / token).exists()]
                if resolved:
                    continue
                if named:
                    findings.append(
                        _finding(
                            rel,
                            "citation",
                            "line %d: '%s' does not resolve in %s" % (lineno, token, ", ".join(named)),
                        )
                    )
                else:
                    findings.append(
                        _finding(
                            rel,
                            "citation",
                            "line %d: '%s' resolves in no skill and the line names no owning skill"
                            % (lineno, token),
                        )
                    )
    return findings


def check_route_table(root, skills):
    findings = []
    hub = root / "skills" / HUB_NAME / "SKILL.md"
    if not hub.is_file():
        findings.append(_finding(_relative(hub, root), "route", "the hub SKILL.md is missing"))
        return findings
    for lineno, line in enumerate(_read(hub).splitlines(), 1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        for match in BACKTICK.finditer(stripped):
            token = match.group(1).strip()
            if not SKILL_TOKEN.match(token):
                continue
            if not (root / "skills" / token).is_dir():
                findings.append(
                    _finding(
                        _relative(hub, root),
                        "route",
                        "line %d: route table names '%s', no such skill directory" % (lineno, token),
                    )
                )
    return findings


def check_reachable(root, skills):
    findings = []
    if HUB_NAME not in skills:
        findings.append(_finding("skills/", "reachable", "the hub skill directory is missing"))
        return findings

    def names_in(name):
        found = set()
        for md in (root / "skills" / name).rglob("*.md"):
            text = _read(md)
            for other in skills:
                if other == name:
                    continue
                pattern = r"(?<![a-z0-9-])" + re.escape(other) + r"(?![a-z0-9-])"
                if re.search(pattern, text):
                    found.add(other)
        return found

    reachable = {HUB_NAME}
    frontier = [HUB_NAME]
    while frontier:
        current = frontier.pop()
        for other in names_in(current):
            if other not in reachable:
                reachable.add(other)
                frontier.append(other)

    for name in skills:
        if name not in reachable:
            findings.append(
                _finding("skills/%s/" % name, "reachable", "orphan skill: nothing reachable from the hub names it")
            )
    return findings


def check_charset(root):
    findings = []
    templates = root / "skills" / "deck-build" / "templates"
    if not templates.is_dir():
        return findings
    candidates = sorted(templates.glob("*.html")) + sorted(templates.glob("*.css"))
    for path in candidates:
        rel = _relative(path, root)
        for lineno, line in enumerate(_read(path).splitlines(), 1):
            if EM_DASH in line:
                findings.append(_finding(rel, "charset", "em dash (U+2014) at line %d" % lineno))
            if MIDDLE_DOT in line:
                findings.append(_finding(rel, "charset", "middle dot (U+00B7) at line %d" % lineno))
    return findings


def collect_findings(root):
    """Run every check over root and return the findings in check order."""
    skills = skill_dirs(root)
    findings = []
    if not skills:
        findings.append(_finding("skills/", "frontmatter", "no skill directories under skills/"))
        return findings
    findings.extend(check_frontmatter_and_names(root, skills))
    findings.extend(check_citations(root, skills))
    findings.extend(check_route_table(root, skills))
    findings.extend(check_reachable(root, skills))
    findings.extend(check_charset(root))
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate the skill package.")
    parser.add_argument("--json", action="store_true", help="print findings as a JSON list")
    args = parser.parse_args(argv)

    root = repo_root()
    skills = skill_dirs(root)
    findings = collect_findings(root)

    verdict = "FAIL" if findings else "OK"
    summary = "validate: %d skills, %d checks, %d finding(s). %s" % (len(skills), len(CHECKS), len(findings), verdict)

    if args.json:
        payload = [{"path": f["path"], "check": f["check"], "message": f["message"]} for f in findings]
        print(json.dumps(payload, indent=2))
        print(summary, file=sys.stderr)
    else:
        for f in findings:
            print("%s: %s" % (f["path"], f["message"]))
        print(summary)

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
