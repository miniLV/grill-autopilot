# Worker-grade tickets

A ticket is **worker-grade** when the cheapest configured model can finish it from the ticket alone, with no design decision left to make. to-tickets' vertical-slice rules still hold; a worker-grade ticket is a thin slice with every decision written down.

## Rules

- **One behaviour, one seam.** Aim for at most 3 production files plus their test file. More tickets is fine. A ticket that needs a judgement call is not: split it, or move the decision into the spec.
- **Files** lists every path the worker may create or edit. The scheduler uses it to keep parallel workers apart, and the reviewer rejects any change outside it, so make it complete.
- **Interface** names the exact signature, endpoint, or CLI shape the slice adds or changes.
- **Examples** give concrete inputs and the literal expected outputs, at least one per acceptance item plus one edge case. They are the independent source of truth: the worker's tests assert them, and the reviewer checks the tests against them.
- **Steps** are at most 5 imperative actions. Words such as "decide", "choose" or "design" mean the ticket is not worker-grade yet.
- **Verify** gives the exact single-test-file command and the typecheck command from the grill.
- **Context** holds pointers only: the spec section, plus 1–3 existing files to imitate.
- Write real paths. Tickets run right away, so paths do not go stale; this replaces to-tickets' "avoid file paths" rule.

## Self-check

This replaces to-tickets' user quiz. Check every ticket, fix what fails, and repeat until all pass:

- [ ] Every template field is filled.
- [ ] Every acceptance item has at least one example with literal values.
- [ ] No step asks the worker to decide something.
- [ ] Every path the slice touches is in Files.
- [ ] The Blocked-by graph has no cycle, and every ticket it names exists.

## Template

```markdown
# <NN>: <Ticket title>

Status: ready-for-agent
Blocked by: <NN, NN> | None
Files:
  - <path>
Interface: <signature / endpoint / CLI shape>
Examples:
  - <input> → <expected output>
Steps:
  1. <imperative action>
Verify:
  - <single-test-file command>
  - <typecheck command>
Context: spec.md#<section>; prior art: <path>
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] <criterion>

## Comments
```
