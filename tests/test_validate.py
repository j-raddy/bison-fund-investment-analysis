"""Tests for scripts/validate.py.

Each test builds a temporary copy of the repository's skills tree, applies one
defect, and asserts the validator reports it. One test asserts the real tree is
clean. Standard library only.
"""

import contextlib
import importlib.util
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

REAL_ROOT = Path(__file__).resolve().parent.parent


def load_validator():
    spec = importlib.util.spec_from_file_location("bfia_validate", REAL_ROOT / "scripts" / "validate.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validate = load_validator()


class ValidatorTreeTests(unittest.TestCase):
    """Fail classes, each applied to a private copy of the skills tree."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="bfia-validate-")
        self.addCleanup(lambda: shutil.rmtree(self._tmp, ignore_errors=True))
        self.root = Path(self._tmp) / "repo"
        shutil.copytree(REAL_ROOT / "skills", self.root / "skills")

    def findings(self):
        return validate.collect_findings(self.root)

    def skill_file(self, skill, name="SKILL.md"):
        return self.root / "skills" / skill / name

    def assert_finding(self, check, path_fragment):
        found = [f for f in self.findings() if f["check"] == check and path_fragment in f["path"]]
        self.assertTrue(found, "expected a %s finding for %s, got %r" % (check, path_fragment, self.findings()))
        return found[0]

    def test_missing_frontmatter(self):
        path = self.skill_file("dcf-model")
        path.write_text("# DCF Model\n\nNo frontmatter block above this line.\n", encoding="utf-8")
        self.assert_finding("frontmatter", "dcf-model/SKILL.md")

    def test_name_that_does_not_match_its_directory(self):
        path = self.skill_file("pitch-deals")
        text = path.read_text(encoding="utf-8").replace("name: pitch-deals", "name: pitch-dealz", 1)
        path.write_text(text, encoding="utf-8")
        finding = self.assert_finding("name", "pitch-deals/SKILL.md")
        self.assertIn("pitch-dealz", finding["message"])

    def test_reference_path_that_resolves_nowhere(self):
        path = self.skill_file("pitch-deals")
        text = path.read_text(encoding="utf-8")
        path.write_text(text + "\nSee `references/not-anywhere.md` for the detail.\n", encoding="utf-8")
        finding = self.assert_finding("citation", "pitch-deals/SKILL.md")
        self.assertIn("not-anywhere.md", finding["message"])

    def test_cross_skill_citation_without_naming_the_owner(self):
        path = self.skill_file("pitch-deals")
        text = path.read_text(encoding="utf-8")
        path.write_text(text + "\nThe writing check is in `references/ai-writing-check.md`.\n", encoding="utf-8")
        finding = self.assert_finding("citation", "pitch-deals/SKILL.md")
        self.assertIn("names no owning skill", finding["message"])

    def test_hub_route_table_naming_a_skill_that_does_not_exist(self):
        path = self.skill_file("bison-fund-investment-analysis")
        text = path.read_text(encoding="utf-8")
        path.write_text(text + "\n| Value it again | `pitch-nope` |\n", encoding="utf-8")
        finding = self.assert_finding("route", "bison-fund-investment-analysis/SKILL.md")
        self.assertIn("pitch-nope", finding["message"])

    def test_orphan_skill_directory(self):
        orphan = self.root / "skills" / "orphan-skill"
        orphan.mkdir()
        (orphan / "SKILL.md").write_text(
            "---\nname: orphan-skill\ndescription: \"Nothing routes to this skill.\"\n---\n\n# Orphan\n",
            encoding="utf-8",
        )
        self.assert_finding("reachable", "skills/orphan-skill/")

    def test_em_dash_in_a_deck_build_template(self):
        path = self.root / "skills" / "deck-build" / "templates" / "deck-house.css"
        text = path.read_text(encoding="utf-8")
        path.write_text(text + "\n/* a stray em dash \u2014 right here */\n", encoding="utf-8")
        finding = self.assert_finding("charset", "deck-house.css")
        self.assertIn("U+2014", finding["message"])

    def test_middle_dot_in_a_deck_build_template(self):
        path = self.root / "skills" / "deck-build" / "templates" / "ndsu-design-tokens.css"
        text = path.read_text(encoding="utf-8")
        path.write_text(text + "\n/* a stray middle dot \u00b7 right here */\n", encoding="utf-8")
        finding = self.assert_finding("charset", "ndsu-design-tokens.css")
        self.assertIn("U+00B7", finding["message"])

    def test_clean_copy_has_no_findings(self):
        self.assertEqual(self.findings(), [])


class FrontmatterReaderTests(unittest.TestCase):
    """The YAML-ish reader, on quoted and unquoted values."""

    def test_reads_quoted_and_unquoted_values(self):
        text = '---\nname: demo-skill\ndescription: "A quoted: value, with a colon."\n---\n\nbody\n'
        data, error = validate.parse_frontmatter(text)
        self.assertIsNone(error)
        self.assertEqual(data["name"], "demo-skill")
        self.assertEqual(data["description"], "A quoted: value, with a colon.")

    def test_rejects_a_file_with_no_leading_marker(self):
        data, error = validate.parse_frontmatter("# Heading\n\nbody\n")
        self.assertIsNone(data)
        self.assertIsNotNone(error)

    def test_rejects_an_unclosed_block(self):
        data, error = validate.parse_frontmatter("---\nname: demo-skill\n\nbody\n")
        self.assertIsNone(data)
        self.assertIsNotNone(error)


class RealRepoTests(unittest.TestCase):
    """The shipped tree, as it stands."""

    def test_real_repo_has_no_findings(self):
        findings = validate.collect_findings(REAL_ROOT)
        self.assertEqual(findings, [], "the real repo has findings: %r" % (findings,))

    def test_cli_exits_zero_on_the_real_repo(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = validate.main([])
        self.assertEqual(code, 0, stdout.getvalue() + stderr.getvalue())
        self.assertIn("OK", stdout.getvalue())

    def test_json_output_is_a_findings_list(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(io.StringIO()):
            validate.main(["--json"])
        payload = json.loads(stdout.getvalue())
        self.assertIsInstance(payload, list)
        for item in payload:
            self.assertEqual(sorted(item.keys()), ["check", "message", "path"])


if __name__ == "__main__":
    unittest.main()
