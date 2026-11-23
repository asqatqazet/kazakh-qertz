#!/usr/bin/env python3
"""Exercise the real installers and release ZIPs in isolated directories on macOS.

Every install/uninstall supplies --dest-dir; HOME and the user's input sources
are never modified. No network access or third-party Python packages required.
"""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
VARIANTS = ("qwertz", "qwerty")


@unittest.skipUnless(sys.platform == "darwin", "Installers require macOS plutil and xmllint")
class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="kazakh-installer-test-")
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.source = self.work / "source with spaces"
        self.source.mkdir()
        for directory in ("Contents", "variants", "scripts"):
            shutil.copytree(ROOT / directory, self.source / directory)
        for filename in ("install.sh", "uninstall.sh", "README.md", "README.kk.md", "README.zh.md", "RELEASE_NOTES.md", "LICENSE"):
            shutil.copy2(ROOT / filename, self.source / filename)
        self.dest = self.work / "isolated Keyboard Layouts"

    def command(self, arguments, *, success=True, env=None):
        result = subprocess.run(
            [str(arg) for arg in arguments], cwd=self.work, env=env,
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def install(self, *args, source=None, success=True, env=None):
        return self.command(
            ["/bin/sh", (source or self.source) / "install.sh", *args, "--dest-dir", self.dest],
            success=success, env=env,
        )

    def uninstall(self, *args, source=None, success=True):
        return self.command(
            ["/bin/sh", (source or self.source) / "uninstall.sh", *args, "--dest-dir", self.dest],
            success=success,
        )

    def bundle(self, variant):
        return self.dest / f"Kazakh-{variant.upper()}.bundle"

    def assert_bundle(self, variant):
        contents = self.bundle(variant) / "Contents"
        self.assertTrue((contents / "Info.plist").is_file())
        self.assertTrue((contents / "Resources" / f"Kazakh-{variant.upper()}.keylayout").is_file())
        self.assertFalse((contents / "Contents").exists(), "Installer nested Contents twice")
        self.assertFalse(list(self.dest.glob(".kazakh-install.*")), "Temporary installation files left behind")

    def test_default_is_qwertz_and_both_can_coexist(self):
        self.install()
        self.assert_bundle("qwertz")
        self.assertFalse(self.bundle("qwerty").exists())
        self.install("both")
        for variant in VARIANTS:
            self.assert_bundle(variant)

    def test_replacing_one_preserves_the_other(self):
        self.install("both")
        for changed, other in (("qwertz", "qwerty"), ("qwerty", "qwertz")):
            with self.subTest(changed=changed):
                sentinel = self.bundle(other) / "keep-me.txt"
                sentinel.write_text("other layout is untouched")
                obsolete = self.bundle(changed) / "obsolete.txt"
                obsolete.write_text("remove during replacement")
                self.install(changed)
                self.assertEqual(sentinel.read_text(), "other layout is untouched")
                self.assertFalse(obsolete.exists())
                self.assert_bundle(changed)

    def test_uninstall_only_removes_requested_variant(self):
        self.install("both")
        self.uninstall()
        self.assertFalse(self.bundle("qwertz").exists())
        self.assert_bundle("qwerty")
        self.uninstall("qwerty")
        self.assertFalse(self.bundle("qwerty").exists())
        self.uninstall("both")  # Repeated removal is harmless.

    def test_missing_source_leaves_both_installed_bundles_untouched(self):
        self.install("both")
        for variant in VARIANTS:
            (self.bundle(variant) / "sentinel").write_text(variant)
        (self.source / "variants/qwerty/Contents/Resources/Kazakh-QWERTY.keylayout").unlink()
        self.install("both", success=False)
        for variant in VARIANTS:
            self.assertEqual((self.bundle(variant) / "sentinel").read_text(), variant)

    def test_malformed_xml_and_metadata_do_not_replace_existing_bundle(self):
        self.install()
        sentinel = self.bundle("qwertz") / "sentinel"
        sentinel.write_text("preserve")
        layout = self.source / "Contents/Resources/Kazakh-QWERTZ.keylayout"
        original = layout.read_bytes()
        layout.write_text('<keyboard name="Kazakh-QWERTZ"><broken>')
        self.install(success=False)
        self.assertEqual(sentinel.read_text(), "preserve")
        layout.write_bytes(original)
        (self.source / "Contents/Info.plist").write_text("not a property list")
        self.install(success=False)
        self.assertEqual(sentinel.read_text(), "preserve")

    def test_invalid_choices_and_unsafe_paths_are_rejected(self):
        self.install("both")
        for choice in ("../qwerty", "../../", "QWERTY", "unknown", "--unknown"):
            with self.subTest(choice=choice):
                self.install(choice, success=False)
                self.uninstall(choice, success=False)
        self.install("qwertz", "qwerty", success=False)
        self.command(["/bin/sh", self.source / "install.sh", "--dest-dir"], success=False)
        for variant in VARIANTS:
            self.assert_bundle(variant)

    def test_symlink_target_is_not_followed_or_replaced(self):
        outside = self.work / "unrelated directory"
        outside.mkdir()
        sentinel = outside / "keep"
        sentinel.write_text("untouched")
        self.dest.mkdir()
        self.bundle("qwertz").symlink_to(outside, target_is_directory=True)
        self.install(success=False)
        self.uninstall(success=False)
        self.assertTrue(self.bundle("qwertz").is_symlink())
        self.assertEqual(sentinel.read_text(), "untouched")

    def test_failed_replacement_restores_previous_bundle(self):
        self.install()
        sentinel = self.bundle("qwertz") / "sentinel"
        sentinel.write_text("old version")
        tools_dir = self.work / "failure injection"
        tools_dir.mkdir()
        mv = tools_dir / "mv"
        mv.write_text('#!/bin/sh\ncase "$1" in */.kazakh-install.*/Kazakh-QWERTZ.bundle) exit 1 ;; esac\nexec /bin/mv "$@"\n')
        mv.chmod(0o755)
        environment = os.environ.copy()
        environment["PATH"] = str(tools_dir) + os.pathsep + environment["PATH"]
        self.install(success=False, env=environment)
        self.assertEqual(sentinel.read_text(), "old version")
        self.assert_bundle("qwertz")

    def test_both_release_zips_install_their_own_variant_by_default(self):
        for variant in VARIANTS:
            with self.subTest(variant=variant):
                self.command([self.source / "scripts/build-zip.sh", "1.2.0", variant])
                archive = self.source / "dist" / f"Kazakh-{variant.upper()}-v1.2.0.zip"
                package = self.work / f"extracted {variant}"
                with zipfile.ZipFile(archive) as zip_file:
                    self.assertIsNone(zip_file.testzip())
                    zip_file.extractall(package)
                for filename in ("README.md", "README.kk.md", "README.zh.md", "RELEASE_NOTES.md", "LICENSE", "Install.command"):
                    self.assertTrue((package / filename).is_file(), filename)
                # Python zipfile does not restore Unix executable bits.
                (package / "install.sh").chmod(0o755)
                self.install(source=package)
                self.assert_bundle(variant)
                self.command(["/bin/sh", package / "Install.command", "--dest-dir", self.dest])
                self.assert_bundle(variant)
                self.uninstall(source=package)
                self.assertFalse(self.bundle(variant).exists())

    def test_invalid_package_version_and_variant_are_rejected(self):
        for arguments in (("../../outside", "qwertz"), ("v1.2.0", "both"), ("v1.2.0", "../../other")):
            self.command([self.source / "scripts/build-zip.sh", *arguments], success=False)
        self.assertFalse((self.source / "dist").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
