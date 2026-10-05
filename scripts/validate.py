#!/usr/bin/env python3
"""Read-only structural checks for a declared source tree or assembled bundle."""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

from _common import DEFAULT_ROOT, validate_instance, validate_source


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Product or bundle root (defaults to this script's source root).")
    parser.add_argument("--instance", type=Path, help="Optionally inspect initializer metadata; manual state has no required helper schema.")
    parser.add_argument("--json", action="store_true", help="Return a machine-readable report.")
    args = parser.parse_args()
    report, _manifest, _sources = validate_source(args.root)
    if args.instance is not None:
        validate_instance(args.instance, args.root, report)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        status = "OK" if report["ok"] else "FAILED"
        counts = report["counts"]
        print(f"{status}: {report['kind']}; {counts['source_files']} declared source files, "
              f"{counts['declared_competences']} competences; version {report['source_version']}.")
        for item in report["errors"]:
            print(f"ERROR {item['code']} [{item['path']}]: {item['message']}")
        for item in report["warnings"]:
            print(f"NOTE {item['code']} [{item['path']}]: {item['message']}")
        print("Structural checks only; no semantic, privacy, installation, host-compatibility, safety, or operation proof.")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
