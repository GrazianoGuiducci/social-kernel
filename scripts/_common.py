"""Shared, standard-library mechanics for optional local source tools.

These checks concern declared files and metadata. They do not evaluate the
social method, authenticate a release, install a receiver, or classify private
content. Source paths are relative to this copy, including in assembled bundles.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
from typing import Any
from urllib.parse import unquote, urlsplit
import uuid


SOURCE_VERSION = "0.1.0-dev.1"
MANIFEST_SCHEMA = "social-kernel.manifest.v1"
INSTANCE_SCHEMA = "social-kernel.instance.v1"
INVENTORY_SCHEMA = "social-kernel.bundle-inventory.v1"
MANIFEST_FILE = "KERNEL_MANIFEST.json"
INVENTORY_FILE = "BUNDLE_INVENTORY.json"
PLUGIN_FILES = ("plugin.json", ".codex-plugin/plugin.json")
REQUIRED_ENTRIES = ("boot", "kernel", "competence_field", "evolution", "current")
DEFAULT_ROOT = Path(__file__).resolve().parent.parent

# These are packaging exclusions, not a private-content or secret classifier.
EXCLUDED_PARTS = frozenset({
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache", "node_modules",
    "private-preview", "tests", "fixtures", "reports", "internal",
    "instances", "credentials", "secrets",
})
EXCLUDED_NAMES = frozenset({
    "instance.json", "credentials.json", "token.json", "tokens.json",
    ".netrc", "id_rsa", "id_ed25519", ".ds_store",
})
CREDENTIAL_FIELDS = frozenset({
    "access_token", "refresh_token", "api_key", "password", "private_key",
    "client_secret", "secret_key", "credentials",
})
FINGERPRINT_SCOPE = (
    "SHA-256 of the sorted source_files inventory encoded as UTF-8 JSON with "
    "sorted object keys, separators ',' and ':', and no trailing newline. "
    "Each entry contains its relative path, byte size, and file SHA-256."
)
FINGERPRINT_QUALIFICATION = (
    "Identifies the local manifest-declared source bytes only. It is not a Git "
    "commit, signed release, authenticity proof, update guarantee, or evidence "
    "of installation, host compatibility, or social operation."
)
LIMITS = [
    "Checks declared source structure, local Markdown file routes, version "
    "identity, and bundle inventory when present.",
    "Packaging exclusions do not classify private content or prove privacy, "
    "semantic correctness, safety, native host compatibility, or operation.",
    "A content fingerprint is not signed source authenticity; external URLs "
    "and Markdown fragment anchors are not fetched or verified.",
]


class ToolError(Exception):
    """A bounded local refusal, safe to show without dumping file contents."""


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def issue(errors: list[dict], code: str, path: str, message: str) -> None:
    errors.append({"code": code, "path": path, "message": message})


def inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def local_path(value: Any) -> str:
    """Read a declared root-relative path, without glob or parent traversal."""
    if not isinstance(value, str) or not value or any(c in value for c in "\\?#") or any(ord(c) < 32 for c in value):
        raise ToolError("Expected a nonempty local path using forward slashes.")
    path = PurePosixPath(value)
    if path.is_absolute() or value.startswith("/") or ":" in value:
        raise ToolError("Absolute paths and URI schemes are not source routes.")
    if path == PurePosixPath(".") or ".." in path.parts or any(c in value for c in "*[]"):
        raise ToolError("Source routes cannot select the root, parent paths, or globs.")
    return path.as_posix()


def excluded(path: str) -> bool:
    parts = tuple(part.lower() for part in PurePosixPath(path).parts)
    name = parts[-1] if parts else ""
    return (
        any(part in EXCLUDED_PARTS for part in parts)
        or name in EXCLUDED_NAMES
        or name == ".env" or name.startswith(".env.")
        or PurePosixPath(name).suffix in {".pyc", ".pem", ".key", ".p12", ".pfx"}
    )


def _unique_object(pairs: list[tuple[str, Any]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON object key.")
        result[key] = value
    return result


def parse_json(data: bytes, path: str, errors: list[dict]) -> Any:
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=_unique_object)
    except (UnicodeError, ValueError):
        issue(errors, "invalid_json", path, "Expected unambiguous UTF-8 JSON.")
        return None


def read_regular(path: Path, label: str, errors: list[dict]) -> bytes | None:
    if path.is_symlink():
        issue(errors, "symlink", label, "Source and metadata files must not be symlinks.")
        return None
    try:
        if not path.is_file():
            issue(errors, "missing_file", label, "Required regular file is missing.")
            return None
        return path.read_bytes()
    except OSError:
        issue(errors, "unreadable_file", label, "Cannot read the required file.")
        return None


def tree_files(root: Path, start: Path, errors: list[dict], filter_exclusions: bool) -> list[Path]:
    found = []

    def walk_error(_error: OSError) -> None:
        issue(errors, "unreadable_directory", start.relative_to(root).as_posix(), "Cannot enumerate this directory.")

    for current, directories, files in os.walk(start, followlinks=False, onerror=walk_error):
        current_path = Path(current)
        keep = []
        for name in sorted(directories):
            child = current_path / name
            label = child.relative_to(root).as_posix()
            if filter_exclusions and excluded(label):
                continue
            if child.is_symlink():
                issue(errors, "symlink", label, "Source trees must not traverse symlink directories.")
            else:
                keep.append(name)
        directories[:] = keep
        for name in sorted(files):
            child = current_path / name
            label = child.relative_to(root).as_posix()
            if filter_exclusions and excluded(label):
                continue
            if child.is_symlink():
                issue(errors, "symlink", label, "Source trees must not include symlink files.")
            else:
                found.append(child)
    return found


def collect_source(root: Path, include: Any, errors: list[dict]) -> dict[str, bytes]:
    if not isinstance(include, list) or not include:
        issue(errors, "bundle_include", MANIFEST_FILE, "source_bundle.include must be a nonempty path list.")
        return {}
    selected = set()
    for value in include:
        try:
            label = local_path(value)
        except ToolError as exc:
            issue(errors, "invalid_route", MANIFEST_FILE, str(exc))
            continue
        if excluded(label) or label in (*PLUGIN_FILES, INVENTORY_FILE):
            issue(errors, "excluded_route", label, "This path cannot be a declared source-bundle input.")
            continue
        target = root / label
        try:
            resolved = target.resolve()
        except (OSError, RuntimeError):
            issue(errors, "unreachable_route", label, "Cannot resolve this source route.")
            continue
        if not inside(resolved, root):
            issue(errors, "outside_root", label, "Source route resolves outside this source root.")
        elif target.is_symlink() or resolved != target:
            issue(errors, "symlink", label, "Declared source routes must not depend on symlinks.")
        elif target.is_dir():
            selected.update(tree_files(root, target, errors, filter_exclusions=True))
        elif target.is_file():
            selected.add(target)
        else:
            issue(errors, "missing_include", label, "Declared source input is missing.")
    result = {}
    for path in sorted(selected):
        label = path.relative_to(root).as_posix()
        data = read_regular(path, label, errors)
        if data is not None:
            result[label] = data
    return result


def inventory(files: dict[str, bytes]) -> list[dict]:
    return [
        {"path": path, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}
        for path, data in sorted(files.items())
    ]


def fingerprint(source_files: list[dict]) -> dict:
    payload = json.dumps(source_files, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {
        "algorithm": "sha256",
        "digest": hashlib.sha256(payload).hexdigest(),
        "file_count": len(source_files),
        "scope": FINGERPRINT_SCOPE,
        "qualification": FINGERPRINT_QUALIFICATION,
    }


def bundle_name(manifest: dict) -> str:
    bundle = manifest.get("source_bundle")
    if isinstance(bundle, dict) and isinstance(bundle.get("name"), str):
        return bundle["name"]
    return "social-kernel"


def plugin_metadata(manifest: dict) -> dict:
    return {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": bundle_name(manifest),
        "version": manifest.get("source_version"),
        "description": "A source kernel for continuing public work through current-field reentry, native expression, relationships, consequences, and learning.",
        "repository": "https://github.com/GrazianoGuiducci/social-kernel",
    }


def receiver_plugin_metadata(value: Any) -> dict:
    """Accept identity/presentation only; no undeclared tools or integrations."""
    allowed = {"$schema", "name", "version", "description", "author", "homepage",
               "repository", "license", "keywords", "extensions"}
    if not isinstance(value, dict) or set(value) - allowed or embedded_credentials(value):
        raise ToolError("Receiver metadata must contain only credential-free plugin identity and presentation.")
    if value.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        raise ToolError("Receiver metadata must use the Agent Plugins 1.0 schema.")
    name, version = value.get("name"), value.get("version")
    if not isinstance(name, str) or len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ToolError("Receiver plugin name must be a lowercase hyphenated identifier of at most 64 characters.")
    if not isinstance(version, str) or not re.fullmatch(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?", version):
        raise ToolError("Receiver plugin version must be a semantic version.")
    if not isinstance(value.get("description"), str) or not value["description"].strip():
        raise ToolError("Receiver plugin metadata requires a description.")
    extensions = value.get("extensions", {})
    if not isinstance(extensions, dict) or set(extensions) - {"com.openai"}:
        raise ToolError("This skills-only builder supports only OpenAI presentation metadata.")
    openai = extensions.get("com.openai", {})
    if not isinstance(openai, dict) or set(openai) - {"interface"}:
        raise ToolError("Receiver metadata cannot introduce tools, hooks, apps or execution capabilities.")
    interface = openai.get("interface", {})
    if not isinstance(interface, dict):
        raise ToolError("Receiver plugin interface must be an object.")
    subtitle = interface.get("shortDescription")
    if subtitle is not None and (not isinstance(subtitle, str) or len(subtitle) > 30):
        raise ToolError("Receiver plugin shortDescription must be at most 30 characters.")
    return value


def assembled_files(manifest: dict, sources: dict[str, bytes], receiver_plugin: dict | None = None) -> dict[str, bytes]:
    files = dict(sources)
    plugin = plugin_metadata(manifest) if receiver_plugin is None else receiver_plugin_metadata(receiver_plugin)
    files["plugin.json"] = json_bytes(plugin)
    if receiver_plugin is None:
        files[".codex-plugin/plugin.json"] = files["plugin.json"]
    else:
        legacy = {key: value for key, value in plugin.items() if key not in {"$schema", "extensions"}}
        legacy.update(plugin.get("extensions", {}).get("com.openai", {}))
        legacy["skills"] = "./skills"
        files[".codex-plugin/plugin.json"] = json_bytes(legacy)
    source_files = inventory(sources)
    contents = {
        "schema_version": INVENTORY_SCHEMA,
        "source_name": bundle_name(manifest),
        "source_version": manifest.get("source_version"),
        "source_files": source_files,
        "source_fingerprint": fingerprint(source_files),
        "files": inventory(files),
        "inventory_excludes": [INVENTORY_FILE],
        "qualification": "Deterministic local source assembly only; no installation, release, execution, or authenticity claim.",
    }
    if receiver_plugin is not None:
        contents["receiver_plugin"] = receiver_plugin
    files[INVENTORY_FILE] = json_bytes(contents)
    return files


def markdown_prose(text: str) -> str:
    """Remove comments and code examples before reading active Markdown links."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    lines = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence is not None:
            if match and match.group(1)[0] == fence[0] and len(match.group(1)) >= fence[1] and not match.group(2).strip():
                fence = None
            continue
        if match:
            fence = (match.group(1)[0], len(match.group(1)))
            continue
        # Four-space/tab-indented blocks are code examples too.
        if line.startswith("    ") or line.startswith("\t"):
            continue
        lines.append(line)
    return re.sub(r"(`+)(.*?)\1", "", "\n".join(lines), flags=re.S)


