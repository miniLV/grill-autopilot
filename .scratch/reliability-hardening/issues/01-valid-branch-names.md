# 01: 默认分支可以创建，已有现场不会被覆盖

**What to build:** 用户采用默认配置时，可以创建集成与 ticket worktree；重复运行遇到已有 ref 时安全停止。

**Blocked by:** None (can start when execution is requested)

**Status:** done

Priority: P1 · 审查发现 1
Spec decisions: D2
User stories: US1, US2

## Context

先读父目录的 spec 与执行索引。本票包含执行所需的行为决定；若现场与基线不同，核对当前实现后记录差异，不默默改变本票目标。

## Scope

主 skill 的 Delivery 与准备步骤、Implement loop 的 Setup、两个 Runtime adapters 的分支创建/清理说明。README 的对应分支示例同步修正。

本票不修改 plexus、全局配置或上游 companion；不启动其他票、不 push、不发布。仅当批次已批准、本票为 ready-for-agent 且 blockers 全部 done 时才可执行。

## Steps

1. 统一默认集成 ref 为 autopilot/<slug>/integration，ticket ref 为 autopilot/<slug>/tickets/<NN>。
2. 创建前检查 base commit、Git ref 合法性、ref 前缀冲突和现存 worktree/ref；保存 base SHA。
3. 已有现场只能由显式恢复处理；普通新运行报告冲突，不 reset、不删除。
4. 新增一份可复现的临时 Git 实验记录，证明默认命名可用。

## Examples

| Input / situation | Expected observable result |
| --- | --- |
| slug=demo，干净且已有 base commit | 创建 integration、tickets/01、tickets/02 均成功；base SHA 不变。 |
| 已存在旧式 autopilot/demo ref | 创建前报告冲突；旧 ref SHA 与文件内容不变。 |
| base 不存在，或 slug 含 Git 不允许的字符 | 没有创建任何 worktree 或 branch。 |

## Acceptance criteria

- [x] 默认命名在所有创建/清理示例一致。
- [x] 三个默认 ref 可同时存在，base ref 未变化。
- [x] 无效 base/ref 和已存在现场有明确的无修改失败出口。

## Verify

在独立临时 Git 仓库逐项运行上述例子，记录命令、退出码、ref 列表及前后 base SHA。检查修复涉及的全文示例；不把文档匹配当产品测试。

交付时列出修改范围、逐项验收结果、实际运行命令/退出码和未验证项。对仓库编辑运行 `git diff --check`，并检查新增文件；此命令不替代行为验证。

## Completion

验收项全部满足且证据可重现后才改为 done。有环境或设计阻碍则改为 blocked，并写明原因、现场和下一步所需条件。未取得真实模型证据时，不使用“端到端通过”的表述。

## Comments

- 2026-10-13：根据架构审查编写；尚未实现，待批次确认。
- 2026-10-13：用户授权架构师决策，批次已定稿；状态改为 ready-for-agent。仍须等待执行指令，且只在前置票全部 done 后执行。

- 2026-10-13：本次 implement-spec 执行已授权，使用 gpt-6.1-sol/high；候选 6664d5b，集成 b15a68e。临时 Git 实验由 worker、root 与 merger 各运行成功（exit 0），diff check 通过。证据：docs/verification/reliability-hardening/01/README.md。属于 Git 实验与协议演练，未称完整 runtime 验证。
