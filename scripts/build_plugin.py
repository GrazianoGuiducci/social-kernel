#!/usr/bin/env python3
"""Assemble canonical source bytes in a new directory; never install or execute."""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
from pathlib import Path

from _common import DEFAULT_ROOT, TARGET_PLUGIN_FILES, ToolError, absent_destination, assembled_files, parse_json, require_valid_source, write_new_tree


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", required=True, help="Absent absolute directory outside the source root, in an existing parent.")
    parser.add_argument("--target", choices=tuple(TARGET_PLUGIN_FILES), default="openai", help="Source projection: openai (default), claude-code, or portable method without plugin metadata.")
    parser.add_argument("--plugin-manifest", type=Path, help="Optional receiver identity JSON: Agent Plugins identity/presentation for OpenAI, shared identity for Claude Code. Source version remains separate.")
    args = parser.parse_args()
    try:
        destination = absent_destination(args.destination, DEFAULT_ROOT)
        manifest, sources = require_valid_source(DEFAULT_ROOT)
        receiver_plugin = None
        if args.plugin_manifest is not None:
            if args.target == "portable":
                raise ToolError("The portable target has no plugin identity; omit --plugin-manifest.")
            try:
                metadata_bytes = args.plugin_manifest.read_bytes()
            except OSError:
                raise ToolError("Cannot read receiver plugin metadata.") from None
            errors = []
            receiver_plugin = parse_json(metadata_bytes, "receiver metadata", errors)
            if errors:
                raise ToolError("Receiver metadata must be unambiguous UTF-8 JSON, without duplicate keys.")
            if not isinstance(receiver_plugin, dict):
                raise ToolError("Receiver plugin metadata must be an object.")
        files = assembled_files(manifest, sources, receiver_plugin, args.target)
        write_new_tree(destination, files)
    except ToolError as exc:
        print("REFUSED: " + str(exc), file=sys.stderr)
        return 1
    print(f"Assembled {len(files)} files for target {args.target} at {destination}")
    print(f"Source version {manifest['source_version']}; deterministic bytes and an independently checkable file inventory.")
    print("Source assembly only: no installation, release, scheduler, account change, or execution.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
