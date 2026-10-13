# Ticket 03: companion-set protocol rehearsal

Scope: D4 companion discovery and semantic overrides. The product is a Markdown protocol. These are manually evaluated installation layouts and read-only source observations, not tests of an automatic resolver or claims of upstream-version/runtime compatibility.

## Reproduce the four layouts

From the repository root:

```sh
python3 docs/verification/reliability-hardening/03/layouts.py > /tmp/grill-autopilot-03-layouts.log
git diff --check
```

Both commands returned **0** on 2026-10-13. The fixture construction command was run before and after the doc change. [layouts.py](layouts.py) builds four fresh temporary layouts, logs writes, inventories file hashes and runs real Git commands for the drift case. It does not read product docs, classify/choose candidates, match documentation text or emit resolver verdicts. [layouts.log](layouts.log) preserves the actual facts and command exit codes; temporary paths and the synthetic source commit vary between runs.

Synthetic skill bodies are layout-only payloads, not copied upstream skills. For the ambiguity and resume decision walkthroughs their semantic eligibility is stipulated; real preparation must read actual templates and steps. The manual conclusions below were made by the ticket executor using [companions.md](../../../../skills/grill-autopilot/companions.md).

| Layout facts inspected | Manual protocol decision and resulting boundary |
| --- | --- |
| `split/project/plugin-a/skills` has only grilling/to-spec/to-tickets; plugin-b has the other three and relevant helpers. No other tier has a candidate. | Neither root is complete. Report the missing companions per root, reject stitching and stop preparation before Go. No collection selected. |
| `missing/project/plugin/skills` contains all six entries plus TDD/triage helpers, but lacks `setup-matt-pocock-skills/issue-tracker-local.md`. No fallback candidate exists. | Reject the root for the missing local-tracker helper, report its path and stop before Go. Six names alone do not qualify it. |
| Two project plugin roots each contain the full stipulated inventory; `grilling/SKILL.md` has hashes `46e19fc2…` and `fc080a60…`. They occupy the same highest eligible tier. | Display both canonical roots and content fingerprints and require a user choice before Go. Rehearsal ends at the unresolved choice; no selection or user approval is invented, and no version/cache ordering breaks the tie. |
| Selected user root is committed; modifying `tdd/tests.md` leaves HEAD unchanged but changes its hash from `e0148cb0…` to `947db367…`. `git status --short` reports the modification. Frozen spec/task hashes remain identical. | Reject resume on helper-content drift even though the commit agrees. Preserve the selected manifest, changed installation content and input snapshots; do not reset/rebaseline or silently switch a collection. No resumed operation is performed. |

Discovery priority was checked as a document contract: adjacent, then project, then user; all candidates in the selected tier are inspected before choosing. Incomplete/incompatible higher-tier candidates are recorded and cannot donate files to a lower-tier collection. The four required layouts exercise rejection, same-tier choice and selected-set drift; they do not empirically test host plugin discovery or symlink aliases.

## Read-only inspection of an installed set

The supplied `/Users/tyrion/.config/plexus/personal/skills` collection was read without editing it. The executor read all six skill bodies, the local tracker/triage helper and TDD references. [inspected-source.log](inspected-source.log) records ten canonical paths and SHA-256 hashes. `git -C <root> rev-parse HEAD` returned **128** because the installed directory has no Git metadata; provenance is recorded as unavailable, not inferred from its folder name. The file/hash capture returned **0**.

Semantic observations from those actual bodies:

- to-spec has a seam-confirmation operation and the seven required spec sections. The override maps to that operation's purpose.
- to-tickets requests human approval of granularity and blocking edges, and supplies a local per-ticket template. That semantic approval maps to the autopilot self-check; its numeric position is irrelevant.
- TDD requires agreed seams and red before green, and points to `tests.md`/`mocking.md`. Its interface-design branch references an additional skill conditionally; the current already-agreed seam does not activate that branch. A future active branch must qualify its dependency inside the chosen collection before use.
- The local tracker helper defines per-ticket files, Status and Comments and references the triage mapping. Other setup templates concern inactive tracker/setup branches, so this inspection does not invoke setup or edit configuration.
- Grilling uses prerequisite-aware rounds; code-review has separate Standards and Spec axes and accepts a fixed point/spec source. These were read as contract evidence, without invoking either workflow.

The product now retains commit provenance when available **and** actual content hashes, records canonical skill/helper paths and semantic evidence, and preserves the saved selection on resume drift. `run-record.md` exposes those fields through its companion section; `SKILL.md` and the ticket self-check locate overrides by purpose. Product and evidence files were inspected, local links resolve, and `git diff --check` passes. These are supplementary document checks, not product automation tests.

## Limits

No real model run, installed-plugin search, ambiguity UI, alias/symlink behavior or recovery operation was executed. The supplied set's current semantics were inspected, but arbitrary upstream versions were not certified. Source files, global/plexus configuration, tracker/spec/index and other tickets were not edited. The construction script removes only its own temporary fixtures after recording observations.