def markdown_targets(text: str) -> list[str]:
    prose = markdown_prose(text)
    # Ordinary inline/image links, including angle-delimited paths with spaces
    # and a single nested parenthesis pair; plus reference-link definitions.
    inline = re.compile(r"\[[^\]\n]*\]\(\s*(<[^>\n]+>|(?:\\.|[^()\s]|\([^()\n]*\))+)(?:\s+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^\n)]*\)))?\s*\)")
    reference = re.compile(r"^ {0,3}\[[^\]\n]+\]:\s*(<[^>\n]+>|\S+)", re.M)
    return [match.group(1).strip("<>") for pattern in (inline, reference) for match in pattern.finditer(prose)]


def check_link(root: Path, origin: str, target: str, sources: dict[str, bytes], errors: list[dict]) -> None:
    target = re.sub(r"\\([\\()\[\] <>])", r"\1", target)
    try:
        uri = urlsplit(target)
    except ValueError:
        issue(errors, "invalid_link", origin, "Malformed Markdown link target.")
        return
    if uri.scheme in {"http", "https", "mailto", "tel", "data"} or target.startswith("//"):
        return  # No network request and no claim about the remote target.
    if uri.scheme:
        issue(errors, "nonportable_link", origin, "A packaged file route uses a receiver-specific URI scheme.")
        return
    if not uri.path:
        return  # Fragment anchors are deliberately outside this check.
    relative = unquote(uri.path)
    if "\x00" in relative or "\\" in relative or relative.startswith("/"):
        issue(errors, "nonportable_link", origin, "Packaged file links must be relative local routes.")
        return
    path = (root / origin).parent / relative
    try:
        resolved = path.resolve()
    except (OSError, RuntimeError):
        issue(errors, "unreachable_link", origin, "Cannot resolve a Markdown file route.")
        return
    if not inside(resolved, root):
        issue(errors, "outside_root_link", origin, "A Markdown file route leaves this source root.")
        return
    label = resolved.relative_to(root).as_posix()
    if not path.exists():
        issue(errors, "missing_link", origin, "Markdown file target is missing: " + label)
    elif path.is_symlink() or resolved != Path(os.path.abspath(path)):
        issue(errors, "symlink_link", origin, "Markdown file routes must not depend on symlinks.")
    elif path.is_file() and label not in sources:
        issue(errors, "unpackaged_link", origin, "Markdown file target is outside the declared bundle: " + label)
    elif path.is_dir() and not any(inside(Path(key), Path(label)) for key in sources):
        issue(errors, "unpackaged_link", origin, "Markdown directory target has no declared bundle content: " + label)


