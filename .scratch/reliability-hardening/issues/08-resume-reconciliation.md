# 08: 恢复运行不会重复派发或覆盖现场

**What to build:** 主会话中断后，重新启动可以核对已有工作，继续或安全停止，而不是重做和覆盖。

**Blocked by:** 07

**Status:** done

Priority: P1 · 审查发现 4 的恢复分支
Spec decisions: D8
User stories: US12

## Context

先读父目录的 spec 与执行索引。本票包含执行所需的行为决定；若现场与基线不同，核对当前实现后记录差异，不默默改变本票目标。

## Scope

主 skill 的启动/恢复入口、Implement loop 的状态核对参考，沿用 run record 与 runtime 生命周期。

本票不修改 plexus、全局配置或上游 companion；不启动其他票、不 push、不发布。仅当批次已批准、本票为 ready-for-agent 且 blockers 全部 done 时才可执行。

## Steps

1. 增加显式 resume 入口，读取 run ID 后先核对宿主进程、worktree、分支和提交祖先关系。
2. 已有活跃 attempt 继续观察，不重复派发；已合并但未更新状态时按证据补记。
3. 缺验证证据时重跑检查；状态矛盾或所有权不明则保存 failed brief 并保留现场。
4. 明确主进程崩溃时无法即时写 brief；下一次恢复先记录中断，不承诺后台自动续跑。

## Examples

| Input / situation | Expected observable result |
| --- | --- |
| 状态claimed，宿主同一agent仍运行 | 不创建新worker，继续观察原agent。 |
| 候选已合并，测试证据匹配SHA，但状态仍in-review | 补记done，不再次merge。 |
| 候选已合并但没有测试证据 | 先验证，不直接done。 |
| 记录branch SHA与现场不同且无法解释 | failed brief；不reset、不删除、不重新派发。 |

## Acceptance criteria

- [x] resume 只复用同一run身份，核对事实先于任何写操作。
- [x] 活跃、已合并、证据缺失与矛盾四种场景都有明确结果。
- [x] 中断后的保障范围与文档一致。

## Verify

用临时Git仓库构造已合并未记状态场景，检查祖先关系与证据匹配；宿主存活场景做有标记的协议演练。真实取消/恢复留给最终验收。

交付时列出修改范围、逐项验收结果、实际运行命令/退出码和未验证项。对仓库编辑运行 `git diff --check`，并检查新增文件；此命令不替代行为验证。

## Completion

验收项全部满足且证据可重现后才改为 done。有环境或设计阻碍则改为 blocked，并写明原因、现场和下一步所需条件。未取得真实模型证据时，不使用“端到端通过”的表述。

## Comments

- 2026-10-13：根据架构审查编写；尚未实现，待批次确认。
- 2026-10-13：用户授权架构师决策，批次已定稿；状态改为 ready-for-agent。仍须等待执行指令，且只在前置票全部 done 后执行。

- 2026-10-14：gpt-6.1-sol/high 候选 58242a3，集成 774f525。worker/root/merger 四个真实 Git 恢复证据场景 exit 0，D8 协议核对及 diff check 通过。证据：docs/verification/reliability-hardening/08/README.md。宿主活动、状态补记和 brief 为手动演练，真实中断/恢复仍待 13。
