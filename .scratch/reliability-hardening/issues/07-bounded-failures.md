# 07: 异常有重试上限，所有可处理终止都产出 brief

**What to build:** worker/reviewer 超时或异常时不会无限卡住；用户可以从 brief 判断成功、部分完成或失败。

**Blocked by:** 04, 05, 06

**Status:** done

Priority: P1 · 审查发现 4
Spec decisions: D7,D8
User stories: US11, US16

## Context

先读父目录的 spec 与执行索引。本票包含执行所需的行为决定；若现场与基线不同，核对当前实现后记录差异，不默默改变本票目标。

## Scope

Implement loop 的派发、review、FAIL 与结束规则，主 skill 各步骤完成条件与 brief，配置中的超时/重试。

本票不修改 plexus、全局配置或上游 companion；不启动其他票、不 push、不发布。仅当批次已批准、本票为 ready-for-agent 且 blockers 全部 done 时才可执行。

## Steps

1. 加入 attempt_seconds=1800、infrastructure=1；写清 worker 初次加2次额外重试、escalate共1次。
2. 对 spawn/权限拒绝、超时、异常退出、无效输出、环境错误规定分类、计数和下一状态。
3. 预算耗尽 block 并传播依赖阻塞；独立票继续。不能安全停止的 child 阻止继续派发/清理并标记 failed。
4. 实现 success/partial/failed 判定与停止时出 brief；full suite 红色进入有限最终修复/报告，只有 success 可按事先选择推送。

## Examples

| Input / situation | Expected observable result |
| --- | --- |
| worker 连续失败，默认预算 | worker 最多3次实现，escalate最多1次，随后 blocked；review不会省略。 |
| 一个 attempt 连续两次瞬时基础设施错误 | 只允许1次额外基础设施重试，之后终止该 attempt 并 block；不计作业务实现重做。 |
| reviewer 超过 timeout 或只返回无效文本 | 取消/收集证据，进入有限错误路径，不永久 in-review。 |
| A done、B blocked，余下集成验证与最终 review 全绿 | result=partial，列出B，不自动推送。 |
| full suite 红色或资源无法安全停止 | result=failed，保留证据和现场，仍交付 brief。 |

## Acceptance criteria

- [x] 所有已列错误均有有限状态出口和证据记录。
- [x] 实现、基础设施和最终修复计数不混用。
- [x] 终态准确，full suite 红色不会阻断 brief。
- [x] partial/failed 不自动推送，活跃资源不被误清理。

## Verify

建立包含输入事件、计数、下一状态、brief结果的场景表，覆盖五个例子并核对实际协议每条分支。无需实现影子 scheduler；真实运行由最后一票验证。

交付时列出修改范围、逐项验收结果、实际运行命令/退出码和未验证项。对仓库编辑运行 `git diff --check`，并检查新增文件；此命令不替代行为验证。

## Completion

验收项全部满足且证据可重现后才改为 done。有环境或设计阻碍则改为 blocked，并写明原因、现场和下一步所需条件。未取得真实模型证据时，不使用“端到端通过”的表述。

## Comments

- 2026-10-13：根据架构审查编写；尚未实现，待批次确认。
- 2026-10-13：用户授权架构师决策，批次已定稿；状态改为 ready-for-agent。仍须等待执行指令，且只在前置票全部 done 后执行。

- 2026-10-14：gpt-6.1-sol/high 候选 11ba513，集成 6ffa530。root 核对 24 个 D7/D8 场景通过；当前交付提交 PASS 和 ticket Verify 分类两处说明已修正；merger 确认文档与候选逐字相同，33 个本地文件链接存在，diff check 通过。证据：docs/verification/reliability-hardening/07/README.md。属于手动协议验证，不称真实 runtime 测试。