def skill_frontmatter(data: bytes, label: str, errors: list[dict]) -> dict[str, str]:
    try:
        lines = data.decode("utf-8").splitlines()
    except UnicodeError:
        issue(errors, "skill_frontmatter", label, "Skill front must be UTF-8 Markdown.")
        return {}
    if not lines or lines[0].lstrip("\ufeff").strip() != "---":
        issue(errors, "skill_frontmatter", label, "Skill front must begin with YAML frontmatter.")
        return {}
    end = next((index for index, line in enumerate(lines[1:], 1) if line.strip() == "---"), None)
    if end is None:
        issue(errors, "skill_frontmatter", label, "Skill frontmatter is not closed.")
        return {}
    result = {}
    for index in range(1, end):
        match = re.match(r"^(name|description):\s*(.*)$", lines[index])
        if not match:
            continue
        key, value = match.groups()
        if key in result:
            issue(errors, "skill_frontmatter", label, "Duplicate name or description in skill frontmatter.")
        if value in {">", "|", ">-", "|-", ">+", "|+"}:
            continuation = []
            for next_line in lines[index + 1:end]:
                if next_line and not next_line[0].isspace():
                    break
                continuation.append(next_line.strip())
            value = " ".join(continuation)
        elif len(value) >= 2 and value[0] == value[-1] and value[0] in {"\"", "'"}:
            value = value[1:-1]
        result[key] = value.strip()
    for key in ("name", "description"):
        if not result.get(key):
            issue(errors, "skill_frontmatter", label, "Skill frontmatter needs nonempty name and description.")
    if result.get("name") and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", result["name"]):
        issue(errors, "skill_name", label, "Skill name must be a lowercase hyphenated identifier.")
    return result


