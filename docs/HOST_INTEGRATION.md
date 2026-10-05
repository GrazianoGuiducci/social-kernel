# Use Social Kernel in your AI environment

Social Kernel supplies methods for understanding a public situation, making
content, continuing relationships and learning from what happens. Your AI
environment supplies reading, writing, memory, media tools and any connection
to outside services. Begin with the environment and knowledge you already use.

## Compose with the existing entry

Find the entry from which your assistant currently starts, the methods it can
reach and the place where your work continues. If you already have a kernel,
skills or project memory, retain their useful knowledge and ownership. Read the
relevant bodies when two methods seem to overlap; similar names do not establish
equivalence, and different names do not require duplicate owners.

Make Social Kernel's [BOOT](../BOOT.md) and pertinent [competences](../COMPETENCES.md)
reachable when public work needs them. An existing reentry or learning method
can continue to perform its function while the public-work methods deepen the
social relation. MAIOS Project Kernel, kernel_chat or another operating system
can participate through what they already know. None is a prerequisite to use
this product.

Keep a small integration note at the current entry if these locations would
otherwise be lost:

| Relation | What the next receiver must be able to reach |
| --- | --- |
| Shared method | This source revision or saved bundle, its BOOT and selected skill bodies. |
| Your current field | Your purpose, sources, drafts, assets, relationships and open obligations. |
| Your learned method | The local extension or existing competence that carries a useful adaptation. |
| Actual means | Available tools, storage and the controller of any selected external action. |

This note can fit the record you already use. Creating a second competing
current-state file is unnecessary. This repository's `AGENTS.md` guides work on
the product source; its product `CURRENT.md` records source development. Keep
your own project instructions and public-work state with their existing owners.

For an initial session, provide the readable method and your current context,
then ask:

> Continue [the selected work] from [my current entry]. Compose the Social
> Kernel method at [its readable BOOT] with the useful methods already present.
> Use the available means, preserve the result and its reasons, and connect
> any learned method to the next relevant entry.

When the host cannot resolve a link, supply the needed body as readable content.
Copying one skill folder can break its references to sibling methods or root
knowledge. Keep the delivered dependency closure reachable.

## Choose a source projection

The optional builder copies the same declared source bytes for three targets:

| Target | Generated files in addition to the shared source | Receiving use |
| --- | --- | --- |
| `portable` | `BUNDLE_INVENTORY.json` | Readable method for a file-based or session-based receiver. |
| `openai` — default | `plugin.json`, `.codex-plugin/plugin.json`, inventory | Source preparation for an OpenAI plugin mechanism. |
| `claude-code` | `.claude-plugin/plugin.json`, inventory | Source preparation using Claude Code's documented plugin layout. |

From the source checkout, select one new destination outside it:

```sh
python3 scripts/build_plugin.py --target portable --destination "/absolute/new/social-kernel-portable"
python3 scripts/build_plugin.py --target openai --destination "/absolute/new/social-kernel-openai"
python3 scripts/build_plugin.py --target claude-code --destination "/absolute/new/social-kernel-claude"
```

These are three alternatives; use the one you need. The destination must be
absent and its parent must exist. In Windows, use the installed Python 3
launcher and a Windows absolute path. The observed interpreter/platform checks
are recorded in [Verification](VERIFICATION.md).

Run the validator copied into the chosen bundle:

```sh
python3 /absolute/new/social-kernel-portable/scripts/validate.py --root "/absolute/new/social-kernel-portable"
```

Its inventory names the projection target, source version, source fingerprint
and any supplied receiver identity. Inventory v2 describes these targets. A
historical v1 bundle keeps its own copied tools and evidence; this command does
not migrate it. The [instance helper schema](STATE_AND_RECORDS.md) remains v1,
and initialization provenance need not equal the newest public source.

The builder creates a new source directory. It does not patch your entry,
memory, settings or installed skills. It supplies no MCP server, social API
client, browser session, hook or scheduler. If an existing receiver package
already contains integrations or assets, its packaging owner must preserve
them during a selected update. This builder accepts only its documented
identity metadata and refuses unsupported metadata fields.

## Connect the entry to the actual host

