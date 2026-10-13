# 06: runtime 能力、角色事实与 agent 容量明确

**What to build:** planner 可以在宿主容量和授权内启动、观察并释放所有角色；实际选模无法验证时不假报成功。

**Blocked by:** 02

**Status:** done

Priority: P2 · 审查发现 7
Spec decisions: D7
User stories: US9, US10

## Context

先读父目录的 spec 与执行索引。本票包含执行所需的行为决定；若现场与基线不同，核对当前实现后记录差异，不默默改变本票目标。

## Scope

Runtime adapters 的公共说明和两种宿主实现、主 skill 的角色准备与模型 guardrail、配置说明。

本票不修改 plexus、全局配置或上游 companion；不启动其他票、不 push、不发布。仅当批次已批准、本票为 ready-for-agent 且 blockers 全部 done 时才可执行。

## Steps

1. 定义 adapter 能力报告及 start/read-result/is-alive/cancel/release 的宿主操作语义，逐项说明不支持时的出口。
2. 记录请求角色与观察角色，区分 match、mismatch、unknown；planner 保持当前模型并显示差异。
3. 区分能力缺失与策略拒绝，只对被允许的缺能力路径使用 CLI fallback。
4. 按所有 child roles 计算 slots；结束 worker 先释放，再优先 review；容量未知时从单 child 起步。

## Examples

| Input / situation | Expected observable result |
| --- | --- |
| 宿主只有 3 个 child slots，3 个 worker 在跑，其中一个结束 | 释放该 worker slot，reviewer 可以启动，不先补第 4 个 worker。 |
| spawn 因上层路由策略拒绝 | 报告不可用，不尝试 CLI 绕过。 |
| 实际模型与配置不同 | 该角色不继续；记录 requested/actual。 |
| 宿主无法提供 actual model | 记录 unknown，Go 前披露，不填写成配置值。 |

## Acceptance criteria

- [x] 两个 runtime 使用相同的能力与结果语义。
- [x] 有界等待、取消不支持与资源释放有明确出口。
- [x] 容量管理包含 reviewer/escalate，拒绝时不会无限 spawn。
- [x] 模型差异与未知项不被隐藏。

## Verify

核对当前宿主实际工具 schema 或 CLI help，记录版本与支持能力；再按四个例子演练。只读检查不算真实模型 dispatch 成功，不能临时启动未经授权的替代模型。

交付时列出修改范围、逐项验收结果、实际运行命令/退出码和未验证项。对仓库编辑运行 `git diff --check`，并检查新增文件；此命令不替代行为验证。

## Completion

验收项全部满足且证据可重现后才改为 done。有环境或设计阻碍则改为 blocked，并写明原因、现场和下一步所需条件。未取得真实模型证据时，不使用“端到端通过”的表述。

## Comments

- 2026-10-13：根据架构审查编写；尚未实现，待批次确认。
- 2026-10-13：用户授权架构师决策，批次已定稿；状态改为 ready-for-agent。仍须等待执行指令，且只在前置票全部 done 后执行。

- 2026-10-14：gpt-6.1-sol/high 候选 ce4f188，集成 000100f。root 核对 schema、四例 D7 协议演练及初始化计时修正通过；worker/root/merger 九条版本/help 命令全部 exit 0，diff check 通过。证据：docs/verification/reliability-hardening/06/README.md。实际模型/effort unknown，slot 释放、取消与 CLI 模型运行未验证。