def declared_route(value: Any, label: str, sources: dict[str, bytes], errors: list[dict]) -> str | None:
    try:
        path = local_path(value)
    except ToolError as exc:
        issue(errors, "invalid_route", label, str(exc))
        return None
    if path not in sources:
        issue(errors, "missing_route", label, "Declared route is absent from the source bundle: " + path)
    return path


def embedded_credentials(value: Any) -> bool:
    if isinstance(value, dict):
        return any(str(key).lower() in CREDENTIAL_FIELDS or embedded_credentials(item) for key, item in value.items())
    if isinstance(value, list):
        return any(embedded_credentials(item) for item in value)
    return False


def validate_source(root: Path) -> tuple[dict, dict, dict[str, bytes]]:
    errors: list[dict] = []
    warnings: list[dict] = []
    report = {"ok": False, "kind": "product_source", "source_version": None,
              "counts": {"source_files": 0, "declared_competences": 0},
              "errors": errors, "warnings": warnings, "limits": list(LIMITS)}
    try:
        root = root.resolve()
    except (OSError, RuntimeError):
        issue(errors, "unreachable_root", ".", "Cannot resolve this source root.")
        return report, {}, {}
    if not root.is_dir():
        issue(errors, "missing_root", ".", "Source root is not an existing directory.")
        return report, {}, {}
    manifest_bytes = read_regular(root / MANIFEST_FILE, MANIFEST_FILE, errors)
    manifest = parse_json(manifest_bytes, MANIFEST_FILE, errors) if manifest_bytes is not None else None
    if not isinstance(manifest, dict):
        if manifest_bytes is not None and not errors:
            issue(errors, "manifest", MANIFEST_FILE, "Manifest must be a JSON object.")
        return report, {}, {}
    if manifest.get("schema_version") != MANIFEST_SCHEMA:
        issue(errors, "manifest_schema", MANIFEST_FILE, "Unknown or missing manifest schema_version.")
    report["source_version"] = manifest.get("source_version")
    if manifest.get("source_version") != SOURCE_VERSION:
        issue(errors, "source_version", MANIFEST_FILE, "Source version differs from this reference tool's version " + SOURCE_VERSION + ".")
    bundle = manifest.get("source_bundle")
    if not isinstance(bundle, dict):
        issue(errors, "bundle_include", MANIFEST_FILE, "Manifest needs source_bundle metadata.")
        bundle = {}
    name = bundle.get("name", "social-kernel")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        issue(errors, "bundle_name", MANIFEST_FILE, "Bundle name must be a lowercase hyphenated identifier.")
    sources = collect_source(root, bundle.get("include"), errors)
    report["counts"]["source_files"] = len(sources)
    if MANIFEST_FILE not in sources:
        issue(errors, "missing_route", MANIFEST_FILE, "The manifest itself must be included in the source bundle.")
    entries = manifest.get("entries")
    if not isinstance(entries, dict):
        issue(errors, "entries", MANIFEST_FILE, "Manifest entries must be a route mapping.")
        entries = {}
    for key in REQUIRED_ENTRIES:
        declared_route(entries.get(key), "entries." + key, sources, errors)
    for key, value in entries.items():
        if key not in REQUIRED_ENTRIES:
            declared_route(value, "entries." + key, sources, errors)
    # These optional source routes are checked when declared. State semantics
    # and any additional user/receiver record format remain unconstrained.
    for key in ("receiver_contract", "adoption"):
        if key in manifest:
            declared_route(manifest[key], key, sources, errors)
    for owner, key in (("state_contract", "guidance"), ("evidence", "record")):
        if isinstance(manifest.get(owner), dict) and key in manifest[owner]:
            declared_route(manifest[owner][key], owner + "." + key, sources, errors)
    required_documents = manifest.get("required_documents", [])
    if not isinstance(required_documents, list):
        issue(errors, "required_documents", MANIFEST_FILE, "required_documents must be a path list when supplied.")
    else:
        for value in required_documents:
            declared_route(value, "required_documents", sources, errors)
    competences = manifest.get("competences")
    if not isinstance(competences, list) or not competences:
        issue(errors, "competences", MANIFEST_FILE, "Manifest competences must be a nonempty list.")
        competences = []
    report["counts"]["declared_competences"] = len(competences)
    names, fronts = set(), set()
    for competence in competences:
        if not isinstance(competence, dict):
            issue(errors, "competence", MANIFEST_FILE, "Each competence must declare name and path.")
            continue
        name = competence.get("name")
        path = declared_route(competence.get("path"), "competences", sources, errors)
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            issue(errors, "competence_name", MANIFEST_FILE, "Competence name must be a lowercase hyphenated identifier.")
        elif name in names:
            issue(errors, "duplicate_competence", MANIFEST_FILE, "Competence names must be unique.")
        else:
            names.add(name)
        if path in fronts:
            issue(errors, "duplicate_front", MANIFEST_FILE, "Each competence front must have one declared owner.")
        if path:
            fronts.add(path)
            if PurePosixPath(path).name != "SKILL.md":
                issue(errors, "competence_front", path, "A declared competence front must be a SKILL.md file.")
            if path in sources:
                front = skill_frontmatter(sources[path], path, errors)
                if front.get("name") != name:
                    issue(errors, "competence_name", path, "Skill frontmatter name differs from its declared competence.")
    for path, data in sources.items():
        if PurePosixPath(path).name == "SKILL.md" and path not in fronts:
            issue(errors, "undeclared_front", path, "This bundled skill front has no manifest competence entry.")
        if path.lower().endswith(".md"):
            try:
                text = data.decode("utf-8")
            except UnicodeError:
                issue(errors, "markdown_encoding", path, "Bundled Markdown must use UTF-8.")
                continue
            for target in markdown_targets(text):
                check_link(root, path, target, sources, errors)
    generated = [path for path in (*PLUGIN_FILES, INVENTORY_FILE) if os.path.lexists(root / path)]
    if generated:
        report["kind"] = "source_bundle"
        receiver_plugin = None
        inventory_bytes = read_regular(root / INVENTORY_FILE, INVENTORY_FILE, errors)
        if inventory_bytes is not None:
            saved_inventory = parse_json(inventory_bytes, INVENTORY_FILE, errors)
            if isinstance(saved_inventory, dict) and "receiver_plugin" in saved_inventory:
                try:
                    receiver_plugin = receiver_plugin_metadata(saved_inventory["receiver_plugin"])
                except ToolError as exc:
                    issue(errors, "receiver_plugin_metadata", INVENTORY_FILE, str(exc))
        expected = assembled_files(manifest, sources, receiver_plugin)
        for path in (*PLUGIN_FILES, INVENTORY_FILE):
            actual = read_regular(root / path, path, errors)
            if actual is not None:
                parsed = parse_json(actual, path, errors)
                if path in PLUGIN_FILES and embedded_credentials(parsed):
                    issue(errors, "credential_metadata", path, "Source plugin metadata cannot embed credential fields.")
                if actual != expected[path]:
                    if path in PLUGIN_FILES and parsed == json.loads(expected[path]):
                        warnings.append({
                            "code": "manifest_serialization", "path": path,
                            "message": "Plugin JSON values match; serialized bytes differ from canonical assembly. The inventory records assembly bytes, not this host serialization.",
                        })
                    else:
                        issue(errors, "bundle_metadata", path, "Generated metadata or inventory differs from the current declared file bytes.")
        actual_paths = {path.relative_to(root).as_posix() for path in tree_files(root, root, errors, filter_exclusions=False)}
        for path in sorted(actual_paths - set(expected)):
            issue(errors, "unlisted_bundle_file", path, "Bundle contains a file outside its declared inventory.")
        for path in sorted(set(expected) - actual_paths):
            issue(errors, "missing_bundle_file", path, "Bundle inventory requires this file.")
    report["ok"] = not errors
    return report, manifest, sources


