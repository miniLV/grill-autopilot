# 04: 新 worktree 测试前有环境准备与绿色基线

**What to build:** worker 开始实现前获得能运行测试的环境；缺依赖或原始失败不会消耗实现重试次数。

**Blocked by:** 02

**Status:** done

Priority: P2 · 审查发现 6
Spec decisions: D5
User stories: US7

## Context

先读父目录的 spec 与执行索引。本票包含执行所需的行为决定；若现场与基线不同，核对当前实现后记录差异，不默默改变本票目标。

## Scope

主 skill 的 Commands 澄清、Implement loop 的集成/worker 准备步骤、worker packet。

本票不修改 plexus、全局配置或上游 companion；不启动其他票、不 push、不发布。仅当批次已批准、本票为 ready-for-agent 且 blockers 全部 done 时才可执行。

## Steps

1. 增加初始化命令的确认，允许显式 None；约定不适用检查需写 N/A 和理由。
2. 集成和 ticket worktree 各自完成初始化与本阶段基线检查，再开始实现。
3. 区分安装已有 lockfile 与改变依赖声明，后者仍需 ticket 授权。
4. 基线红色、凭据缺失和初始化失败写成环境错误，交由运行失败路径处理。

## Examples

| Input / situation | Expected observable result |
| --- | --- |
| 原 checkout 有 ignored 依赖，新 worktree 没有 | 在初始化完成前不进入 TDD。 |
| 初始化命令退出 7 | 记录命令、退出 7、环境错误；worker 实现次数保持 0。 |
| 初始化成功，原始测试仍红色 | 不要求 worker 修改业务代码，保留错误证据。 |
| 仅使用 Python 标准库 fixture，typecheck 不适用 | 记录 N/A 及理由，行为测试仍必须运行。 |

## Acceptance criteria

- [x] Commands 包含初始化、单票检查、full suite 与 typecheck/N/A 的明确选择。
- [x] 两个种类 worktree 都有初始化和基线门槛。
- [x] 环境失败不计为实现失败，且有证据可交接。

## Verify

使用一个初始化前失败、初始化后成功的临时命令，以及退出 7 的初始化命令演练。记录状态和次数；不要创建真实凭据或联网安装无关依赖。

交付时列出修改范围、逐项验收结果、实际运行命令/退出码和未验证项。对仓库编辑运行 `git diff --check`，并检查新增文件；此命令不替代行为验证。

## Completion

验收项全部满足且证据可重现后才改为 done。有环境或设计阻碍则改为 blocked，并写明原因、现场和下一步所需条件。未取得真实模型证据时，不使用“端到端通过”的表述。

## Comments

- 2026-10-13：根据架构审查编写；尚未实现，待批次确认。
- 2026-10-13：用户授权架构师决策，批次已定稿；状态改为 ready-for-agent。仍须等待执行指令，且只在前置票全部 done 后执行。

- 2026-10-14：gpt-6.1-sol/high 候选 1165333，集成 aac7199。worker/root/merger 的真实 Git/命令初始化实验 exit 0，D5 协议审查与 diff check 通过。证据：docs/verification/reliability-hardening/04/README.md。计数/None/N/A 为明确标记的 planner 演练，真实 runtime 处理尚未验证。
