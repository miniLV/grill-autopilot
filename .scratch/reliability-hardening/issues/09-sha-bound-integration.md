# 09: 只合入被审查的候选，失败回到精确基点

**What to build:** PASS 对应具体候选提交；并行完成的票串行集成，验证失败不损伤其他已合并工作。

**Blocked by:** 05, 07

**Status:** ready-for-agent

Priority: P1 · 审查发现 4 的集成事务
Spec decisions: D9
User stories: US13, US14

## Context

先读父目录的 spec 与执行索引。本票包含执行所需的行为决定；若现场与基线不同，核对当前实现后记录差异，不默默改变本票目标。

## Scope

Implement loop 的 worker/reviewer packets、On PASS 与合并失败路径。

本票不修改 plexus、全局配置或上游 companion；不启动其他票、不 push、不发布。仅当批次已批准、本票为 ready-for-agent 且 blockers 全部 done 时才可执行。

## Steps

1. worker/reviewer结果携带候选和reviewed SHA及证据指针；固定比较基点。
2. merge前核对候选仍等于reviewed SHA，并保存精确integration pre-merge SHA。
3. 串行运行merge、Verify、状态写入；验证通过后才done。
4. 冲突保存诊断并abort；检查失败恢复记录SHA；不清理未知文件。worker合并tip冲突同样保存并报告。

## Examples

| Input / situation | Expected observable result |
| --- | --- |
| review PASS针对A，branch已前进到B | 拒绝套用PASS，B重新review。 |
| A已成功合入，B合入后Verify失败 | 恢复到B合入前的精确SHA，A仍存在，B不done。 |
| 检查生成已知产物和未知用户文件 | 仅处理归属本事务的产物；未知文件保留并报告。 |
| 两个review同时PASS | 一次只集成一个，第二个使用更新后的integration基点验证。 |

## Acceptance criteria

- [ ] verdict可追溯到不可变候选，stale PASS无效。
- [ ] done出现在merge和验证成功之后。
- [ ] 恢复目标不依赖ORIG_HEAD。
- [ ] 并行worker不导致并行merge事务，冲突现场可解释。

## Verify

临时Git实验复现先合A、后合B失败并恢复，比较SHA与文件内容；另构造A审后branch前进到B。记录实际Git结果，说明由planner执行的契约尚待真实运行验证。

交付时列出修改范围、逐项验收结果、实际运行命令/退出码和未验证项。对仓库编辑运行 `git diff --check`，并检查新增文件；此命令不替代行为验证。

## Completion

验收项全部满足且证据可重现后才改为 done。有环境或设计阻碍则改为 blocked，并写明原因、现场和下一步所需条件。未取得真实模型证据时，不使用“端到端通过”的表述。

## Comments

- 2026-10-13：根据架构审查编写；尚未实现，待批次确认。
- 2026-10-13：用户授权架构师决策，批次已定稿；状态改为 ready-for-agent。仍须等待执行指令，且只在前置票全部 done 后执行。
