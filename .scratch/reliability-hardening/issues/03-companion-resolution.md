# 03: 运行前选中完整且可识别的一套 companion

**What to build:** 插件或 skills 以不同方式安装时，都能明确解析一套依赖；缺文件、版本混用或来源歧义在 Go 前暴露。

**Blocked by:** None (can start when execution is requested)

**Status:** done

Priority: P2 · 审查发现 8
Spec decisions: D4
User stories: US5, US6

## Context

先读父目录的 spec 与执行索引。本票包含执行所需的行为决定；若现场与基线不同，核对当前实现后记录差异，不默默改变本票目标。

## Scope

主 skill 的 Resolve roles and companions 步骤及相关已知限制说明。按需要添加该步骤专属的披露参考，不复制上游技能。

本票不修改 plexus、全局配置或上游 companion；不启动其他票、不 push、不发布。仅当批次已批准、本票为 ready-for-agent 且 blockers 全部 done 时才可执行。

## Steps

1. 按 spec D4 的优先级以完整根目录为单位发现依赖。
2. 核对六个 skill、local tracker 辅助文件和实际必要的相对引用。
3. 保存来源 commit 或内容 hash；多个同优先级且指纹不同的完整集合要求 Go 前选择。
4. 把覆盖上游“第 4 步”改为按步骤语义与模板契约定位；恢复时核对指纹。

## Examples

| Input / situation | Expected observable result |
| --- | --- |
| 六个文件分散在两个不完整根目录 | 拒绝拼装，不进入 Go。 |
| 完整 plugin 根目录但缺 local tracker 辅助文件 | 报告缺失文件并停止准备。 |
| 同优先级有两套不同指纹的完整集合 | 列出候选并在 Go 前选择，不猜最新版。 |
| 已选来源在恢复前发生 hash 漂移 | 保留现场，拒绝按新依赖静默恢复。 |

## Acceptance criteria

- [x] 所有依赖来自同一个完整根目录。
- [x] 优先级、歧义、缺失辅助文件与指纹漂移均有明确处理。
- [x] 步骤覆盖以语义为准，说明不再把名称存在等同兼容。

## Verify

使用临时目录构造上述四种安装布局，按文档步骤逐个演练并记录最终选择/错误。此验证只确认发现契约，不宣称上游任意版本兼容。

交付时列出修改范围、逐项验收结果、实际运行命令/退出码和未验证项。对仓库编辑运行 `git diff --check`，并检查新增文件；此命令不替代行为验证。

## Completion

验收项全部满足且证据可重现后才改为 done。有环境或设计阻碍则改为 blocked，并写明原因、现场和下一步所需条件。未取得真实模型证据时，不使用“端到端通过”的表述。

## Comments

- 2026-10-13：根据架构审查编写；尚未实现，待批次确认。
- 2026-10-13：用户授权架构师决策，批次已定稿；状态改为 ready-for-agent。仍须等待执行指令，且只在前置票全部 done 后执行。

- 2026-10-13：gpt-6.1-sol/high 候选 f69c32c，集成 61c1175。四布局构造/检查 exit 0；root 独立核对 D4 手动结论通过，merger 复验通过；实际 companion 只读捕获十个 hash，Git 来源不可用如实记录。证据：docs/verification/reliability-hardening/03/README.md。未声明真实 runtime 或任意上游版本兼容。
