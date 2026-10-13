# Worker-grade tickets

A ticket is **worker-grade** when the cheapest configured model can finish it from the ticket alone, with no design decision left to make. to-tickets' vertical-slice rules still hold; a worker-grade ticket is a thin slice with every decision written down.

## Rules

- **One behaviour, one seam.** Aim for at most 3 production files plus their test file as a size heuristic. Keep a complete, independently verifiable behavior together even if it needs more files; split only into independently verifiable slices. Resolve design decisions in the spec before dispatch. An unresolved decision blocks ticket preparation; return to the spec under run-record.md's scope-change gate rather than assigning the choice to a worker.
- **Files** lists every path the worker may create or edit. The scheduler uses it to keep parallel workers apart, and the reviewer rejects any change outside it, so make it complete.
- **Source** maps approved spec user stories and acceptance items to this ticket's acceptance IDs. If the spec lacks IDs, use a section pointer plus the exact criterion. Keep a set-level coverage table: every approved story and acceptance item → delivering ticket/acceptance IDs, or an explicit exclusion already approved in the spec with its pointer. A ticket-local exclusion cannot drop an in-scope requirement.
- **Blocked by** names business prerequisites: if B needs an interface, artifact or behavior delivered by A, record A on B even when their Files are disjoint. Files overlap is a separate scheduling constraint; disjoint files alone do not make tickets independent.
- **Interface** names the exact signature, endpoint, or CLI shape the slice adds or changes.
- **Examples** name acceptance IDs and give concrete inputs with literal expected observable results, at least one per acceptance item plus one edge case, covering applicable boundary and error inputs too (values, error messages, exit codes or state changes). Explain any inapplicable input class. They are the independent source of truth: the worker's behavior checks assert them, and the reviewer checks the evidence against them.
- **Steps** are at most 5 imperative actions. Words such as "decide", "choose" or "design" mean the ticket is not worker-grade yet.
- **Verify** gives the exact single-test-file command and typecheck command from grill (or its agreed N/A reason). If the new test file does not yet exist, record the agreed existing seam baseline used before implementation.
- **Context** holds pointers only: the spec section, plus 1–3 existing files to imitate.
- Write real paths. Tickets run right away, so paths do not go stale; this replaces to-tickets' "avoid file paths" rule.

## Self-check

This replaces to-tickets' human approval of ticket granularity and blocking edges, located by meaning rather than step number (see [companions.md](companions.md)). Check the whole set and every ticket, record failures, fix them and repeat. Publish the set as ready-for-agent only when all checks pass:

- [ ] Every template field is filled.
- [ ] The coverage table accounts for every approved spec user story **and** acceptance item; each delivery mapping names an existing ticket and acceptance ID. Every ticket Source mapping agrees with it. Only spec-approved exclusions pass; missing or unexplained coverage fails the set.
- [ ] Every acceptance ID has at least one linked concrete input and literal observable expectation, plus at least one edge case for the ticket; applicable error and boundary inputs are covered, or their inapplicability is explained. Vague results such as “works normally” fail.
- [ ] No step asks the worker to decide something.
- [ ] Every path the slice touches is in Files.
- [ ] Every required interface/artifact/behavior is already available at the agreed baseline or supplied by a named Blocked-by ticket. Check this independently of Files overlap; separately keep overlapping writers apart during scheduling.
- [ ] Every Blocked-by ID exists and the graph is acyclic, including self-dependencies. Report missing IDs or the cycle's ticket chain; correct the graph before readiness. A genuine prerequisite cycle needs a settled spec/slice change, not removal of a required edge to pass the check.

## Template

```markdown
# <NN>: <Ticket title>

Status: ready-for-agent
Blocked by: <NN, NN> | None
Files:
  - <path>
Source: <spec story/acceptance IDs or exact criterion pointers> → <AC1, AC2>
Interface: <signature / endpoint / CLI shape>
Examples:
  - AC1: <concrete input> → <literal observable result>
  - AC1: <boundary/error input> → <literal result, or reason inapplicable>
Steps:
  1. <imperative action>
Verify:
  - <single-test-file command>
  - <typecheck command or agreed N/A with reason>
Context: spec.md#<section>; prior art: <path>
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC1: <criterion>

## Comments
```
