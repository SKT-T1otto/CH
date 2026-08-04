import ast
import hashlib
import json
from pathlib import Path
import unittest


class Phase1ACoreFreezeTest(unittest.TestCase):
    def test_preexisting_core_python_files_unchanged(self):
        root = Path(__file__).resolve().parents[1]; manifest = json.loads((root / "docs/chapter3_bser/phase1a/core_freeze_before.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["existing_core_python_count"], 40)
        for record in manifest["files"]:
            data = (root / record["path"]).read_bytes(); self.assertEqual(hashlib.sha256(data).hexdigest(), record["sha256"], record["path"])
            dump = ast.dump(ast.parse(data.decode("utf-8")), annotate_fields=True, include_attributes=True); self.assertEqual(hashlib.sha256(dump.encode()).hexdigest(), record["ast_dump_sha256"], record["path"])


if __name__ == "__main__": unittest.main()
