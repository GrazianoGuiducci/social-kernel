#!/usr/bin/env python3
"""Optionally seed a new private field outside the public source tree."""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import uuid

from _common import DEFAULT_ROOT, INSTANCE_SCHEMA, ToolError, absent_destination, bundle_name, fingerprint, inventory, json_bytes, require_valid_source, write_new_tree


CURRENT = """# Current private social field

Status: unconfigured.

## Owner and purpose

No owner, public identity, project, audience, channel, or receiver is selected.
Connect this entry to the situation and private sources you choose to use.

## Present situation

No sources, relationships, earlier effects, open obligations, or learned local
methods have been imported. Preserve relevant continuity through the records
and storage that suit your actual work; this file is only a starting entry.

## Authority and capability

No account, controller, credential, publication, messaging, moderation,
spending, or recurring authority is configured or inherited from the product.
Resolve the actual receiver capability and applicable user authority when a
selected movement needs them.

## Next useful reentry

Provide the selected Social Kernel source entry and the actual situation to
your receiver. Start with the useful work now possible. Preserve its result,
reason, material uncertainty, and learned method where later work can reach it.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", required=True, help="Absent absolute directory outside the source root, in an existing parent.")
    parser.add_argument("--name", default="Private Social Kernel instance", help="Private descriptive name; does not configure a public identity.")
    args = parser.parse_args()
    try:
        if not args.name.strip() or any(ord(character) < 32 for character in args.name):
            raise ToolError("Name must contain text and no control characters.")
        destination = absent_destination(args.destination, DEFAULT_ROOT)
        manifest, sources = require_valid_source(DEFAULT_ROOT)
        metadata = {
            "schema_version": INSTANCE_SCHEMA,
            "instance_id": str(uuid.uuid4()),
            "name": args.name.strip(),
            "source": {"name": bundle_name(manifest), "version": manifest["source_version"],
                       "fingerprint": fingerprint(inventory(sources))},
            "state_entry": "CURRENT.md",
        }
        write_new_tree(destination, {"instance.json": json_bytes(metadata), "CURRENT.md": CURRENT.encode("utf-8")}, private=True)
    except ToolError as exc:
        print("REFUSED: " + str(exc), file=sys.stderr)
        return 1
    print(f"Created a private instance at {destination}")
    print(f"Source version {manifest['source_version']}; CURRENT.md is unconfigured, with no inherited authority.")
    print("Only instance.json and CURRENT.md were created. Manual or host-native state remains a valid alternative.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
