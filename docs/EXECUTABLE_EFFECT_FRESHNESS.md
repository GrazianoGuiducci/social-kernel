# Executable Effect Freshness

Social Kernel treats an executable packet, scheduled artifact or browser handoff
as a **projection of a prior public field**, not as permanent authority.

## Core relation

~~~text
field at T0
-> effect selected
-> executable packet formed

field changes at T1
+ a newer consequence / source / relationship / authority relation
  changes whether the effect is still useful or valid
-> prior packet loses semantic eligibility
-> controller must reenter current field before the write
~~~

A technically valid packet can therefore be semantically stale.

## Before an external effect

Resolve both:

~~~text
mechanical readiness
  surface / account / controller / native rules / artifact

semantic freshness
  current owner state / current effect eligibility / current authority /
  duplicate-or-overlap / newer consequence
~~~

Passing the first does not imply the second.

## Current owner outranks queued projection

When a current owner-native state explicitly requalifies, supersedes, closes or
materially changes an effect:

~~~text
current owner decision
> older queue entry
> older browser packet
> older schedule
~~~

The old packet remains genealogy. It is not executable authority.

Do not ask the operator to reconfirm an effect that the current field has already
made obsolete merely because an automation or browser still has its copy.

## Controller behavior

A browser, agent, scheduler or other executor should:

1. reenter the minimum current owner state before the first write;
2. verify that the effect id is still selected/eligible;
3. stop the stale effect if current state disagrees;
4. return the semantic drift as a readback;
5. execute only after current semantic and mechanical conditions agree.

## Automation boundary

A scheduler may wake the system but should not blindly paste an old artifact.

Preferred relation:

~~~text
scheduled wake
-> current-field reentry
-> effect freshness / authority / duplicate / native-rule preflight
-> execute | requalify | wait | no_action
-> receipt
-> consequence
~~~

## Generalization boundary

This relation does not require one universal queue schema or scheduler.

It is a semantic invariant:

> **A later current determination can invalidate an earlier executable
> projection without rewriting the earlier occurrence.**

This is compatible with posts, replies, DMs, publication queues, campaigns,
browser handoffs and other social/public effect carriers.

## Source exercise

The relation was exposed in K-Social on 2026-10-03:

- E01 Reddit was initially execution-ready;
- later public-field readback showed independent semantic overlap;
- E01 was requalified to `DO_NOT_POST_AS_QUEUED`;
- the older Codex/browser packet still instructed E01 to execute first;
- a fresh MAIOS ChatGPT Adapter 0.2.1 receiver detected the contradiction before
  mutation.

The learning is generalized here; K-Social keeps the private occurrence.
