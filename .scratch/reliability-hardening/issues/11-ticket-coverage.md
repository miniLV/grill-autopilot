# 11: ticket拆分覆盖需求且不会误判可并行

**What to build:** 便宜worker拿到的票有完整验收例子，planner不会因文件不重叠漏掉业务依赖。

**Blocked by:** None (can start when execution is requested)

**Status:** ready-for-agent

Priority: P2 · 审查中的需求覆盖建议
Spec decisions: D12
User stories: US18

## Context

先读父目录的 spec 与执行索引。本票包含执行所需的行为决定；若现场与基线不同，核对当前实现后记录差异，不默默改变本票目标。

## Scope

Worker-grade tickets的Rules、Self-check、Template与主skill票据完成条件。

本票不修改 plexus、全局配置或上游 companion；不启动其他票、不 push、不发布。仅当批次已批准、本票为 ready-for-agent 且 blockers 全部 done 时才可执行。

## Steps

1. 为每张票记录来源用户故事/验收项映射，整套票检查覆盖及明确排除项。
2. 检查每个验收项至少一个具体例子，以及错误/边界输入。
3. 依赖检查包含业务前置、缺失节点与环；文件范围检查独立进行。
4. 保留少量文件的启发式，但不强迫拆碎无法独立验收的完整行为；不能消除的设计问题block或回到规格阶段。

## Examples

| Input / situation | Expected observable result |
| --- | --- |
| spec有US1、US2，票只覆盖US1 | 自检失败，不能标整套票ready。 |
| A与B修改不同文件，但B需要A提供接口 | B显式Blocked by A。 |
| 验收项只有“正常工作”，没有具体期望 | 自检失败，要求写可观察例子。 |
| 闭环A依赖B，B依赖A | 自检失败并报告环。 |

## Acceptance criteria

- [ ] 模板能追溯来源，未覆盖需求无法通过。
- [ ] 字面例子、边界场景与业务blocking edge均被检查。
- [ ] Files隔离与依赖关系不混为一谈。

## Verify

构造四套极小票据，手动按自检给出失败原因或修正结果。无需新增只匹配模板字符串的测试。

交付时列出修改范围、逐项验收结果、实际运行命令/退出码和未验证项。对仓库编辑运行 `git diff --check`，并检查新增文件；此命令不替代行为验证。

## Completion

验收项全部满足且证据可重现后才改为 done。有环境或设计阻碍则改为 blocked，并写明原因、现场和下一步所需条件。未取得真实模型证据时，不使用“端到端通过”的表述。

## Comments

- 2026-10-13：根据架构审查编写；尚未实现，待批次确认。
- 2026-10-13：用户授权架构师决策，批次已定稿；状态改为 ready-for-agent。仍须等待执行指令，且只在前置票全部 done 后执行。
