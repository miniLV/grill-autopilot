# Worker-grade tickets

Follow to-tickets as written. This file lists only where autopilot differs from it; to-tickets itself is never edited.

## Overrides

1. **No quiz.** Replace to-tickets' human approval of granularity and blocking edges with the [self-check](#self-check).
2. **Real paths.** Write `Files` and `Context` as real repo paths; this replaces "avoid file paths". The scheduler keeps tickets with overlapping Files apart, and the DONE check rejects changes outside them.
3. **Extra fields.** Use the [template](#template): it adds `Implementer`, `Files`, `Interface`, `Examples`, `Verify` and `Context`. Examples give literal inputs and expected results, at least one per acceptance item plus one edge case; the worker's tests assert them and the reviewer checks against them.

## Grading

Before the self-check, the planner sets each ticket's Implementer. A ticket goes to `worker` (cheap model) only when **all** of these hold:

- One module: at most 3 production files plus their test file.
- Interface and Examples are literal; nothing is left to decide.
- Context names at least one existing file in the repo to imitate.
- No concurrency, ordering, async timing or state shared across modules.
- Not a data migration, not a wide-refactor batch, not a bug fix without a reproduction.
- Not security, authorization or performance-sensitive code.

If an item fails, split the ticket along independently verifiable behaviours and grade each part again. Do not split below one behaviour just to reach `worker`: every ticket costs one reviewer call. If it cannot split further, set `escalate (<failed item>)` (strong model).

## Self-check

Check every ticket, fix what fails, and repeat until all pass:

- [ ] Every template field is filled; Verify uses the commands agreed in grill (or their agreed N/A reason).
- [ ] The Implementer matches Grading, and every `escalate` names the failed item.
- [ ] Every acceptance item has an Example with literal values.
- [ ] Every path the ticket touches is in Files.
- [ ] Nothing asks the implementer to decide; an open design decision goes back to the spec.

## Template

```markdown
# <NN>: <Ticket title>

Status: ready-for-agent
Blocked by: <NN, NN> | None
Implementer: worker | escalate (<failed grading item>)
Files:
  - <path>
Interface: <signature / endpoint / CLI shape>
Examples:
  - AC1: <concrete input> → <literal expected result>
  - AC1: <edge or error input> → <literal expected result>
Verify:
  - <single-test-file command>
  - <typecheck command or agreed N/A with reason>
Context: spec.md#<section>; prior art: <path>
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC1: <criterion>

## Comments
```
