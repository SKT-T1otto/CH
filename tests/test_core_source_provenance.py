import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CoreSourceProvenanceTests(unittest.TestCase):
    def test_all_27_authority_records_map_to_current_core_files(self):
        path = ROOT / "docs/provenance/ch3_to_core_migration_manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["authority_record_count"], 27)
        self.assertFalse(manifest["semantic_changes"])
        self.assertEqual(len(manifest["records"]), 27)
        for record in manifest["records"]:
            self.assertFalse(record["semantic_changes"])
            target = ROOT / record["new_core_path"]
            self.assertTrue(target.is_file(), record["new_core_path"])
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), record["new_core_sha256"])


if __name__ == "__main__":
    unittest.main()
