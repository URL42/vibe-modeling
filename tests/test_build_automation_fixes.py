import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import rebuild_stale_designs  # noqa: E402
import scad_build_all  # noqa: E402
import scad_new_revision  # noqa: E402


@contextlib.contextmanager
def working_directory(path: Path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def tree(root: Path) -> set:
    return {p.relative_to(root).as_posix() for p in root.rglob("*")}


class NewRevisionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name).resolve()
        (self.root / "designs" / "demo" / "src").mkdir(parents=True)
        (self.root / "designs" / "demo" / "src" / "main.scad").write_text("cube(1);", encoding="utf-8")
        self.configs = self.root / "designs" / "demo" / "configs"
        self.configs.mkdir()
        (self.configs / "rev_0001.json").write_text('{"part": "demo", "w": 1}\n', encoding="utf-8")
        # Hand-formatted on purpose: params.json must stay byte-identical.
        (self.configs / "rev_0002.json").write_text('{"part":"demo","w":2}', encoding="utf-8")
        published = self.root / "revisions" / "demo" / "rev_0001"
        published.mkdir(parents=True)
        (published / "params.json").write_bytes((self.configs / "rev_0001.json").read_bytes())

    def tearDown(self):
        self.temporary.cleanup()

    def run_revision(self, base: str, *extra: str, build_ok: bool = True):
        def fake_build(command, check):
            out_dir = Path(command[command.index("--out-dir") + 1])
            (out_dir / "demo.stl").write_text("solid demo\nendsolid demo\n", encoding="utf-8")
            if not build_ok:
                raise subprocess.CalledProcessError(1, command)

        argv = ["scad_new_revision.py", "--design", "demo", "--base-config", base, *extra]
        with working_directory(self.root), \
             mock.patch.object(sys, "argv", argv), \
             mock.patch.object(scad_new_revision.subprocess, "run", side_effect=fake_build), \
             contextlib.redirect_stdout(io.StringIO()):
            return scad_new_revision.main()

    def test_staged_candidate_publishes_under_its_own_number(self):
        self.run_revision("designs/demo/configs/rev_0002.json")
        rev = self.root / "revisions" / "demo" / "rev_0002"
        self.assertTrue((rev / "demo.stl").is_file())
        self.assertEqual((rev / "params.json").read_bytes(), (self.configs / "rev_0002.json").read_bytes())
        self.assertFalse((self.configs / "rev_0003.json").exists())

    def test_published_base_is_copied_to_next_unused_number(self):
        self.run_revision("designs/demo/configs/rev_0001.json")
        self.assertEqual(json.loads((self.configs / "rev_0003.json").read_text()), {"part": "demo", "w": 1})
        self.assertTrue((self.root / "revisions" / "demo" / "rev_0003" / "params.json").is_file())

    def test_older_unpublished_config_copies_forward_instead_of_publishing_out_of_order(self):
        (self.configs / "rev_0003.json").write_text('{"part":"demo","w":3}', encoding="utf-8")
        self.run_revision("designs/demo/configs/rev_0002.json")
        self.assertFalse((self.root / "revisions" / "demo" / "rev_0002").exists())
        self.assertEqual(json.loads((self.configs / "rev_0004.json").read_text()), {"part": "demo", "w": 2})
        self.assertTrue((self.root / "revisions" / "demo" / "rev_0004" / "params.json").is_file())

    def test_unpadded_config_name_is_not_published_in_place(self):
        (self.configs / "rev_0002.json").rename(self.configs / "rev_2.json")
        self.run_revision("designs/demo/configs/rev_2.json")
        self.assertFalse((self.root / "revisions" / "demo" / "rev_0002").exists())
        self.assertTrue((self.root / "revisions" / "demo" / "rev_0003").is_dir())

    def test_failed_build_leaves_no_config_or_revision(self):
        before = tree(self.root)
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_revision("designs/demo/configs/rev_0001.json", build_ok=False)
        self.assertEqual(tree(self.root), before)

    def test_failed_candidate_publication_keeps_candidate_config(self):
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_revision("designs/demo/configs/rev_0002.json", build_ok=False)
        self.assertTrue((self.configs / "rev_0002.json").is_file())
        self.assertFalse((self.root / "revisions" / "demo" / "rev_0002").exists())

    def test_dry_run_writes_nothing(self):
        before = tree(self.root)
        self.run_revision("designs/demo/configs/rev_0001.json", "--dry-run")
        self.run_revision("designs/demo/configs/rev_0002.json", "--dry-run")
        self.assertEqual(tree(self.root), before)


class AssetProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name).resolve()
        design = self.root / "designs" / "demo"
        (design / "src").mkdir(parents=True)
        (design / "src" / "main.scad").write_text('import("../assets/a.stl");', encoding="utf-8")
        (design / "configs").mkdir()
        self.config = design / "configs" / "rev_0001.json"
        self.config.write_text("{}", encoding="utf-8")
        self.parts = design / "parts.json"
        self.parts.write_text('{"schema_version": 1, "parts": [{"part_id": 1, "name": "a"}]}', encoding="utf-8")
        self.assets = design / "assets"
        self.assets.mkdir()
        (self.assets / "a.stl").write_text("solid a\nendsolid a\n", encoding="utf-8")
        self.source = design / "src"
        self.patch = mock.patch.object(scad_build_all, "REPO_ROOT", self.root)
        self.patch.start()
        self.write_manifest(scad_build_all.assets_provenance(self.assets))

    def tearDown(self):
        self.patch.stop()
        self.temporary.cleanup()

    def write_manifest(self, assets):
        output = self.root / "output" / "demo"
        output.mkdir(parents=True, exist_ok=True)
        (output / "a_rev_0001.stl").write_text("solid a\nendsolid a\n", encoding="utf-8")
        manifest = scad_build_all.create_build_manifest(
            "demo", "rev_0001", "current",
            self.config, scad_build_all.sha256_file(self.config),
            self.parts, scad_build_all.sha256_file(self.parts),
            self.source, scad_build_all.sha256_tree(self.source, (".scad",)),
            self.source / "main.scad", "openscad", scad_build_all.load_parts(self.parts),
            scad_build_all.artifact_records(output, {"a_rev_0001.stl"}),
            assets,
        )
        (output / scad_build_all.BUILD_MANIFEST_NAME).write_text(json.dumps(manifest), encoding="utf-8")

    def audit(self):
        with contextlib.redirect_stdout(io.StringIO()):
            scad_build_all.audit("demo", "rev_0001", "current", self.config, self.parts,
                                 self.source, assets_root=self.assets)

    def test_unchanged_assets_pass(self):
        self.audit()

    def test_changed_asset_fails_audit(self):
        (self.assets / "a.stl").write_text("solid changed\nendsolid changed\n", encoding="utf-8")
        with self.assertRaisesRegex(SystemExit, "assets have changed"):
            self.audit()

    def test_manifest_without_asset_record_fails_audit(self):
        self.write_manifest(None)
        with self.assertRaisesRegex(SystemExit, "never recorded"):
            self.audit()

    def test_removed_assets_fail_audit(self):
        for path in self.assets.iterdir():
            path.unlink()
        with self.assertRaisesRegex(SystemExit, "no longer exist"):
            self.audit()

    def test_hidden_files_do_not_change_asset_hash(self):
        (self.assets / ".DS_Store").write_bytes(b"\0finder")
        self.audit()

    def test_review_rejects_printable_build_with_stale_assets(self):
        manifest = json.loads((self.root / "output" / "demo" / scad_build_all.BUILD_MANIFEST_NAME).read_text())
        scad_build_all.check_assets(manifest, self.assets)
        (self.assets / "a.stl").write_text("solid changed\nendsolid changed\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            scad_build_all.check_assets(manifest, self.assets)

    def test_designs_without_assets_record_nothing(self):
        self.assertIsNone(scad_build_all.assets_provenance(self.root / "missing"))


class LineEndingNormalizationTests(unittest.TestCase):
    def test_text_hash_ignores_crlf_but_binary_is_exact(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            lf, crlf = root / "lf.stl", root / "crlf.stl"
            lf.write_bytes(b"solid a\nendsolid a\n")
            crlf.write_bytes(b"solid a\r\nendsolid a\r\n")
            self.assertEqual(scad_build_all.file_fingerprint(lf), scad_build_all.file_fingerprint(crlf))
            binary_lf, binary_crlf = root / "lf.png", root / "crlf.png"
            binary_lf.write_bytes(b"\x89PNG\0\n")
            binary_crlf.write_bytes(b"\x89PNG\0\r\n")
            self.assertNotEqual(scad_build_all.sha256_file(binary_lf), scad_build_all.sha256_file(binary_crlf))


class StaleDetectionTests(unittest.TestCase):
    def test_audit_result_decides_staleness(self):
        config = rebuild_stale_designs.ROOT / "designs" / "demo" / "configs" / "rev_0001.json"
        for returncode, expected in ((0, True), (1, False)):
            with self.subTest(returncode=returncode), \
                 mock.patch.object(rebuild_stale_designs.subprocess, "run",
                                   return_value=subprocess.CompletedProcess([], returncode, "", "hash mismatch")) as run, \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertIs(rebuild_stale_designs.is_current("demo", config), expected)
                self.assertIn("--audit-only", run.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