def validate_instance(instance: Path, source_root: Path, report: dict) -> None:
    errors, warnings = report["errors"], report["warnings"]
    try:
        instance, source_root = instance.resolve(), source_root.resolve()
    except (OSError, RuntimeError):
        issue(errors, "unreachable_instance", "instance", "Cannot resolve the instance or source root.")
        report["ok"] = False
        return
    if inside(instance, source_root):
        issue(errors, "instance_inside_source", "instance", "A private instance must be outside the public source root.")
    if not instance.is_dir():
        issue(errors, "missing_instance", "instance", "Instance path is not an existing directory.")
        report["ok"] = False
        return
    metadata_path = instance / "instance.json"
    if not os.path.lexists(metadata_path):
        warnings.append({"code": "manual_state", "path": "instance", "message": "No initializer metadata is present. Manual or host-native state is not assessed by this helper schema."})
        report["ok"] = not errors
        return
    data = read_regular(metadata_path, "instance/instance.json", errors)
    value = parse_json(data, "instance/instance.json", errors) if data is not None else None
    if not isinstance(value, dict):
        if data is not None:
            issue(errors, "instance_schema", "instance/instance.json", "Initializer metadata must be a JSON object.")
        report["ok"] = False
        return
    if value.get("schema_version") != INSTANCE_SCHEMA:
        issue(errors, "instance_schema", "instance/instance.json", "Unknown or missing initializer schema_version; no migration is attempted.")
        report["ok"] = False
        return
    try:
        uuid.UUID(value.get("instance_id", ""))
    except (ValueError, TypeError, AttributeError):
        issue(errors, "instance_id", "instance/instance.json", "instance_id must be a UUID string.")
    if not isinstance(value.get("name"), str) or not value["name"].strip():
        issue(errors, "instance_name", "instance/instance.json", "Instance name must be a nonempty string.")
    source = value.get("source")
    if not isinstance(source, dict) or not isinstance(source.get("name"), str) or not source.get("name") or not isinstance(source.get("version"), str) or not source.get("version"):
        issue(errors, "instance_source", "instance/instance.json", "Instance source needs a name and version.")
    else:
        mark = source.get("fingerprint")
        if not isinstance(mark, dict) or mark.get("algorithm") != "sha256" or not isinstance(mark.get("digest"), str) or not re.fullmatch(r"[a-f0-9]{64}", mark.get("digest", "")) or mark.get("scope") != FINGERPRINT_SCOPE or mark.get("qualification") != FINGERPRINT_QUALIFICATION or not isinstance(mark.get("file_count"), int) or isinstance(mark.get("file_count"), bool) or mark["file_count"] < 1:
            issue(errors, "instance_fingerprint", "instance/instance.json", "Expected a qualified local source-inventory fingerprint.")
        warnings.append({"code": "historical_provenance", "path": "instance/instance.json", "message": "Source provenance records initialization. It is not required to equal today's source and does not establish current applicability."})
    try:
        entry = local_path(value.get("state_entry"))
        state_path = instance / entry
        resolved_state = state_path.resolve()
        if not inside(resolved_state, instance):
            issue(errors, "instance_state", "instance/instance.json", "State entry must remain within its private instance.")
        elif resolved_state != state_path:
            issue(errors, "instance_state", "instance/instance.json", "Initializer state entry must not depend on a symlink.")
        else:
            read_regular(state_path, "instance/" + entry, errors)
    except (ToolError, OSError, RuntimeError):
        issue(errors, "instance_state", "instance/instance.json", "State entry must be a reachable local file in this instance.")
    if embedded_credentials(value):
        issue(errors, "credential_metadata", "instance/instance.json", "Initializer metadata cannot embed credential fields.")
    report["ok"] = not errors


