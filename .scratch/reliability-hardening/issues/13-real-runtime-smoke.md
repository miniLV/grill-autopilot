# 13: 取得一次真实成功、失败保留和恢复的证据

**What to build:** 在一个实际可用且获授权的runtime上证明完整入口可跑，并如实记录失败和恢复能力。

**Blocked by:** 08, 12

**Status:** ready-for-agent

Priority: P1 · 发布前验证，不是benchmark
Spec decisions: D12
User stories: US19

## Context

先读父目录的 spec 与执行索引。本票包含执行所需的行为决定；若现场与基线不同，核对当前实现后记录差异，不默默改变本票目标。

## Scope

独立临时fixture仓库、仓库内的验证报告、README的验证矩阵。仅使用已经修复的skill；不借试运行修改其他功能。

本票不修改 plexus、全局配置或上游 companion；不启动其他票、不 push、不发布。仅当批次已批准、本票为 ready-for-agent 且 blockers 全部 done 时才可执行。

## Steps

1. 准备Python标准库fixture：独立normalize_name与parse_limit两票，render_message第三票依赖前两票；提供unittest和typecheck N/A理由。
2. 用用户执行阶段选定的runtime/角色配置，从skill实际入口跑成功样本，记录版本、模型事实、命令、refs与brief。
3. 在新的run做受控失败：保留dirty tracked/untracked后终止/拒绝一个attempt；用明确的测试配置缩短timeout和重试预算，验证blocked与证据保存。
4. 在另一个run中断planner后执行显式resume，核对没有重复派发/merge；记录全部证据并仅更新有依据的runtime状态。

## Examples

| Input / situation | Expected observable result |
| --- | --- |
| normalize_name输入" Ada "，parse_limit输入"0" | 分别输出"Ada"与0；parse_limit输入"x"产生ValueError；render_message(" Ada ","2")输出"Ada:2"。 |
| 两个前置票完成，第三票依赖它们 | 第三票只在两者done后开始；最终结果success且base未变。 |
| 故障run留有dirty文件，重试预算用尽 | ticket blocked，两个文件仍在，brief含现场路径且不push。 |
| 已完成merge后中断、恢复 | 通过SHA与验证证据核对，不重复merge；状态和brief一致。 |
| 环境、模型或取消能力不足 | 此票blocked，提交证据和缺口，不伪造完整验证通过。 |

## Acceptance criteria

- [ ] 成功、失败和恢复各有独立run身份与真实日志。
- [ ] 报告区分Git实验、协议演练与实际模型执行。
- [ ] 实际模型不可观测字段为unknown，不声称匹配已验证。
- [ ] 验证矩阵仅据证据更新；未验证runtime仍标未验证。
- [ ] 成本/耗时只记录能拿到的真实数据，无比较收益结论；不push/PR/发布。

## Verify

运行fixture的Python unittest；核对所有run的ref、worktree、dirty内容、attempt记录、最终SHA review和brief。执行过程产生的新缺陷记录为后续票并阻塞本票，不扩展本票做无界修复。

交付时列出修改范围、逐项验收结果、实际运行命令/退出码和未验证项。对仓库编辑运行 `git diff --check`，并检查新增文件；此命令不替代行为验证。

## Completion

验收项全部满足且证据可重现后才改为 done。有环境或设计阻碍则改为 blocked，并写明原因、现场和下一步所需条件。未取得真实模型证据时，不使用“端到端通过”的表述。

## Comments

- 2026-10-13：根据架构审查编写；尚未实现，待批次确认。
- 2026-10-13：用户授权架构师决策，批次已定稿；状态改为 ready-for-agent。仍须等待执行指令，且只在前置票全部 done 后执行。
