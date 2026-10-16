"""Tests for the DCF script.

The model math is otherwise checked only by running --demo by hand, so these tests pin the
demo record, the formulas behind it, and the key lookup order the README documents. They need
no key and no network.
"""
import importlib.util
import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "skills", "dcf-model", "scripts", "fmp_dcf.py")


def load_module():
    spec = importlib.util.spec_from_file_location("fmp_dcf", SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fmp_dcf = load_module()


class TestMath(unittest.TestCase):
    def test_dcf_formula(self):
        stream = [100.0, 115.0, 130.0, 145.0, 160.0]
        wacc, g, net_debt, shares = 0.09, 0.025, 500.0, 100.0
        r = fmp_dcf.dcf(stream, wacc, g, net_debt, shares)

        pv = sum(f / (1 + wacc) ** (i + 1) for i, f in enumerate(stream))
        tv = stream[-1] * (1 + g) / (wacc - g)
        pv_tv = tv / (1 + wacc) ** len(stream)

        self.assertAlmostEqual(r["pv_fcf"], pv, places=6)
        self.assertAlmostEqual(r["terminal_value"], tv, places=6)
        self.assertAlmostEqual(r["pv_terminal"], pv_tv, places=6)
        self.assertAlmostEqual(r["enterprise_value"], pv + pv_tv, places=6)
        self.assertAlmostEqual(r["equity_value"], pv + pv_tv + net_debt, places=6)
        self.assertAlmostEqual(r["per_share"], (pv + pv_tv + net_debt) / shares, places=6)
        self.assertAlmostEqual(r["tv_share"], pv_tv / (pv + pv_tv), places=6)

    def test_sensitivity_grid_shape_and_direction(self):
        grid = fmp_dcf.grid(100.0, [0.08, 0.09, 0.10], [0.02, 0.025, 0.03], 500.0, 100.0)
        self.assertEqual(sorted(grid.keys()), ["0.08", "0.09", "0.10"])
        for row in grid.values():
            self.assertEqual(len(row), 3)
            # A higher terminal growth in the same row is worth more.
            self.assertLess(row[0], row[1])
            self.assertLess(row[1], row[2])
        # A higher discount rate on the same growth column is worth less.
        self.assertGreater(grid["0.09"][1], grid["0.10"][1])

    def test_demo_record_is_stable(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            fmp_dcf.demo()
        out = buf.getvalue()
        self.assertIn("math verified", out)
        for label, value in (("pv_fcf", "495.63"), ("terminal_value", "2523.08"),
                             ("enterprise_value", "2135.46"), ("equity_value", "2635.46"),
                             ("per_share", "26.35"), ("tv_share", "0.77")):
            self.assertIn(label, out)
            self.assertIn(value, out)


class TestKeyLookup(unittest.TestCase):
    """The lookup order the README documents: env, then the secrets file, then its dotfile, then
    the config path. The tests run in a temporary home so a real key on the machine is never read
    and never printed."""

    def setUp(self):
        self.home = tempfile.mkdtemp()
        self.old_home = os.environ.get("HOME")
        self.old_key = os.environ.pop("FMP_API_KEY", None)
        os.environ["HOME"] = self.home
        self.env_home = self.home
        os.environ.pop("FMP_API_KEY", None)

    def tearDown(self):
        if self.old_home is None:
            os.environ.pop("HOME", None)
        else:
            os.environ["HOME"] = self.old_home
        os.environ.pop("FMP_API_KEY", None)
        if self.old_key is not None:
            os.environ["FMP_API_KEY"] = self.old_key

    def write(self, relpath, text):
        path = os.path.join(self.home, relpath)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            fh.write(text)
        return path

    def test_empty_when_nothing_is_set(self):
        self.assertEqual(fmp_dcf.load_key(), "")

    def test_environment_wins(self):
        self.write(".hermes/secrets/fmp_api_key", "from-file")
        os.environ["FMP_API_KEY"] = "from-env"
        self.assertEqual(fmp_dcf.load_key(), "from-env")

    def test_secrets_file_order(self):
        self.write(".config/fmp/api_key", "from-config")
        self.assertEqual(fmp_dcf.load_key(), "from-config")
        self.write(".hermes/secrets/.fmp_api_key", "from-dotfile")
        self.assertEqual(fmp_dcf.load_key(), "from-dotfile")
        self.write(".hermes/secrets/fmp_api_key", "from-secrets")
        self.assertEqual(fmp_dcf.load_key(), "from-secrets")

    def test_wrapper_prefix_is_stripped(self):
        self.write(".hermes/secrets/fmp_api_key", "FMP_API_KEY=abc123\n")
        self.assertEqual(fmp_dcf.load_key(), "abc123")

    def test_surrounding_whitespace_is_stripped(self):
        self.write(".hermes/secrets/fmp_api_key", "  abc123  \n")
        self.assertEqual(fmp_dcf.load_key(), "abc123")

    def test_demo_never_prints_the_key(self):
        sentinel = "SENTINELKEY1234567890"
        env = dict(os.environ)
        env["FMP_API_KEY"] = sentinel
        proc = subprocess.run([sys.executable, SCRIPT, "--demo"],
                              capture_output=True, text=True, env=env, cwd=REPO)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn(sentinel, proc.stdout + proc.stderr)


class TestCommandLine(unittest.TestCase):
    def test_no_arguments_prints_help(self):
        proc = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True, cwd=REPO)
        self.assertIn("usage", (proc.stdout + proc.stderr).lower())

    def test_live_run_without_a_key_exits_with_a_plain_message(self):
        env = dict(os.environ)
        env.pop("FMP_API_KEY", None)
        env["HOME"] = tempfile.mkdtemp()
        proc = subprocess.run([sys.executable, SCRIPT, "UBER"],
                              capture_output=True, text=True, env=env, cwd=REPO)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("No FMP key", proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