def absent_destination(value: str, source_root: Path) -> Path:
    requested = Path(value).expanduser()
    if not requested.is_absolute():
        raise ToolError("Destination must be an absolute path.")
    if os.path.lexists(requested):
        raise ToolError("Destination already exists; nothing was overwritten or migrated.")
    try:
        parent = requested.parent.resolve(strict=True)
    except (OSError, RuntimeError):
        raise ToolError("Destination parent must already exist.") from None
    if not parent.is_dir():
        raise ToolError("Destination parent must be an existing directory.")
    destination = parent / requested.name
    if inside(destination, source_root.resolve()):
        raise ToolError("Destination must be outside the public product or source-bundle root.")
    if os.path.lexists(destination):
        raise ToolError("Destination already exists; nothing was overwritten or migrated.")
    return destination


def write_new_tree(destination: Path, files: dict[str, bytes], private: bool = False) -> None:
    """Create absent files only; clean up only objects created by this call."""
    directory_mode, file_mode = (0o700, 0o600) if private else (0o755, 0o644)
    created_directories = []
    created_files = []
    try:
        destination.mkdir(mode=directory_mode)
        created_directories.append(destination)
        parents = set()
        for label in files:
            local_path(label)
            for parent in PurePosixPath(label).parents:
                if parent != PurePosixPath("."):
                    parents.add(parent)
        for relative in sorted(parents, key=lambda item: (len(item.parts), item.as_posix())):
            directory = destination / relative.as_posix()
            directory.mkdir(mode=directory_mode)
            created_directories.append(directory)
        for label, data in sorted(files.items()):
            path = destination / label
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, file_mode)
            identity = os.fstat(descriptor)
            created_files.append((path, identity.st_dev, identity.st_ino))
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(data)
    except (OSError, ToolError):
        for path, device, inode in reversed(created_files):
            try:
                status = path.lstat()
                if (status.st_dev, status.st_ino) == (device, inode):
                    path.unlink()
            except OSError:
                pass
        for directory in reversed(created_directories):
            try:
                directory.rmdir()
            except OSError:
                pass
        raise ToolError("Could not create the absent destination; no existing file was overwritten. Inspect the destination if another writer changed it during creation.") from None


def require_valid_source(root: Path) -> tuple[dict, dict[str, bytes]]:
    report, manifest, sources = validate_source(root)
    if not report["ok"]:
        first = report["errors"][0]
        raise ToolError("Source validation failed (" + first["code"] + ": " + first["path"] + "). Run scripts/validate.py --root for details.")
    return manifest, sources
