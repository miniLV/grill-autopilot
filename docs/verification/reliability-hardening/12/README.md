# Ticket 12: installation, claims and diagram evidence

Client date: 2026-10-14 Asia/Shanghai. Clean starting HEAD and integration were `1aa984e1c577f805441d287e6445b4df23b876ed`; blockers 03/10/11 were done. Scope is README, the skill entry's description of bounded host execution, and this evidence directory. No tracker/spec/index, runtime adapter, defaults, global installation, plexus or companion source was edited.

The approved seam is skill inputs → external Git/worktree state, ticket state and brief. These checks exercise **real temporary installation operations** and manually audit document promises against the implemented protocol. They are not a full skill run, model smoke test or shadow scheduler.

## Installation: RED then GREEN

Before changing the installation example, `python3 docs/verification/reliability-hardening/12/verify.py` exited **1**: with a skill source present but no skills directory, the baseline `ln` failed with “No such file or directory”; [install-red.log](install-red.log) captures the failure. Only the baseline tilde paths were redirected to quoted fixture paths. The RED is the missing-directory behavior, not shell quoting or a prose assertion.

A separate baseline uninstall slice created one unrelated regular file in each fixture runtime directory, executed the old README `rm` with only its paths redirected, and observed exit **0** and **0 foreign files remaining**: [uninstall-red.log](uninstall-red.log). Expected behavior was refusal and preservation. This was performed before replacing the uninstall block; no real installation was touched.

After replacing the README install and uninstall blocks, the executable examples were rerun. The current [verify.py](verify.py) extracts the README's bash install/uninstall blocks and redirects only `autopilot_checkout` / `autopilot_skills` to a temporary `fixture_home` (including spaces). It never assigns `HOME`, `home` or `CODEX_HOME`. Run from the repository:

```bash
python3 docs/verification/reliability-hardening/12/verify.py
```

Exit **0**; [install-green.log](install-green.log) retains **28 real shell operations** across `.codex/skills` and `.claude/skills` (trailing whitespace normalized). Literal external observations:

| Input | Observed GREEN |
| --- | --- |
| Source present; skills directory absent | Directory created; target is the exact source symlink; exit 0. |
| Owned installed link; repeat install | Exit 0, same link and unchanged source directory inventory. |
| Owned link; uninstall then repeat uninstall | Link removed, source bytes retained; absent target is an exit-0 no-op. |
| Foreign file, directory, directory symlink or dangling foreign symlink | Both install and uninstall exit 1; original bytes, directory inventory and link target remain intact. |
| Owned dangling source link | Uninstall exits 0 and removes only that link. |
| Missing source | Install exits 1 and creates no target. |

Temporary fixtures are removed by `TemporaryDirectory`. Clone network access was **not** exercised: `git remote -v` independently reports `https://github.com/miniLV/grill-autopilot.git`, the source of the owner correction. Existing checkout handling is explicit in the README; no repeated clone or automatic update was run.

## Document contract: RED then GREEN audit

These are manual decisions against independent spec decisions D1/D11 and existing companion/runtime/failure/final-review/ticket contracts, not automated prose-string tests.

| Example / promise | Baseline RED | GREEN evidence and decision |
| --- | --- | --- |
| Only Git fixtures pass; no full model run | Experimental status still presented numerical savings and broad host availability. | README removes all five old PNG references and the unmeasured percentages/ratios/interaction comparison; one Mermaid and text tables qualify the available evidence. Historical PNG files are unchanged. Full run is explicitly pending ticket 13. |
| Original checkout / delivery | Tracker exception already present, but push required only prior selection; final summary skipped new-SHA review. | Tracker writes stay the manifest-owned exception under [run-record.md](../../../../skills/grill-autopilot/run-record.md); current-tip review/checks and success-only authorized push match [final-review.md](../../../../skills/grill-autopilot/final-review.md) and [failures.md](../../../../skills/grill-autopilot/failures.md). Partial/failed remain local. |
| Model request accepted without actual metadata | Role defaults and fallback wording could be read as actual routing guarantees. | Requested vs trusted observed/unknown, unchanged planner session, mismatch stop and rejection-not-capability-gap match [runtimes.md](../../../../skills/grill-autopilot/runtimes.md). Runtime matrix distinguishes native schema from read-only CLI help. |
| Claude has no native schema or real run evidence | “Both usable” with blanket Codex CLI fallback. | Claude native stays unverified; CLI syntax evidence does not verify model dispatch/lifecycle. Codex native schema/request acceptance is not full skill success. [Ticket 06 evidence](../06/README.md) is the independently captured source. |
| Timeout, unknown activity, interrupted session | “Leave after Go” and final-only review oversimplified stop behavior. | Finite attempt/retry/final-fix limits, unsafe-resource failed exit and explicit reconciliation on resume match failures/runtime/[resume.md](../../../../skills/grill-autopilot/resume.md). Skill entry now states crash/background limits. |
| Cost/token/cache/review/retry/timing data unavailable | Unit-price assumptions stood in for total savings. | README reports the full-run values as unknown, defines per-field evidence and requires a comparable measured baseline before savings/speed claims. |

## Actual Mermaid render and visual inspection

[flow.mmd](flow.mmd) is the evidence snapshot extracted from the README's sole Mermaid block, not another maintained product diagram. A temporary npm prefix under `/tmp/grill-autopilot-12-render-tools.*` installed **@mermaid-js/mermaid-cli 12.0.0** with `PUPPETEER_SKIP_DOWNLOAD=true` (exit **0**, 195 temporary packages). No repository package file, framework or production dependency was added. Rendering used the existing local Chrome executable and its temporary Puppeteer profile. The temporary `puppeteer.json` contains:

```json
{"executablePath":"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome","args":["--no-sandbox"]}
```

With `render_tools` pointing at that temporary prefix, executed commands were:

```bash
"$render_tools/node_modules/.bin/mmdc" -p "$render_tools/puppeteer.json" -i docs/verification/reliability-hardening/12/flow.mmd -o docs/verification/reliability-hardening/12/flow.svg -b white
"$render_tools/node_modules/.bin/mmdc" -p "$render_tools/puppeteer.json" -i docs/verification/reliability-hardening/12/flow.mmd -o /tmp/grill-autopilot-12-flow-preview.png -b white --size 1800
```

Both exited **0**. [flow.svg](flow.svg) is the actual rendered artifact; [render.log](render.log) retains output. The first PNG invocation used `-w 1800` and exited **1** with “unknown option '-w'”; inspecting this installed CLI's `--help` (exit **0**) corrected it to `--size 1800` above. This was a repaired tooling command, not a skipped preview.

The executor opened `/tmp/grill-autopilot-12-flow-preview.png` with `view_image`: Chinese/English labels, normal path, failure exits and final-fix loop are readable, with no clipping or overlapping nodes. The PNG is temporary visual evidence, not a redesign/replacement of the historical images. The unsafe-resource edge reaches brief directly; other remaining work reaches final review only when resources are safe. No root UI action was needed.

## Limits and closeout

Actual native model/effort remains **unknown**; this ticket made no new model/runtime calls. Costs, token/cache usage, model review/retry distribution and total full-run timing remain **unknown**. No end-to-end success/failure/resume, cross-runtime compatibility, performance or savings pass is claimed. The default budgets are configured protection values, not measured optimal values. No push, PR, publication or global settings change occurred.

`git diff --check` and independent local Markdown file-target checks supplement the operations/audit/render above. The parent independently reviews the candidate and reruns Verify after integration-tip merge; exact candidate/merge SHA and final check exits are returned to it separately so this evidence does not claim an unperformed integration.
