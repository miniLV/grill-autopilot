# 10: 最终修复必须复审，最终tip才决定交付

**What to build:** 用户拿到的最终提交既通过测试也通过review；修复超限时明确failed而非宣称完成。

**Blocked by:** 09

**Status:** ready-for-agent

Priority: P1 · 审查发现 3
Spec decisions: D10
User stories: US15, US16

## Context

先读父目录的 spec 与执行索引。本票包含执行所需的行为决定；若现场与基线不同，核对当前实现后记录差异，不默默改变本票目标。

## Scope

主 skill 的Final review、完成条件与PR brief，配置中的final_review重试。

本票不修改 plexus、全局配置或上游 companion；不启动其他票、不 push、不发布。仅当批次已批准、本票为 ready-for-agent 且 blockers 全部 done 时才可执行。

## Steps

1. 加入retry.final_review=2，表示最多两轮最终修复，不含最初审查。
2. 无findings时直接验证证据；有findings才交escalate修复，每次修复后跑suite/typecheck并复审新SHA。
3. 将最终verdict和测试证据绑定integration tip，代码变化使旧证据失效。
4. 预算耗尽仍有findings或红色检查则failed；known blocked范围独立列明，其他spec偏离仍算finding。

## Examples

| Input / situation | Expected observable result |
| --- | --- |
| 首次最终review无findings，suite绿 | 0次修复，最终SHA有效，可按全部票状态判success/partial。 |
| 修复让测试绿但删弱断言 | 复审拒绝，不能只凭绿测试交付。 |
| 两轮修复后仍有finding | 停止修复，failed brief列出剩余项。 |
| 最终PASS之后tip变化 | 旧PASS失效，新tip需验证和review。 |

## Acceptance criteria

- [ ] 每次最终修复都复审，不再存在审后直接交付路径。
- [ ] 修复预算为有限的2轮，准确计数。
- [ ] 最终tip与review/test证据一致。
- [ ] 未解决项与blocked范围在brief清楚区分。

## Verify

以四个例子逐步列出SHA、修复次数、suite状态和verdict，核对流程能给唯一终态；真实审查行为由试运行补证。

交付时列出修改范围、逐项验收结果、实际运行命令/退出码和未验证项。对仓库编辑运行 `git diff --check`，并检查新增文件；此命令不替代行为验证。

## Completion

验收项全部满足且证据可重现后才改为 done。有环境或设计阻碍则改为 blocked，并写明原因、现场和下一步所需条件。未取得真实模型证据时，不使用“端到端通过”的表述。

## Comments

- 2026-10-13：根据架构审查编写；尚未实现，待批次确认。
- 2026-10-13：用户授权架构师决策，批次已定稿；状态改为 ready-for-agent。仍须等待执行指令，且只在前置票全部 done 后执行。
