# 05: 失败票保留完整现场，成功票才清理

**What to build:** 用户接手 blocked ticket 时能拿到未提交修改、分支与日志；成功 ticket 可以安全清理。

**Blocked by:** 02

**Status:** ready-for-agent

Priority: P1 · 审查发现 2
Spec decisions: D6
User stories: US8

## Context

先读父目录的 spec 与执行索引。本票包含执行所需的行为决定；若现场与基线不同，核对当前实现后记录差异，不默默改变本票目标。

## Scope

Implement loop 的 FAIL/PASS 路径、worker retry 起点、两个 Runtime adapters 的 Cleanup。

本票不修改 plexus、全局配置或上游 companion；不启动其他票、不 push、不发布。仅当批次已批准、本票为 ready-for-agent 且 blockers 全部 done 时才可执行。

## Steps

1. 将 blocked 默认动作改为保留完整 worktree 与 branch，并在 brief 指出路径和 dirty 状态。
2. 只有已合并、clean、无活跃 agent 且属于本 run 的 worktree 才允许删除。
3. 取消 worker 起点的无条件 hard reset；新建与恢复分别核对基点，不销毁旧 attempt。
4. 清理失败记 warning 并继续交付 brief；保留集成 worktree。

## Examples

| Input / situation | Expected observable result |
| --- | --- |
| worker 修改 tracked 文件并新增 untracked 文件后 STUCK | 两个文件、branch 和 worktree 均保留，brief 有路径。 |
| 票已合并且 clean，无存活 agent | 删除票 worktree 和已合并票 branch；保留集成 worktree。 |
| 仍有 active agent，或路径不属于本 run | 不执行删除。 |
| Git 删除命令失败 | 报告 cleanup warning，不使用 --force，不丢失最终结果。 |

## Acceptance criteria

- [ ] blocked 不再要求删除 worktree。
- [ ] 未提交 tracked/untracked 修改都有保全规则。
- [ ] 清理前所有权、活动状态、merged 和 clean 条件缺一不可。
- [ ] 重试/恢复不再使用无条件破坏性 reset。

## Verify

在临时 Git 仓库创建 dirty blocked 和 clean merged 两个 worktree，分别执行允许的操作并核对内容/refs。证明保留 branch 不等于保存 dirty 修改。

交付时列出修改范围、逐项验收结果、实际运行命令/退出码和未验证项。对仓库编辑运行 `git diff --check`，并检查新增文件；此命令不替代行为验证。

## Completion

验收项全部满足且证据可重现后才改为 done。有环境或设计阻碍则改为 blocked，并写明原因、现场和下一步所需条件。未取得真实模型证据时，不使用“端到端通过”的表述。

## Comments

- 2026-10-13：根据架构审查编写；尚未实现，待批次确认。
- 2026-10-13：用户授权架构师决策，批次已定稿；状态改为 ready-for-agent。仍须等待执行指令，且只在前置票全部 done 后执行。
