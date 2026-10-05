"""Fictional, local contract exercises; no accounts, network, or social effects.

Run from the source checkout with:
    python3 -B -m unittest discover -s tests -v
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
import uuid


PRODUCT_ROOT = Path(__file__).resolve().parent.parent
VERSION = "0.1.0-dev.1"


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def snapshot(root: Path) -> dict[str, bytes]:
    return {path.relative_to(root).as_posix(): path.read_bytes()
            for path in root.rglob("*") if path.is_file() and not path.is_symlink()}


class ReferenceToolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="social-kernel-fictional-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "fictional-source"
        self.root.mkdir()
        (self.root / "scripts").mkdir()
        for path in (PRODUCT_ROOT / "scripts").glob("*.py"):
            shutil.copyfile(path, self.root / "scripts" / path.name)
        (self.root / "docs").mkdir()
        self.text("docs/GUIDE.md", "# Fictional guide\n\nNo real user or platform is represented.\n")
        self.text("BOOT.md", "# Fixture entry\n\n[Method](KERNEL.md), [field](COMPETENCES.md), [learning](EVOLUTION.md).\n")
        self.text("KERNEL.md", "# Fictional method\n\n[Guide](docs/GUIDE.md).\n")
        self.text("EVOLUTION.md", "# Fictional learning\n")
        self.text("CURRENT.md", "# Product fixture state\n\nNo private instance facts.\n")
        self.text("COMPETENCES.md", "# Fixture field\n\n[Read](skills/fixture-reading/SKILL.md) and [return](skills/fixture-return/SKILL.md).\n")
        self.text("skills/fixture-reading/SKILL.md", "---\nname: fixture-reading\ndescription: Use for this fictional reading exercise.\n---\n\n# Read\n\n[Return](../fixture-return/SKILL.md). [Guide](../../docs/GUIDE.md).\n")
        self.text("skills/fixture-return/SKILL.md", "---\nname: fixture-return\ndescription: >-\n  Use for this fictional return exercise,\n  with no external effects.\n---\n\n# Return\n\n[Read](../fixture-reading/SKILL.md).\n")
        self.manifest = {
            "schema_version": "social-kernel.manifest.v1",
            "source_version": VERSION,
            "entries": {"boot": "BOOT.md", "kernel": "KERNEL.md", "competence_field": "COMPETENCES.md", "evolution": "EVOLUTION.md", "current": "CURRENT.md"},
            "competences": [
                {"name": "fixture-reading", "path": "skills/fixture-reading/SKILL.md"},
                {"name": "fixture-return", "path": "skills/fixture-return/SKILL.md"},
            ],
            "state_contract": {"storage": "Chosen by the fictional receiver; no universal shape."},
            "source_bundle": {"name": "social-kernel", "include": ["BOOT.md", "KERNEL.md", "EVOLUTION.md", "COMPETENCES.md", "CURRENT.md", "KERNEL_MANIFEST.json", "docs/", "skills/", "scripts/"]},
        }
        self.save_manifest()

    def text(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def save_manifest(self) -> None:
        write_json(self.root / "KERNEL_MANIFEST.json", self.manifest)

    def run_tool(self, tool: str, *arguments: object, root: Path | None = None) -> subprocess.CompletedProcess:
        source = root or self.root
        return subprocess.run([sys.executable, "-B", str(source / "scripts" / tool), *map(str, arguments)],
                              cwd=self.base, text=True, capture_output=True, timeout=15, check=False)

    def validate(self, root: Path | None = None, instance: Path | None = None) -> tuple[subprocess.CompletedProcess, dict]:
        source = root or self.root
        arguments = ["--root", source, "--json"]
        if instance is not None:
            arguments.extend(["--instance", instance])
        process = self.run_tool("validate.py", *arguments, root=source)
        self.assertIn(process.returncode, (0, 1), process.stderr)
        try:
            result = json.loads(process.stdout)
        except json.JSONDecodeError:
            self.fail("Validator did not return a JSON report: " + process.stderr)
        self.assertEqual(process.returncode == 0, result["ok"])
        return process, result

    def build(self, name: str = "assembled-source") -> Path:
        destination = self.base / name
        result = self.run_tool("build_plugin.py", "--destination", destination)
        self.assertEqual(result.returncode, 0, result.stderr)
        return destination

    def initialize(self, name: str = "private-fictional-field") -> Path:
        destination = self.base / name
        result = self.run_tool("init_instance.py", "--destination", destination, "--name", "Fictional local exercise")
        self.assertEqual(result.returncode, 0, result.stderr)
        return destination

    def error_codes(self, result: dict) -> set[str]:
        return {error["code"] for error in result["errors"]}

    def symlink(self, link: Path, target: Path, *, directory: bool = False) -> None:
        try:
            link.symlink_to(target, target_is_directory=directory)
        except OSError as exc:
            if os.name == "nt" and getattr(exc, "winerror", None) == 1314:
                self.skipTest("This Windows process lacks the symbolic-link creation privilege; symlink behavior is unverified here.")
            raise

    def test_valid_source_is_read_only(self) -> None:
        before = snapshot(self.root)
        process, report = self.validate()
        self.assertEqual(process.returncode, 0, report)
        self.assertEqual(report["counts"]["declared_competences"], 2)
        self.assertEqual(snapshot(self.root), before)
        self.assertFalse(list(self.root.rglob("__pycache__")))

    def test_manifest_routes_can_use_a_valid_different_layout(self) -> None:
        # The manifest owns its routes; a particular root filename is not a
        # universal state or method schema imposed by the validator.
        (self.root / "BOOT.md").unlink()
        self.text("docs/ENTRY.md", "# Alternate fictional entry\n\n[Method](../KERNEL.md).\n")
        self.manifest["entries"]["boot"] = "docs/ENTRY.md"
        self.manifest["source_bundle"]["include"].remove("BOOT.md")
        self.manifest["state_contract"] = {"receiver_record_kind": ["conversation", "selected documents"]}
        self.save_manifest()
        self.assertTrue(self.validate()[1]["ok"])

    def test_broken_declared_route_is_detected_without_rewrite(self) -> None:
        self.manifest["entries"]["boot"] = "docs/ABSENT.md"
        self.save_manifest()
        before = snapshot(self.root)
        report = self.validate()[1]
        self.assertIn("missing_route", self.error_codes(report))
        self.assertEqual(snapshot(self.root), before)

    def test_broken_sibling_link_is_detected(self) -> None:
        path = self.root / "skills/fixture-reading/SKILL.md"
        path.write_text(path.read_text().replace("../fixture-return/SKILL.md", "../absent-competence/SKILL.md"))
        self.assertIn("missing_link", self.error_codes(self.validate()[1]))

    def test_code_examples_are_not_active_routes_and_valid_markdown_variants_work(self) -> None:
        self.text("docs/Brief (final).md", "# Fictional brief\n")
        with (self.root / "KERNEL.md").open("a") as stream:
            stream.write("\n[Brief](<docs/Brief (final).md>)\n[Reference][guide]\n[guide]: docs/GUIDE.md \"Guide\"\n\n")
            stream.write("`[inline example](not-an-active-file.md)`\n\n```md\n[example](not-an-active-file.md)\n```\n\n~~~text\n[example](not-an-active-file.md)\n~~~\n\n    [indented example](not-an-active-file.md)\n\n<!-- [comment](not-an-active-file.md) -->\n")
            stream.write("\n[External source](https://example.invalid/fictional) and [anchor](#unverified-anchor).\n")
        self.assertTrue(self.validate()[1]["ok"])

    def test_existing_unbundled_file_is_not_a_closed_reference(self) -> None:
        self.text("outside-allowlist.md", "# Fictional extra\n")
        self.text("KERNEL.md", "# Fictional method\n\n[Extra](outside-allowlist.md).\n")
        self.assertIn("unpackaged_link", self.error_codes(self.validate()[1]))

    def test_frontmatter_names_and_required_descriptions_are_checked(self) -> None:
        path = self.root / "skills/fixture-return/SKILL.md"
        path.write_text("---\nname: wrong-fictional-name\n---\n\n# Fictional return\n")
        codes = self.error_codes(self.validate()[1])
        self.assertIn("competence_name", codes)
        self.assertIn("skill_frontmatter", codes)

    def test_missing_required_include_and_unknown_source_version_are_refused(self) -> None:
        (self.root / "EVOLUTION.md").unlink()
        self.manifest["source_version"] = "999.0.0-fictional"
        self.save_manifest()
        codes = self.error_codes(self.validate()[1])
        self.assertIn("missing_include", codes)
        self.assertIn("source_version", codes)
        destination = self.base / "must-not-be-created"
        self.assertEqual(self.run_tool("build_plugin.py", "--destination", destination).returncode, 1)
        self.assertFalse(destination.exists())

    def test_malformed_manifest_reports_a_refusal(self) -> None:
        for malformed in (b"{", b"[]", b'{"schema_version":"one","schema_version":"two"}'):
            with self.subTest(malformed=malformed):
                (self.root / "KERNEL_MANIFEST.json").write_bytes(malformed)
                before = snapshot(self.root)
                self.assertFalse(self.validate()[1]["ok"])
                self.assertEqual(snapshot(self.root), before)

    def test_malformed_bundle_manifest_still_returns_a_structured_refusal(self) -> None:
        bundle = self.build()
        write_json(bundle / "KERNEL_MANIFEST.json", {"source_bundle": []})
        before = snapshot(bundle)
        self.assertFalse(self.validate(root=bundle)[1]["ok"])
        self.assertEqual(snapshot(bundle), before)

    def test_bundle_is_reproducible_and_validates_without_its_origin(self) -> None:
        source = snapshot(self.root)
        first = self.build("first-bundle")
        second = self.build("second-bundle")
        self.assertEqual(snapshot(first), snapshot(second))
        inventory = json.loads((first / "BUNDLE_INVENTORY.json").read_text())
        for entry in inventory["source_files"]:
            expected = source[entry["path"]]
            self.assertEqual((first / entry["path"]).read_bytes(), expected)
            self.assertEqual(entry["sha256"], hashlib.sha256(expected).hexdigest())
            self.assertEqual(entry["size"], len(expected))
        self.assertEqual({entry["path"] for entry in inventory["source_files"]}, set(source))
        self.assertEqual({entry["path"] for entry in inventory["files"]}, set(snapshot(first)) - {"BUNDLE_INVENTORY.json"})
        self.assertEqual((first / "plugin.json").read_bytes(), (first / ".codex-plugin/plugin.json").read_bytes())
        plugin = json.loads((first / "plugin.json").read_text())
        self.assertEqual((plugin["name"], plugin["version"]), ("social-kernel", VERSION))
        self.root.rename(self.base / "origin-no-longer-at-its-path")
        before = snapshot(first)
        report = self.validate(root=first)[1]
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["kind"], "source_bundle")
        self.assertEqual(snapshot(first), before)
        self.assertNotIn(str(self.root).encode(), b"\n".join(snapshot(first).values()))

    def test_tampered_inventory_is_detected(self) -> None:
        bundle = self.build()
        path = bundle / "BUNDLE_INVENTORY.json"
        value = json.loads(path.read_text())
        value["files"][0]["sha256"] = "0" * 64
        write_json(path, value)
        before = snapshot(bundle)
        self.assertIn("bundle_metadata", self.error_codes(self.validate(root=bundle)[1]))
        self.assertEqual(snapshot(bundle), before)

    def test_changed_bundle_bytes_and_unlisted_files_are_detected(self) -> None:
        bundle = self.build()
        (bundle / "KERNEL.md").write_text("# Changed fictional method\n")
        (bundle / "unlisted.txt").write_text("Fictional unexpected file.\n")
        codes = self.error_codes(self.validate(root=bundle)[1])
        self.assertIn("bundle_metadata", codes)
        self.assertIn("unlisted_bundle_file", codes)

    def test_bundle_excludes_known_non_source_paths(self) -> None:
        contaminants = ["docs/internal/note.md", "docs/reports/note.md", "skills/fixture-reading/tests/data.txt", "skills/fixture-reading/credentials.json", "skills/fixture-reading/private-preview/old.md", "scripts/__pycache__/cache.pyc", "docs/instances/local/CURRENT.md"]
        for name in contaminants:
            self.text(name, "Fictional excluded file; no real private data.\n")
        # Historical paths outside the allowlist are not a second source owner.
        self.text("plugin-adapters/openai/private-preview/plugin.json", "{}\n")
        bundle = self.build()
        for name in contaminants:
            self.assertFalse((bundle / name).exists(), name)
        self.assertFalse((bundle / "plugin-adapters").exists())
        self.assertTrue(self.validate(root=bundle)[1]["ok"])

    def test_symlink_source_reference_is_refused(self) -> None:
        outside = self.base / "fictional-outside.txt"
        outside.write_text("A fictional outside source.\n")
        self.symlink(self.root / "docs/linked.md", outside)
        report = self.validate()[1]
        self.assertIn("symlink", self.error_codes(report))

    def test_route_through_a_symlink_ancestor_cannot_falsely_pass_closure(self) -> None:
        self.symlink(self.root / "alias", self.root / "docs", directory=True)
        self.text("KERNEL.md", "# Fictional method\n\n[Guide](alias/GUIDE.md).\n")
        report = self.validate()[1]
        self.assertIn("symlink_link", self.error_codes(report))
        self.manifest["source_bundle"]["include"].append("alias/GUIDE.md")
        self.save_manifest()
        self.assertIn("symlink", self.error_codes(self.validate()[1]))

    def test_both_writers_preserve_existing_files_and_directories(self) -> None:
        existing_file = self.base / "existing-file"
        existing_file.write_bytes(b"KEEP EXACT FICTIONAL BYTES\x00\xff")
        empty = self.base / "empty-directory"
        empty.mkdir()
        populated = self.base / "populated-directory"
        populated.mkdir()
        (populated / "keep.bin").write_bytes(b"DO NOT ALTER\x00")
        for tool in ("init_instance.py", "build_plugin.py"):
            for destination in (existing_file, empty, populated):
                with self.subTest(tool=tool, destination=destination.name):
                    result = self.run_tool(tool, "--destination", destination)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertEqual(existing_file.read_bytes(), b"KEEP EXACT FICTIONAL BYTES\x00\xff")
                    self.assertEqual(snapshot(populated), {"keep.bin": b"DO NOT ALTER\x00"})
                    self.assertEqual(list(empty.iterdir()), [])

    def test_both_writers_preserve_existing_and_broken_symlinks(self) -> None:
        existing_file = self.base / "existing-file"
        existing_file.write_bytes(b"KEEP EXACT FICTIONAL BYTES\x00\xff")
        link, broken = self.base / "existing-link", self.base / "broken-link"
        self.symlink(link, existing_file)
        self.symlink(broken, self.base / "missing-link-target")
        for tool in ("init_instance.py", "build_plugin.py"):
            for destination in (link, broken):
                with self.subTest(tool=tool, destination=destination.name):
                    result = self.run_tool(tool, "--destination", destination)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertEqual(existing_file.read_bytes(), b"KEEP EXACT FICTIONAL BYTES\x00\xff")
                    self.assertTrue(link.is_symlink())
                    self.assertTrue(broken.is_symlink())
                    self.assertFalse(broken.exists())

    def test_both_writers_reject_product_destinations(self) -> None:
        before = snapshot(self.root)
        for tool in ("init_instance.py", "build_plugin.py"):
            destination = self.root / "new-field"
            self.assertEqual(self.run_tool(tool, "--destination", destination).returncode, 1)
            self.assertFalse(destination.exists())
        self.assertEqual(snapshot(self.root), before)

    def test_both_writers_reject_product_destinations_through_parent_aliases(self) -> None:
        alias = self.base / "alias-to-product"
        self.symlink(alias, self.root, directory=True)
        before = snapshot(self.root)
        for tool in ("init_instance.py", "build_plugin.py"):
            for destination in (self.root / "new-field", alias / "new-field"):
                with self.subTest(tool=tool, destination=str(destination)):
                    self.assertEqual(self.run_tool(tool, "--destination", destination).returncode, 1)
                    self.assertFalse(destination.exists())
        self.assertEqual(snapshot(self.root), before)

    def test_receiver_plugin_preserves_identity_prompts_and_source_fingerprint(self) -> None:
        metadata = {"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
                    "name": "fictional-existing-plugin", "version": "0.3.0-dev.1",
                    "description": "Fictional receiver-owned identity.",
                    "extensions": {"com.openai": {"interface": {
                        "displayName": "Fictional receiver", "shortDescription": "Continuing public work",
                        "defaultPrompt": ["First unchanged prompt", "Second unchanged prompt"]}}}}
        path = self.base / "receiver-metadata.json"
        write_json(path, metadata)
        bundles = []
        for name in ("receiver-one", "receiver-two"):
            destination = self.base / name
            result = self.run_tool("build_plugin.py", "--destination", destination, "--plugin-manifest", path)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(self.validate(root=destination)[1]["ok"])
            bundles.append(destination)
        self.assertEqual(snapshot(bundles[0]), snapshot(bundles[1]))
        portable = json.loads((bundles[0] / "plugin.json").read_text())
        legacy = json.loads((bundles[0] / ".codex-plugin/plugin.json").read_text())
        self.assertEqual(portable, metadata)
        self.assertEqual(legacy["interface"], metadata["extensions"]["com.openai"]["interface"])
        self.assertEqual((legacy["name"], legacy["version"]), (metadata["name"], metadata["version"]))
        standard = self.build("standard-comparison")
        original = json.loads((standard / "BUNDLE_INVENTORY.json").read_text())
        custom = json.loads((bundles[0] / "BUNDLE_INVENTORY.json").read_text())
        self.assertEqual(custom["source_fingerprint"], original["source_fingerprint"])
        self.assertEqual(custom["source_version"], VERSION)
        # The delivered validator must keep working without the original source.
        self.root.rename(self.base / "origin-unavailable")
        self.assertTrue(self.validate(root=bundles[0])[1]["ok"])
        portable["version"] = "0.3.0-dev.2"
        write_json(bundles[0] / "plugin.json", portable)
        self.assertIn("bundle_metadata", self.error_codes(self.validate(root=bundles[0])[1]))

    def test_receiver_metadata_cannot_add_execution_or_leak_credential_values(self) -> None:
        base = {"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
                "name": "fictional-plugin", "version": "0.3.0", "description": "Fictional metadata."}
        cases = [dict(base, extensions={"com.openai": {"hooks": "undeclared.json"}}),
                 dict(base, access_token="FICTIONAL_TOKEN_NEVER_ECHO"),
                 dict(base, extensions={"com.openai": {"interface": {"shortDescription": "x" * 31}}}),
                 dict(base, name="../escape"), None]
        for i, metadata in enumerate(cases):
            with self.subTest(case=i):
                path = self.base / "receiver-metadata.json"
                write_json(path, metadata)
                destination = self.base / f"refused-receiver-{i}"
                result = self.run_tool("build_plugin.py", "--destination", destination, "--plugin-manifest", path)
                self.assertEqual(result.returncode, 1)
                self.assertFalse(destination.exists())
                self.assertNotIn("FICTIONAL_TOKEN_NEVER_ECHO", result.stdout + result.stderr)

    def test_both_writers_require_absolute_paths_and_existing_parents(self) -> None:
        for tool in ("init_instance.py", "build_plugin.py"):
            for destination in ("relative-destination", self.base / "absent-parent" / "new-field"):
                with self.subTest(tool=tool, destination=str(destination)):
                    self.assertEqual(self.run_tool(tool, "--destination", destination).returncode, 1)
        self.assertFalse((self.base / "relative-destination").exists())
        self.assertFalse((self.base / "absent-parent").exists())

    def test_initializer_creates_only_unconfigured_private_state_and_qualified_provenance(self) -> None:
        instance = self.initialize()
        self.assertEqual(set(snapshot(instance)), {"instance.json", "CURRENT.md"})
        metadata = json.loads((instance / "instance.json").read_text())
        self.assertEqual(metadata["schema_version"], "social-kernel.instance.v1")
        self.assertEqual(str(uuid.UUID(metadata["instance_id"])), metadata["instance_id"])
        self.assertEqual(metadata["name"], "Fictional local exercise")
        self.assertEqual(metadata["source"]["version"], VERSION)
        self.assertEqual(metadata["state_entry"], "CURRENT.md")
        self.assertIn("local manifest-declared source bytes only", metadata["source"]["fingerprint"]["qualification"])
        self.assertIn("Status: unconfigured", (instance / "CURRENT.md").read_text())
        bundle = self.build()
        inventory = json.loads((bundle / "BUNDLE_INVENTORY.json").read_text())
        self.assertEqual(metadata["source"]["fingerprint"], inventory["source_fingerprint"])
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(instance.stat().st_mode) & 0o077, 0)
            self.assertEqual(stat.S_IMODE((instance / "instance.json").stat().st_mode) & 0o077, 0)
        # Subsequent real state belongs to its receiver, not to this template.
        (instance / "CURRENT.md").write_text("# Fictional receiver-native continuation\n\nA different record layout.\n")
        before = snapshot(instance)
        self.assertTrue(self.validate(instance=instance)[1]["ok"])
        self.assertEqual(snapshot(instance), before)

    def test_malformed_or_unknown_instance_schema_is_refused_read_only(self) -> None:
        instance = self.initialize()
        path = instance / "instance.json"
        for malformed in (b"{not-json", b"[]", b'{"schema_version":"fictional.future.v99"}'):
            with self.subTest(malformed=malformed):
                path.write_bytes(malformed)
                before = snapshot(instance)
                self.assertFalse(self.validate(instance=instance)[1]["ok"])
                self.assertEqual(snapshot(instance), before)

    def test_manual_state_without_helper_metadata_is_accepted_without_schema_claim(self) -> None:
        instance = self.base / "manual-fictional-state"
        instance.mkdir()
        (instance / "reader-selected-entry.txt").write_text("Fictional host-native continuity.\n")
        before = snapshot(instance)
        report = self.validate(instance=instance)[1]
        self.assertTrue(report["ok"])
        self.assertIn("manual_state", {warning["code"] for warning in report["warnings"]})
        self.assertEqual(snapshot(instance), before)

    def test_initializer_state_route_cannot_escape_its_instance(self) -> None:
        instance = self.initialize()
        path = instance / "instance.json"
        metadata = json.loads(path.read_text())
        metadata["state_entry"] = "../fictional-outside.md"
        write_json(path, metadata)
        before = snapshot(instance)
        self.assertIn("instance_state", self.error_codes(self.validate(instance=instance)[1]))
        self.assertEqual(snapshot(instance), before)

    def test_known_helper_metadata_credential_fields_are_refused_without_echoing_values(self) -> None:
        instance = self.initialize()
        path = instance / "instance.json"
        metadata = json.loads(path.read_text())
        fictional_value = "FICTIONAL-NON-CREDENTIAL-VALUE-ONLY"
        metadata["access_token"] = fictional_value
        write_json(path, metadata)
        before = snapshot(instance)
        process, report = self.validate(instance=instance)
        self.assertIn("credential_metadata", self.error_codes(report))
        self.assertNotIn(fictional_value, process.stdout + process.stderr)
        self.assertEqual(snapshot(instance), before)

    def test_historical_instance_source_is_not_silently_upgraded(self) -> None:
        instance = self.initialize()
        path = instance / "instance.json"
        metadata = json.loads(path.read_text())
        metadata["source"]["version"] = "0.0.0-fictional-earlier-source"
        write_json(path, metadata)
        before = snapshot(instance)
        report = self.validate(instance=instance)[1]
        self.assertTrue(report["ok"])
        self.assertEqual(snapshot(instance), before)
        self.assertIn("historical_provenance", {warning["code"] for warning in report["warnings"]})


if __name__ == "__main__":
    unittest.main()
