import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryMetadataTests(unittest.TestCase):
    def test_metadata_matches_completed_phase0b2(self):
        attributes = ROOT / ".gitattributes"
        ignore = ROOT / ".gitignore"
        self.assertTrue(attributes.is_file())
        self.assertTrue(ignore.is_file())

        attributes_text = attributes.read_text(encoding="utf-8")
        for rule in (
            "core/**/*.py text eol=lf",
            "chapter3_bser/**/*.py text eol=lf",
            "chapter4_rcag/**/*.py text eol=lf",
            "chapter5_vsgc/**/*.py text eol=lf",
            "tests/**/*.py text eol=lf",
            "tools/**/*.py text eol=lf",
            "docs/provenance/*.json text eol=lf",
        ):
            self.assertIn(rule, attributes_text)

        root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        core_readme = (ROOT / "core/README.md").read_text(encoding="utf-8")
        chapter3_readme = (ROOT / "chapter3_bser/README.md").read_text(encoding="utf-8")
        self.assertNotIn("Phase 0A empty production skeleton", root_readme)
        self.assertNotIn("Phase 0A permits structure", agents)
        self.assertNotIn("Future shared", core_readme)
        self.assertNotIn("placeholder only", core_readme)
        if "# BSER Phase 1A" in chapter3_readme:
            self.assertIn("offline, high-level finite allocation model", chapter3_readme)
            self.assertIn("BSER is not implemented as an online controller", chapter3_readme)
        else:
            self.assertIn("BSER is not implemented", chapter3_readme)
            self.assertIn("next phase is Phase 1A", chapter3_readme)

        source_text = (ROOT / "SOURCE_MANIFEST.json").read_text(encoding="utf-8")
        source_manifest = json.loads(source_text)
        self.assertNotEqual(source_manifest["phase"], "0A")
        self.assertIs(source_manifest["formal_code_migrated"], True)
        self.assertIs(source_manifest["core_self_contained"], True)
        self.assertIs(source_manifest["runtime_legacy_dependency"], False)
        self.assertNotIn(r"E:\gym\code\WORKSPACE".lower(), source_text.lower())

    def test_formal_evidence_is_not_ignored(self):
        for relative in (
            "docs/phase0b2/delivery_validation.json",
            "docs/provenance/ch3_to_core_migration_manifest.json",
            "experiments/chapter3/e0_core_migration/core_without_legacy_summary.json",
            "configs/scenarios/e0_equivalence/M20_MOVING_UNKNOWN_MULTI.json",
        ):
            completed = subprocess.run(
                ["git", "check-ignore", "--quiet", relative],
                cwd=ROOT,
                check=False,
            )
            self.assertEqual(completed.returncode, 1, relative)

        checkpoint = subprocess.run(
            ["git", "check-ignore", "--quiet", "--no-index", "phase0b2_1_probe.pt"],
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(checkpoint.returncode, 0)

    def test_all_27_provenance_hashes_still_match(self):
        manifest = json.loads(
            (ROOT / "docs/provenance/ch3_to_core_migration_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(manifest["authority_record_count"], 27)
        self.assertEqual(len(manifest["records"]), 27)
        for record in manifest["records"]:
            self.assertIs(record["semantic_changes"], False)
            target = ROOT / record["new_core_path"]
            self.assertTrue(target.is_file(), record["new_core_path"])
            self.assertEqual(
                hashlib.sha256(target.read_bytes()).hexdigest(),
                record["new_core_sha256"],
                record["new_core_path"],
            )


if __name__ == "__main__":
    unittest.main()
