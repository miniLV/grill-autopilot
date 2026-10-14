import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(*args):
    return subprocess.run([sys.executable, "-m", "ledger", *args], cwd=ROOT, capture_output=True, text=True)


class CliTest(unittest.TestCase):
    def test_add_then_list(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "l.json")
            self.assertEqual(run("--file", path, "add", "2026-01-05", "12.5", "food", "lunch").returncode, 0)
            result = run("--file", path, "list")
            self.assertEqual(result.stdout, "2026-01-05 12.50 food lunch\n")


if __name__ == "__main__":
    unittest.main()
