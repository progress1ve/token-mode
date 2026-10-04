import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("installer", ROOT / "scripts/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class Helpers(unittest.TestCase):
    def test_modes_are_persistent_and_isolated(self):
        with tempfile.TemporaryDirectory() as tmp:
            def call(mode, chat):
                return subprocess.check_output([sys.executable, str(ROOT / "skills/token-mode/scripts/mode.py"), mode, "--chat", chat, "--state-dir", tmp], text=True).strip()
            self.assertEqual(call("detailed", "a"), "token-mode: detailed")
            self.assertEqual(call("get", "a"), "token-mode: detailed")
            self.assertEqual(call("get", "b"), "token-mode: economy")
            self.assertEqual(call("economy", "a"), "token-mode: economy")
            self.assertEqual(len(list(Path(tmp).glob("*.json"))), 1)
            self.assertEqual(json.loads(next(Path(tmp).glob("*.json")).read_text()), {"mode": "economy"})

    def test_update_preserves_user_files_and_instructions(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "skill"
            rules = Path(tmp) / "rules.md"
            rules.write_text("Owner rules\n", encoding="utf-8")
            installer.install(target, rules)
            (target / "notes.md").write_text("Keep me", encoding="utf-8")
            with self.assertRaises(ValueError):
                installer.install(target, rules)
            installer.install(target, rules, True)
            self.assertEqual((target / "notes.md").read_text(), "Keep me")
            text = rules.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("Owner rules\n"))
            self.assertEqual(text.count(installer.START), 1)

    def test_bad_markers_fail_before_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "skill"
            rules = Path(tmp) / "rules.md"
            rules.write_text(installer.START)
            with self.assertRaises(ValueError):
                installer.install(target, rules)
            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
