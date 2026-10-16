#!/usr/bin/env python3
"""Tests for setup.py, and for the handoff from setup to the model script.

Run from the repository root:

    python3 tests/test_setup.py

No network is needed: the live verification calls are replaced with stubs, so the
suite tests the branch logic, the key writing, and the config record. One optional
test exercises a real free-source call and skips itself when the network is down.

Why this file exists: a key-path mismatch shipped once because nothing joined
setup's write to the script's read. test_handoff_is_readable_by_the_model_script
is that join, and it fails on the version that shipped.
"""
import builtins, fcntl, importlib.util, io, json, os, pty, shutil, sys, tempfile, time, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_PATH = os.path.join(ROOT, "setup.py")

# setup.py resolves its paths at import time, so point HOME at a sandbox first.
SANDBOX = tempfile.mkdtemp(prefix="bison-test-home-")
os.environ["HOME"] = SANDBOX
os.environ["BISON_CONTACT"] = "test@example.edu"
os.environ.pop("FMP_API_KEY", None)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


setup = load("bison_setup", os.path.join(ROOT, "setup.py"))
fmp_dcf = load("bison_fmp_dcf", os.path.join(ROOT, "skills/dcf-model/scripts/fmp_dcf.py"))


class SetupCase(unittest.TestCase):
    """Drives setup.main() with the terminal prompts stubbed out."""

    def setUp(self):
        # The suite drives the numbered fallback, which is what piped and Windows
        # use. The arrow-key and masked prompts are covered by InteractivePrompt,
        # which runs them in a child that has a real terminal.
        setup.raw_supported = lambda: False
        if os.path.isdir(setup.KEY_DIR):
            shutil.rmtree(setup.KEY_DIR)
        if os.path.exists(setup.CONFIG):
            os.remove(setup.CONFIG)
        os.environ.pop("FMP_API_KEY", None)

    def drive(self, answers, secret=""):
        """answers: what the menu and the provider-name prompt return.

        Returns the exit code. The script's own output is captured, so the suite
        result is not buried in menu text; test_the_key_is_never_printed reads it
        through self.output.
        """
        replies = iter(list(answers))
        real_input, real_getpass, real_stdout = builtins.input, setup.getpass.getpass, sys.stdout
        buf = io.StringIO()
        builtins.input = lambda prompt="": next(replies)
        setup.getpass.getpass = lambda prompt="", stream=None: secret
        sys.stdin.isatty = lambda: True
        sys.stdout = buf
        try:
            code = setup.main()
        except SystemExit as e:
            code = e.code
        finally:
            builtins.input, setup.getpass.getpass, sys.stdout = real_input, real_getpass, real_stdout
        self.output = buf.getvalue()
        return code

    def config(self):
        with open(setup.CONFIG) as f:
            return json.load(f)

    # --- finding 1: an out-of-range menu number must not pick another source ---

    def test_zero_and_negative_do_not_select_a_source(self):
        for bad in ("0", "-1", "-4", "5", "99"):
            with self.subTest(input=bad):
                code = self.drive([bad])
                self.assertIsInstance(code, str, "should exit with a message, not a config")
                self.assertIn("Pick a number", code)
                self.assertFalse(os.path.exists(setup.CONFIG),
                                 "nothing may be written for the rejected input %s" % bad)

    def test_a_word_is_rejected(self):
        code = self.drive(["one"])
        self.assertIn("Not a number", code)
        self.assertFalse(os.path.exists(setup.CONFIG))

    # --- the four branches ---

    def test_fmp_key_that_fails_verification_is_kept_unverified(self):
        setup.verify_fmp = lambda key: (_ for _ in ()).throw(RuntimeError("HTTP Error 401"))
        code = self.drive(["1"], secret="sk_dummy_key_12345")
        self.assertEqual(code, 0)
        cfg = self.config()
        self.assertEqual(cfg["provider"], "fmp")
        self.assertFalse(cfg["keys"]["fmp"]["verified"])
        with open(os.path.join(setup.KEY_DIR, "fmp.key")) as f:
            self.assertEqual(f.read().strip(), "sk_dummy_key_12345")

    def test_an_empty_key_is_refused_and_writes_nothing(self):
        code = self.drive(["1"], secret="")
        self.assertIsInstance(code, str)
        self.assertIn("No key given", code)
        self.assertFalse(os.path.exists(setup.CONFIG))

    def test_fmp_key_that_verifies_is_marked_verified(self):
        setup.verify_fmp = lambda key: "AAPL quoted at 250.0"
        self.drive(["1"], secret="sk_good")
        self.assertTrue(self.config()["keys"]["fmp"]["verified"])

    def test_other_provider_is_stored_and_named(self):
        code = self.drive(["3", "finnhub"], secret="abc123")
        self.assertEqual(code, 0)
        cfg = self.config()
        self.assertEqual(cfg["provider"], "other")
        self.assertIn("finnhub", cfg["keys"])
        self.assertFalse(cfg["keys"]["finnhub"]["verified"])

    def test_free_source_records_the_choice(self):
        setup.verify_free = lambda: "SEC EDGAR and the Treasury yield curve both answered"
        self.drive(["2"])
        self.assertEqual(self.config()["provider"], "free")

    def test_bloomberg_records_nothing_but_the_choice(self):
        self.drive(["4"])
        cfg = self.config()
        self.assertEqual(cfg["provider"], "bloomberg")
        self.assertFalse(os.path.exists(setup.KEY_DIR))

    # --- finding 4: the config carries only what a reader consumes ---

    def test_config_carries_only_the_fields_that_are_read(self):
        setup.verify_free = lambda: "ok"
        self.drive(["2"])
        cfg = self.config()
        self.assertEqual(sorted(cfg), ["configured_at", "keys", "provider"])

    # --- key handling ---

    def test_key_file_is_owner_only(self):
        setup.verify_fmp = lambda key: "ok"
        self.drive(["1"], secret="sk_secret")
        mode = os.stat(os.path.join(setup.KEY_DIR, "fmp.key")).st_mode & 0o777
        self.assertEqual(mode, 0o600)

    def test_the_key_is_never_printed(self):
        setup.verify_fmp = lambda key: "ok"
        self.drive(["1"], secret="sk_must_not_appear")
        self.assertNotIn("sk_must_not_appear", self.output)

    def test_eof_exits_with_a_message(self):
        real_input = builtins.input
        builtins.input = lambda prompt="": (_ for _ in ()).throw(EOFError())
        sys.stdin.isatty = lambda: True
        try:
            with self.assertRaises(SystemExit) as ctx:
                setup.main()
        finally:
            builtins.input = real_input
        self.assertIn("No input", str(ctx.exception))

    def test_rerun_keeps_an_existing_key(self):
        setup.verify_fmp = lambda key: "ok"
        self.drive(["1"], secret="sk_first")
        self.drive(["4"])                      # switch source
        self.assertIn("fmp", self.config()["keys"])
        with open(os.path.join(setup.KEY_DIR, "fmp.key")) as f:
            self.assertEqual(f.read().strip(), "sk_first")

    # --- the handoff that shipped broken ---

    def test_handoff_is_readable_by_the_model_script(self):
        """setup writes the key; fmp_dcf.load_key must find it. This is the bug
        that shipped: setup wrote keys/fmp.key while the script read fmp_api_key."""
        setup.verify_fmp = lambda key: "ok"
        self.drive(["1"], secret="sk_handoff_key")
        os.environ.pop("FMP_API_KEY", None)
        self.assertEqual(fmp_dcf.load_key(), "sk_handoff_key",
                         "the model script cannot read the key setup wrote")

    def test_detection_reports_a_stored_key(self):
        setup.verify_fmp = lambda key: "ok"
        self.drive(["1"], secret="sk_seen")
        found = setup.detect()
        self.assertTrue(any("fmp key is stored" in line for line in found), found)


