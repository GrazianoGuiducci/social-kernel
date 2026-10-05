# Begin with a useful piece of public work

Social Kernel can be used through readable sources before any platform integration is selected. Choose a situation whose current meaning matters: a discussion to understand, a draft to prepare, an open relationship to resume, or a consequence that should change later work.

The current source state is in [CURRENT](../CURRENT.md). [BOOT](../BOOT.md) leads to the operating knowledge; [the worked example](WORKED_EXAMPLE.md) shows a complete relation using fictional material.

## Give your receiver a reachable entry

Use the route available in your environment:

| Route | What to provide | What can continue |
| --- | --- | --- |
| Readable repository | This repository's BOOT and access to the linked public sources, plus the relevant user context. | The current exercise; durable continuation depends on a real user-owned write route. |
| User-owned files or project | BOOT, its linked knowledge and the selected private field's actual sources/state. | Method and state can continue in those files when the receiver can write them. |
| Session-only sources | BOOT and the method bodies it selects, plus the situation, as readable attachments or text. | Work can continue in the current session; ask for a concise continuation to save and supply at the next entry. |

Ask the receiver:

> Read BOOT and use Social Kernel for this situation: [describe the actual work or provide its current source]. Recover the relevant context and use the competences that change the result. Continue from what is already known, make any missing source or capability precise, and preserve the useful result and learned method through the means available here.

Opening a repository or attaching files does not itself install an assistant extension. A native host entry must follow that host's actual discovery mechanism and remain connected to the living method. [The receiver contract](RECEIVER_CONTRACT.md) explains this translation.

## Keep your continuing field under your control

Keep accounts, contacts, private drafts, relationship state and permissions in a location selected for your own work. The public product checkout is the source of shared methods, not a place to commit that private field.

Reuse a suitable existing private owner where possible. Its current entry should reach the actual purpose, source references, relevant past events, pending work, current authority and learned methods. Preserve only the detail that later work needs. [State and records](STATE_AND_RECORDS.md) supplies the method without requiring one storage schema.

### Optional local initialization

The small [initializer](../scripts/init_instance.py) creates an initial private field in a separate directory you select. It requires Python 3; reading and exercising the semantic method does not. The exact locally exercised interpreter is recorded in the product's verification evidence; this command example does not establish a wider support matrix.

From the source checkout, run:

```sh
python3 scripts/init_instance.py --destination "/absolute/path/to/new-private-field" --name "My public work"
```

Replace the destination with an absolute directory outside the public checkout that does not yet exist, within an existing parent directory. The command refuses every existing destination, including an empty directory or symlink. It creates `instance.json` with a new instance identity, source version and qualified fingerprint of the declared source bytes, and a private `CURRENT.md` with context unconfigured and no inherited effect authority. The fingerprint describes local source identity; it is not a Git release or host-compatibility certificate. The command does not install a host adapter, create accounts, start automation or grant publishing rights.

Read the new CURRENT with your receiver and connect it to your real situation. Preserve a route to the public revision or saved bodies that supplied the method; a version label alone does not recover their knowledge. An unconfigured field can begin with observation, inquiry or a draft. The user determines any authority that becomes pertinent to an actual effect; completing a template cannot manufacture it.

### Optional source bundle

[The bundle builder](../scripts/build_plugin.py) can assemble the current canonical knowledge for an OpenAI-oriented receiver:

```sh
python3 scripts/build_plugin.py --destination "/absolute/path/to/new-social-kernel-bundle"
```

Use a new absent destination outside the source checkout, within an existing parent directory. This produces source material for receiver exercise; bundle assembly is separate from host installation, discovery and observed behavior. Existing private-preview files describe an earlier probe and are not proof that this candidate is already installed anywhere. See [the adapter record](OPENAI_PLUGIN_INCARNATION.md).

## Complete one useful movement

Let the situation determine whether the useful result is understanding, a response, a draft, a source correction, a delegated observation, or a deliberate wait. Reach deeper expression, relationship or cognitive-integrity methods when they contribute. A content calendar is unnecessary for this first use.

If an external effect is selected, use the actual controller and applicable authority, check the current source and target relation, then preserve native readback. If the purpose is only preparation, stop at the useful artifact. [Recurring operation](RECURRENT_OPERATION.md) is available when a later task actually calls for scheduled work; no cadence is inherited by adoption.

Read what the result changes. Teach a reusable difference to the owning competence and keep a compact current continuation pointing to it. At the next relevant situation, inspect whether that knowledge changes the question or decision. The [worked example](WORKED_EXAMPLE.md) carries this through two different encounters.

## Return after an interruption or source change

Give the next receiver your private current entry and a reachable version of the public method. Reconcile current user intent, material source changes, still-open effects and relationship state before continuing. A previous next action may now be stale; a closed action need not reopen without a relevant change.

When considering a newer public source, compare the method you began with, your locally evolved knowledge and the new proposal. Preserve compatible learning and follow selected changes into the entries that actually consume them. [Evolution](../EVOLUTION.md) explains how the changed result keeps its own evidence.

If no durable write route is available, have the receiver return the current purpose, source identity, completed result, its reason, the changed method, unresolved question and next useful entry. Save that continuation yourself. This qualifies what can survive; it does not require inventing a filesystem or background agent.
