# Executable Effect Freshness

A prepared post, browser handoff or scheduled artifact expresses an earlier
determination. Its content may remain mechanically usable while its purpose,
source, relationship or authority has changed.

Use this method from [effect boundary](../skills/social-effect-boundary/SKILL.md)
whenever an external action depends on saved state.

## The relation that must survive

At T0 an effect is selected and a packet is prepared. At T1 a new source,
consequence, correction or policy changes its eligibility. The old packet
remains evidence of the earlier choice; it must not execute as though T1 had
not happened.

Current applicable owner determination takes precedence over a stale queue or
schedule. Currentness is not simply the newest timestamp: resolve what each
source governs, when it applies and what it actually supersedes. Compatible
knowledge from different owners can remain jointly useful.

## Before the dependent write

Resolve both mechanical readiness and semantic eligibility.

| Mechanical relation | Semantic relation |
| --- | --- |
| Correct native account, target and available means | Current operator direction and selected purpose |
| Final content, links and assets render as intended | Source claims and exact approved revision still apply |
| Controller can perform the action | That controller has authority for this action class |
| Native constraints permit the intended form | Conversation, relationship and newer consequences still support the movement |
| Native receipt can be inspected | No duplicate or unresolved attempt makes this a repeat |

Check relations whose drift could change this action. An old coordinate is
genealogy, not proof that the outside world is unchanged. A found search result
or reselected browser tab also needs relevant freshness qualification.
If a handoff, delay or new signal intervenes and can change a decisive condition,
refresh that relation at the actual write. A past preflight does not lock a
changing external authority or guarantee an atomic check-and-send operation.

If the effect remains authorized and useful, execute it. Do not require another
approval of unchanged scope simply because the system woke again.

If it was requalified, superseded or closed, stop that effect and recompose.
Do not ask for reconfirmation of obsolete copy to satisfy an old queue.

## Approval and artifact changes

When policy requires approval, bind it to the exact revision, destination,
identity and material assets. A visual must actually be visible to the approving
person. Approval of a topic or an inaccessible image path does not approve
unseen final content.
Positive feedback on layout or tone has its own scope; it does not by itself
approve the message or the complete text-and-asset package.

Resolve authority again when changed content, assets, meaning or destination
falls outside the approval or allowed deviations. Preserve the earlier approval
and later reason. Clear contextual approval is sufficient; do not require a
special phrase or repeat the request when the exact choice is already clear.

A broad project description does not silently cancel a specific restriction.
A general method document cannot restore permission revoked by the authorized
operator.

## Uncertain occurrence and duplicate recovery

A timeout, disappearing success notice, failed screenshot or failed source
push does not show that publication failed.

Before retrying:

1. Recover the in-flight target, action, account and content/revision.
2. Inspect the native target, permalink, Sent folder or equivalent occurrence
   source through available authorized means.
3. Compare identity, body/action and time with the attempted effect.
4. If it occurred, recover the receipt into the local owner; do not send again
   to repair bookkeeping.
5. If unresolved, retain uncertainty and the missing observation. Retry only
   when non-occurrence or a safe native retry mechanism is established.

Native idempotency may help when actually available. These instructions do not
provide a distributed exactly-once guarantee. Several receivers should consult
one current effect controller and shared receipts. See
[recurrent operation](RECURRENT_OPERATION.md).

## Fictional example

A research group's assistant prepares an answer to a forum question. Before
sending, the author answers it and another participant supplies the planned
example. The old answer is still correct and the account works. Its
conversational function has changed.

The assistant reads the exchange, retains the draft as superseded, and chooses
a distinct useful follow-up or no_action. It does not paste the saved answer
solely because it was ready yesterday.

If a later useful reply is sent but the local record write fails, the next
receiver inspects the native thread first. A matching reply restores the receipt,
not another publication.

This illustrates the contract; it is not an occurred customer result or a
platform test.

## Return

Preserve what changed eligibility, its source, the disposition, any actual
occurrence and the next useful continuation.
[State and records](STATE_AND_RECORDS.md) offers adaptable record shapes.
[Effect and consequence](../skills/social-effect-consequence/SKILL.md) interprets
observed results without fabricated causality.