class KeySanitizing(unittest.TestCase):
    def test_bracketed_paste_markers_are_stripped(self):
        self.assertEqual(setup.sanitize_key("\x1b[200~sk_abc123\x1b[201~"), "sk_abc123")

    def test_an_ordinary_key_survives_unchanged(self):
        self.assertEqual(setup.sanitize_key("sk-abc_123.456"), "sk-abc_123.456")

    def test_whitespace_is_dropped(self):
        self.assertEqual(setup.sanitize_key("  sk_abc \n"), "sk_abc")


def run_on_a_terminal(code, feed, wait_for, timeout=10):
    """Run `code` in a child that has a real terminal, then answer its prompt.

    Waits until `wait_for` appears on the child's screen before sending the keys.
    Sending them earlier lands while the terminal is still in canonical mode,
    where the line discipline echoes them and swallows them, and the child then
    waits forever for input it already received.

    Returns (what the screen showed, the repr of the child's result).
    """
    out_path = os.path.join(SANDBOX, "pty-result.txt")
    if os.path.exists(out_path):
        os.remove(out_path)
    src = ("import importlib.util as u\n"
           "s = u.spec_from_file_location('bison_setup', %r)\n"
           "m = u.module_from_spec(s)\n"
           "s.loader.exec_module(m)\n"
           "result = None\n"
           "%s\n"
           "open(%r, 'w').write(repr(result))\n" % (SETUP_PATH, code, out_path))
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(sys.executable, [sys.executable, "-c", src])
    # Non-blocking, so a child waiting for input cannot hang the suite past the deadline.
    fcntl.fcntl(fd, fcntl.F_SETFL, fcntl.fcntl(fd, fcntl.F_GETFL) | os.O_NONBLOCK)
    screen, done, deadline = b"", False, time.time() + timeout
    while wait_for.encode() not in screen and time.time() < deadline:
        try:
            screen += os.read(fd, 65536)
        except BlockingIOError:
            pass
        except OSError:
            break
        time.sleep(0.02)
    try:
        os.write(fd, feed)
    except OSError as e:
        # The child is already gone. Say so, and keep its screen for the report.
        screen += ("\n[the child was gone before the keys were sent: %s]" % e).encode()
    while time.time() < deadline and not done:
        try:
            chunk = os.read(fd, 65536)
            screen += chunk
        except BlockingIOError:
            pass
        except OSError:
            break
        try:
            done = bool(os.waitpid(pid, os.WNOHANG)[0])
        except ChildProcessError:
            done = True
        time.sleep(0.05)
    if not done:
        try:
            os.kill(pid, 9)
            os.waitpid(pid, 0)
        except (ProcessLookupError, ChildProcessError):
            pass
    os.close(fd)
    result = open(out_path).read() if os.path.exists(out_path) else None
    return screen.decode(errors="replace"), result