The following documented routes were inspected on **2026-10-05**. They guide
adaptation; [Verification](VERIFICATION.md) records what this source was actually
tested to do.

### Codex and OpenAI receivers

Codex's local skill discovery uses its documented `.agents/skills` locations;
an arbitrary repository `skills/` folder is not that installation route. Skill
descriptions help selection, and the body is loaded when selected. Use the
actual skill selector or loading evidence to resolve the intended method,
especially in a large existing catalog. See [OpenAI's skill documentation](https://learn.chatgpt.com/docs/build-skills).

Codex also reads an instruction chain whose project position affects what
guidance applies. Integrate a reference into the appropriate existing entry
when that change is selected, preserving its useful instructions. See
[AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

For plugin delivery, use the mechanism supported by the actual OpenAI surface.
OpenAI documents plugin discovery in the ChatGPT desktop app and Codex CLI,
with different support in other surfaces; a repository bundle is not an
installed catalog entry. See [OpenAI plugins](https://learn.chatgpt.com/docs/plugins)
and the [OpenAI projection guide](OPENAI_PLUGIN_INCARNATION.md).

### Claude Code

Claude Code documents `.claude-plugin/plugin.json` with skills under `skills/`.
Plugin skills use a plugin namespace, which lets them coexist with local
skills. The generated target follows that layout. A `CLAUDE.md` placed in the
plugin root does not load as context, so the method must be reached through
its skill entry or an explicit read. See the [plugin manifest reference](https://code.claude.com/docs/en/plugins-reference)
and [skill documentation](https://code.claude.com/docs/en/skills).

In an equipped environment where this bounded exercise is selected, first
use the native validator, then load the new directory for an isolated session:

```sh
claude plugin validate "/absolute/new/social-kernel-claude"
claude --plugin-dir "/absolute/new/social-kernel-claude"
```

Inspect the discovered entry, such as
`/social-kernel:social-kernel-operating-cycle` with the default plugin name.
Confirm the body and its references are readable, then use it for one useful
piece of work. These commands are receiving instructions, not evidence that
they have run for this product.

When using an existing project, preserve its `CLAUDE.md`, memory and local
rules. Granting access to an additional directory does not by itself load that
directory's memory files; the host has separate import rules. See
[Claude Code memory](https://code.claude.com/docs/en/memory).

### Other receivers

Provide BOOT, its necessary linked bodies and your own current field as
readable files or attachments. Translate entry and persistence into the
receiver's real means. Keep the original source identity and the local
adaptation distinguishable. A prompt-only receiver can prepare and reason with
those sources; durable file updates and external execution depend on tools it
actually exposes.

## Make external capabilities concrete

A method can select a useful action before the current host has a way to
execute it. Resolve the actual callable operation: which tool or provider is
available, which account and target it reaches, what it can read or change,
and what return will establish the result. An API description, URL or key is
only preparation until an available client, connector, MCP server or other
tool exposes the operation. See the distinction between skills and tool
services in [OpenAI plugins](https://learn.chatgpt.com/docs/plugins) and
[Claude Code MCP](https://code.claude.com/docs/en/mcp).

Use an existing capable integration where it fits. If a custom bridge is
needed, prepare its exact operation, inputs, output/readback and missing setup
for the owner who can build it. Keep useful independent preparation moving.
The [effect boundary](../skills/social-effect-boundary/SKILL.md) governs the
selected action through the current controller and applicable authority.

## Verify continuation and preserve local learning

Observe the real receiving chain: source available, intended entry discovered,
body read, method exercised, result saved and later work changed by the saved
knowledge. Record the host/version, source identity, observed artifacts and any
extra help. A native manifest check establishes its own loading contract; it
does not establish editorial quality, media generation or later assimilation.

Keep generated assets and their selected versions with the private work.
Keep a reusable local method where the next entry can reach it. Before an
upstream update, compare the old shared base, local changes and incoming
method. Preserve useful local learning and reconcile the routes that consume
the change. For managed or immutable bundles, keep extensions at a separate
writable owner rather than editing a cached projection. Continue through
[Adoption](ADOPTION.md), [Evolution](../EVOLUTION.md) and the bounded tasks in
[Codex continuation](CODEX_CONTINUATION.md).
