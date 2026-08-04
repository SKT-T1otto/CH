import hashlib,json,subprocess
from pathlib import Path
import unittest

class Phase1A1OriginalCoreFreezeTest(unittest.TestCase):
    def test_original_40_core_python_files_match(self):
        root=Path(__file__).resolve().parents[1]; manifest=json.loads((root/"docs/chapter3_bser/phase1a1/core_freeze_before.json").read_text()); self.assertEqual(len(manifest["files"]),40)
        for record in manifest["files"]:
            blob=subprocess.check_output(["git","cat-file","blob",f"HEAD:{record['path']}"],cwd=root)
            self.assertEqual(hashlib.sha256(blob).hexdigest(),record["git_blob_sha256"],record["path"])