def child_reported(screen):
    """The assertion message, so a failure shows what the child actually said."""
    return "the child's screen showed:\n%s" % screen


class InteractivePrompt(unittest.TestCase):
    """The arrow-key menu and the masked key prompt, on a real terminal."""

    OPTIONS = "[('a', ''), ('b', ''), ('c', '')]"

    # The child opens a terminal, asks, and stores its answer in `result`.
    def menu(self, feed):
        code = ("with m.Terminal() as t:\n"
                "    result = m.choose('pick one', %s, t)" % self.OPTIONS)
        return run_on_a_terminal(code, feed, "pick one")

    def hidden(self, feed):
        code = ("with m.Terminal() as t:\n"
                "    result = t.line('Paste key: ', secret=True)")
        return run_on_a_terminal(code, feed, "Paste key:")

    def test_down_arrow_then_enter_selects_the_second_option(self):
        screen, result = self.menu(b"\x1b[B\r")
        self.assertEqual(result, "2", child_reported(screen))

    def test_up_arrow_wraps_to_the_last_option(self):
        screen, result = self.menu(b"\x1b[A\r")
        self.assertEqual(result, "3", child_reported(screen))

    def test_typing_a_number_still_selects(self):
        screen, result = self.menu(b"3")
        self.assertEqual(result, "3", child_reported(screen))

    def test_masked_input_shows_a_star_per_character_and_hides_the_key(self):
        screen, result = self.hidden(b"sk_abc123\r")
        self.assertEqual(result, "'sk_abc123'", child_reported(screen))
        self.assertIn("*********", screen, child_reported(screen))
        self.assertNotIn("sk_abc123", screen, child_reported(screen))

    def test_backspace_deletes_a_character(self):
        screen, result = self.hidden(b"sk_abX\x7fc\r")
        self.assertEqual(result, "'sk_abc'", child_reported(screen))

    def test_an_empty_line_reads_as_empty(self):
        screen, result = self.hidden(b"\r")
        self.assertEqual(result, "''", child_reported(screen))


class LiveCheck(unittest.TestCase):
    """One real call, to prove the keyless path still answers. Skips offline."""

    def test_free_sources_answer(self):
        try:
            setup.verify_free()
        except Exception as e:
            self.skipTest("no network, or the free source is down: %s" % str(e)[:80])


if __name__ == "__main__":
    try:
        unittest.main(verbosity=2)
    finally:
        shutil.rmtree(SANDBOX, ignore_errors=True)
