# 12: 安装说明可用，收益与兼容性声明有证据

**What to build:** 新用户能按文档安装，并准确理解当前保护范围、验证状态和成本限制。

**Blocked by:** 03, 10, 11

**Status:** ready-for-agent

Priority: P2 · 审查发现 9 与发布建议
Spec decisions: D1,D11
User stories: US4, US10, US17

## Context

先读父目录的 spec 与执行索引。本票包含执行所需的行为决定；若现场与基线不同，核对当前实现后记录差异，不默默改变本票目标。

## Scope

README的Quick start、输出、安全、限制、模型和收益段落，主skill及runtime适配的入口描述。现有宣传图引用。

本票不修改 plexus、全局配置或上游 companion；不启动其他票、不 push、不发布。仅当批次已批准、本票为 ready-for-agent 且 blockers 全部 done 时才可执行。

## Steps

1. 使用miniLV克隆地址，安装前mkdir，目标已存在时检查并报告冲突；维护源指向当前仓库。
2. 同步原checkout运行资料例外、实际模型/unknown、有限等待、恢复与partial/failed行为。
3. 移除旧图引用，改为一张Mermaid流程和文本表格；删除2.5倍与未经实测的汇总省钱百分比。
4. 建立运行证据字段与runtime验证矩阵：有真实日志才标验证通过；执行下一票前保留尚未完成端到端验证。

## Examples

| Input / situation | Expected observable result |
| --- | --- |
| 空白临时HOME，没有skills目录 | mkdir后可以创建指向仓库的链接。 |
| 安装目标已有其他文件/链接 | 不覆盖，明确报告。 |
| 只有Git fixture通过，没有真实模型run | 状态仍为未完成端到端验证。 |
| 只验证Codex，Claude没有运行证据 | 矩阵分别标记，不能笼统称两者都验证过。 |
| 成本token/缓存拿不到 | 记录unknown，不由单价比例推导总体节省。 |

## Acceptance criteria

- [ ] 安装没有owner占位符，缺目录与目标冲突可处理。
- [ ] 宣传图不再覆盖或矛盾于文本契约。
- [ ] 数字收益、验证状态、checkout和选模承诺准确。
- [ ] 不写plexus，不改全局配置，不执行发布。

## Verify

在临时HOME下演练目录和软链接操作，只将路径作为测试变量；核对文档每条承诺与本spec/现有证据。渲染或预览Mermaid以检查可读性。

交付时列出修改范围、逐项验收结果、实际运行命令/退出码和未验证项。对仓库编辑运行 `git diff --check`，并检查新增文件；此命令不替代行为验证。

## Completion

验收项全部满足且证据可重现后才改为 done。有环境或设计阻碍则改为 blocked，并写明原因、现场和下一步所需条件。未取得真实模型证据时，不使用“端到端通过”的表述。

## Comments

- 2026-10-13：根据架构审查编写；尚未实现，待批次确认。
- 2026-10-13：用户授权架构师决策，批次已定稿；状态改为 ready-for-agent。仍须等待执行指令，且只在前置票全部 done 后执行。
