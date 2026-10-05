#!/usr/bin/env python3
"""Assemble canonical source bytes in a new directory; never install or execute."""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse

from _common import DEFAULT_ROOT, ToolError, absent_destination, assembled_files, require_valid_source, write_new_tree


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", required=True, help="Absent absolute directory outside the source root, in an existing parent.")
    args = parser.parse_args()
    try:
        destination = absent_destination(args.destination, DEFAULT_ROOT)
        manifest, sources = require_valid_source(DEFAULT_ROOT)
        files = assembled_files(manifest, sources)
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
