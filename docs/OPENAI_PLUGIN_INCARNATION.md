# OpenAI source bundle

The canonical Social Kernel method lives in the public core and `skills/`. An OpenAI-style source bundle is one receiver projection. The reference builder includes those owners and their local dependencies so a receiving skill does not require an inaccessible private repository.

[Host integration](HOST_INTEGRATION.md) also describes the portable method
and Claude Code projections, with their documented entry routes and actual
evidence limits. Every projection copies the same declared source bytes.

## Assemble and inspect

From the product checkout, choose a new destination outside it:

```bash
python3 scripts/build_plugin.py --target openai --destination /absolute/new/social-kernel-bundle
python3 /absolute/new/social-kernel-bundle/scripts/validate.py --root /absolute/new/social-kernel-bundle
```

The bundle carries plugin metadata, canonical skill bodies, core knowledge and an inventory of its bytes. Rebuilding the same source should produce the same file content. It does not create a private user instance, publish a release or install anything in a host.

Omitting `--target` preserves the OpenAI default. `--target portable` omits
plugin metadata; `--target claude-code` derives `.claude-plugin/plugin.json`
instead of the two OpenAI manifests. Inventory schema v2 records the target
alongside source identity. Earlier v1 bundles retain their own tools and proof;
no inventory or user-instance migration is performed.

## Update an existing receiver identity

An existing plugin can have its own name, version history and presentation.
Preserve these when bringing it the current public method. The public source
version and receiver plugin version identify different objects; a source
version must not downgrade or rename the installed plugin.

Read the current plugin's effective manifests and preserve its identity,
audience, author metadata, assets and complete default prompts. Prepare a
portable Agent Plugins 1.0 manifest outside this public source. Use a greater
receiver version and retain presentation under
`extensions.com.openai.interface`. The listing subtitle is at most 30
characters. Then assemble with:

```bash
python3 scripts/build_plugin.py --target openai --destination /absolute/new/receiver-bundle --plugin-manifest /absolute/receiver-metadata.json
python3 /absolute/new/receiver-bundle/scripts/validate.py --root /absolute/new/receiver-bundle
```

The optional manifest supplies identity and presentation only. This builder
refuses tool, hook and app configuration rather than silently introducing
capabilities or claiming to preserve integrations it did not package. Referenced
assets still need their native packaging owner. The canonical skill bytes are
copied unchanged; the compatibility manifest derives its presentation from the
portable manifest. The inventory records both source identity and receiver
metadata, and the copied validator checks that resulting projection.

For `claude-code`, the same option accepts shared identity fields: name,
semantic version, description and optional author/homepage/repository/license/
keywords. It rejects OpenAI presentation extensions and execution fields so
they cannot disappear silently or become new capabilities. The optional
`$schema`, when supplied, must be the shared Agent Plugins 1.0 identity schema.
The portable method-only target rejects `--plugin-manifest`. Input JSON with
duplicate keys is refused for either plugin target.

Keep account identifiers, update receipts and previous-package backups at the
private receiver owner. Use the host's supported update mechanism and guard
against a concurrently changed release. Native discovery and later use must
observe the installed result; a successful account update alone establishes
only the saved release.

A receiving service may reserialize generated plugin JSON without changing
its values. Read back the actual saved archive when exact byte identity matters;
a text-file API may also normalize line endings. The validator accepts equivalent
JSON values for the two generated plugin manifests and explicitly reports the
serialization difference. Their inventory hashes still identify canonical
assembly bytes, not the host's serialization. Canonical source bodies and the
inventory itself retain exact-byte checks; a changed metadata value still fails.

## Verify the receiving host

Use the receiver's actually available installation or loading mechanism. Confirm what it loads, whether discovery reaches the intended skill body and whether local references remain reachable. A file check does not prove the current host accepts the package or that its model follows the method.

Public source version `0.2.0-dev.2` is a development identity. Native installation, activation and post-interruption use remain separate checks in [Codex continuation](CODEX_CONTINUATION.md). Preserve existing configured skills and user state until a selected update has its own recovery path.

## Earlier probe

`plugin-adapters/openai/private-preview/` preserves the earlier 0.2.1 skills-only source snapshot. It is excluded from current bundle assembly. Its five skill files are a historical partial projection; current canonical skills supply the fuller method. No private plugin release identifier or installation result is needed to use the public source.
