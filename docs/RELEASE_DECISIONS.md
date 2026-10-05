# License and first release: prepared owner decisions

The current result is the `0.2.0-dev.1` public source candidate. Source changes,
local assembly and recorded exercises do not select a license or publish a
stable release. This document makes those remaining decisions concrete.

## Choose the reuse grant

For a product intended to be reused and adapted in different AI environments,
a single permissive license for the original method, documentation and helper
code would keep adoption understandable. Two practical choices are:

| Choice | Material terms | Why choose it here |
| --- | --- | --- |
| **Apache-2.0 — proposed** | Express copyright and contributor patent grants; redistribution retains applicable notices and identifies changed files. It does not grant trademark use. See the [official license, sections 2–4 and 6](https://www.apache.org/licenses/LICENSE-2.0). | Makes the reuse terms explicit for organizations integrating and extending the product. |
| **MIT** | Broad permission to use, modify and distribute software and associated documentation, including commercial reuse, with the copyright and permission notice retained. See the [official license text](https://opensource.org/license/mit). | A shorter notice and a simpler distribution document, if that is the owner's priority. |

This proposal is a product choice to review, not a license grant. The owner
must select the license, copyright holder and covered material. Do not infer
that choice from another MAIOS repository's license.

Keep the scope inspectable:

- Original kernel, skills, references, documentation and helper code: include
  them explicitly in the selected grant.
- Linked sources: retain their provenance. A link does not import that
  source's entire license or make its contents part of this package.
- Included examples and media: retain their production provenance and identify
  any separately licensed material. Decide their distribution terms with the
  source grant; do not silently describe generated imagery as an exclusive
  owned brand asset.
- User instances, account state and private learned methods: they are outside
  this public package and remain with their owners.

After selection, add the actual `LICENSE` and any required notice, include
them in `KERNEL_MANIFEST.json`'s source bundle, and make the generated metadata
agree with that selected source license. Rebuild and validate each affected
profile. Adding a license file beside an inventory does not update a previously
built package.

## Choose the first distribution form

**Proposed next form: a development pre-release** tied to one exact reviewed
source commit, with the three mechanically checked projections and their
inventories. A suitable tag is `v0.2.0-dev.1` if it remains unused and still
identifies the selected source. Include release notes explaining the useful
creative methods, the observed internal exercise, the actual host checks and
any remaining receiving limits.

This form lets early adopters inspect and exercise the same source while its
native receiving evidence grows. The alternative is to keep distributing the
source branch until a selected native-host trial is complete. A stable release
should state only the host behavior and continuing use actually observed for
its version; it need not promise universal portability.

The bundle builder prepares directories. Creating archives, a Git tag, a GitHub
release, a marketplace listing or an installed personal plugin remains a
separate selected action. The current work does not perform those actions.

## Exact receiving packet after the owner decides

Record the chosen license and holder, covered material, source commit,
release form and tag, intended audiences, and host claims supported by the
[verification record](VERIFICATION.md). Confirm the license and notices are
inside every delivered archive. Keep a previous receiver's version and local
learning intact when any later installation is selected.

Use [Codex continuation](CODEX_CONTINUATION.md) for native validation and
bounded receiving use. Those tasks can expose a concrete source correction;
they do not choose the product's legal or release identity on the owner's
behalf.
