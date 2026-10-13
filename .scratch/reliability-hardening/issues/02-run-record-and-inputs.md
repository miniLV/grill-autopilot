# 02: 独立 worktree 能读取稳定输入并留下可恢复记录

**What to build:** worker/reviewer 从任意工作目录读取已确认的 spec/ticket；用户可找到唯一的运行状态和证据。

**Blocked by:** 01

**Status:** ready-for-agent

Priority: P2 · 审查发现 5
Spec decisions: D3
User stories: US3, US4, US12

## Context

先读父目录的 spec 与执行索引。本票包含执行所需的行为决定；若现场与基线不同，核对当前实现后记录差异，不默默改变本票目标。

## Scope

主 skill 的 spec/ticket/brief 步骤、Implement loop 的 Setup 与两个 packet。使用现有本地 tracker 作为资料位置。

本票不修改 plexus、全局配置或上游 companion；不启动其他票、不 push、不发布。仅当批次已批准、本票为 ready-for-agent 且 blockers 全部 done 时才可执行。

## Steps

1. 定义 planner 独占写入的 run record 与每票事件字段，采用 spec D3 的最小字段集合。
2. packet 中所有文件位置传 canonical 绝对路径；先保存 spec 与 ticket 任务正文的只读快照；packet 指向快照，Status/Comments 留在可变 tracker。
3. 记录原 checkout 的 ref、tracked diff 和非本 run 所有的 untracked 文件基线。
4. 明确只允许在原 checkout 写本 run 的 tracker 资料，产品修改均在专用 worktree；同步相关安全说明。

## Examples

| Input / situation | Expected observable result |
| --- | --- |
| 原 checkout 有未提交运行资料，worker worktree 不含这些文件 | 使用 packet 的绝对路径能读取；不要求把资料提交到 base。 |
| 从两个不同 worktree 启动 reader | 读到同一份 spec/ticket 快照，且内容 hash 相同。 |
| 运行前原 checkout 有不属于本 run 的 untracked 文件 | 不修改、不删除；结束核对仍存在且内容不变。 |
| 实现中发现需要扩大 scope | 记录原因并 block，不修改已经分发的 spec/ticket 题目。 |

## Acceptance criteria

- [ ] run record 包含 D3 所列身份、配置、路径、SHA 和尝试证据字段。
- [ ] 两个 packet 不再依赖当前工作目录解析输入。
- [ ] 源输入不可变、planner 单写状态的职责明确。
- [ ] 用户源代码、base ref 和非运行资料保持不变。

## Verify

临时 Git 仓库建立两个 worktree，验证相对文件缺失但 canonical 指针可读，并比较 hash 与原 checkout 状态。按字段清单审查一份示例 run record。

交付时列出修改范围、逐项验收结果、实际运行命令/退出码和未验证项。对仓库编辑运行 `git diff --check`，并检查新增文件；此命令不替代行为验证。

## Completion

验收项全部满足且证据可重现后才改为 done。有环境或设计阻碍则改为 blocked，并写明原因、现场和下一步所需条件。未取得真实模型证据时，不使用“端到端通过”的表述。

## Comments

- 2026-10-13：根据架构审查编写；尚未实现，待批次确认。
- 2026-10-13：用户授权架构师决策，批次已定稿；状态改为 ready-for-agent。仍须等待执行指令，且只在前置票全部 done 后执行。
