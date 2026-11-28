import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class CheckLayersTests(unittest.TestCase):
    def test_check_layers_script_passes(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check_layers.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=result.stderr or result.stdout,
        )


if __name__ == "__main__":
    unittest.main()