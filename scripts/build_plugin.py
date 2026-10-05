#!/usr/bin/env python3
"""Assemble canonical source bytes in a new directory; never install or execute."""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

from _common import DEFAULT_ROOT, ToolError, absent_destination, assembled_files, require_valid_source, write_new_tree


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", required=True, help="Absent absolute directory outside the source root, in an existing parent.")
    parser.add_argument("--plugin-manifest", type=Path, help="Optional Agent Plugins identity/presentation JSON for an existing receiver; source version remains separate.")
    args = parser.parse_args()
    try:
        destination = absent_destination(args.destination, DEFAULT_ROOT)
        manifest, sources = require_valid_source(DEFAULT_ROOT)
        receiver_plugin = None
        if args.plugin_manifest is not None:
            try:
                receiver_plugin = json.loads(args.plugin_manifest.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, ValueError):
                raise ToolError("Cannot read receiver plugin metadata as UTF-8 JSON.") from None
            if receiver_plugin is None:
                raise ToolError("Receiver plugin metadata must be an object.")
        files = assembled_files(manifest, sources, receiver_plugin)
        write_new_tree(destination, files)
    except ToolError as exc:
        print("REFUSED: " + str(exc), file=sys.stderr)
        return 1
    print(f"Assembled {len(files)} files at {destination}")
    print(f"Source version {manifest['source_version']}; deterministic bytes and an independently checkable file inventory.")
    print("Source assembly only: no installation, release, scheduler, account change, or execution.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
