# reliability-hardening：规格与执行索引

Status: partial — 2026-10-14：01–12 已在 integration 分支完成；13 已提交真实成功与拒绝证据，因 dirty 故障和实际中断恢复缺口保持 blocked。

用户已选择本地 Markdown tracker。规格在 [spec.md](spec.md)，每个 issue 独立放在 [issues](issues/) 中；所有文件仅属于当前仓库。无需为了本批任务运行 setup skill 或修改 plexus/global 配置。

## 已确定的架构选择

- 测试 seam：一次 skill run 的输入 → Git/worktree 状态、ticket 状态与 brief。临时 Git 实验、协议演练和真实模型运行分层记证，不混称端到端验证。
- 粒度：13 张票，一张一个主要结果；复杂故障处理已拆开。
- 依赖：如下表。是业务前置，不是文件锁；没有依赖也不代表能同时修改同一文档。
- 已定稿决定：默认分支使用 integration/tickets 独立 ref；运行资料留原 checkout 的明确例外；30 分钟 attempt 超时、1 次基础设施重试、2 轮最终修复；只有 success 可按事先授权推送。

用户回复“你从架构师角度做一个最优选择”，已将本批测试 seam、粒度和依赖的决策交给当前会话。因此规格与 13 张票已定稿，不再等待额外确认。用户切换模型并发出执行指令后才开始实现。

选择理由：13 张行为切片限制每票的上下文；串行执行避免共享文档冲突；一个产品 seam 保持验收完整。超时与重试值是可配置的起始保护值，真实运行后再校准，不当作实测最优。

## Issue 列表

| # | 交付结果 | Blocked by |
| --- | --- | --- |
| [01](issues/01-valid-branch-names.md) | 默认分支可以创建，已有现场不被覆盖 | 无 |
| [02](issues/02-run-record-and-inputs.md) | 独立 worktree 读取稳定快照，状态可追溯 | 01 |
| [03](issues/03-companion-resolution.md) | 选择完整且可识别的一套 companion | 无 |
| [04](issues/04-worktree-bootstrap.md) | 初始化与基线检查先于实现 | 02 |
| [05](issues/05-preserve-blocked-work.md) | blocked 保留现场，成功票安全清理 | 02 |
| [06](issues/06-runtime-lifecycle.md) | runtime 能力、模型事实与容量明确 | 02 |
| [07](issues/07-bounded-failures.md) | 异常有预算，终止有 brief | 04、05、06 |
| [08](issues/08-resume-reconciliation.md) | 恢复不重复派发、合并或覆盖 | 07 |
| [09](issues/09-sha-bound-integration.md) | 按 SHA 审查、串行合并与精确回滚 | 05、07 |
| [10](issues/10-final-review-gate.md) | 最终修复复审，最终 tip 决定结果 | 09 |
| [11](issues/11-ticket-coverage.md) | 需求覆盖与业务依赖自检 | 无 |
| [12](issues/12-honest-install-and-docs.md) | 安装、图文和收益声明与证据一致 | 03、10、11 |
| [13](issues/13-real-runtime-smoke.md) | 真实成功、失败保存和恢复证据 | 08、12 |

## 执行方式与当前进度

本批已定稿，用户选择 gpt-6.1-sol / high，并授权继续执行到完成，不使用 Luna 5.6。实现集中在 `codex/reliability-hardening/integration`，保存的审查基线为 `89246ffdcbc1efcdc2142610d7d52a62ac5520b4`。原 checkout 保持 master 与该基线，未 push、创建 PR 或发布。

01–12 的具体提交和验收证据见各 issue Comments。13 的成功样本通过现有原配置 native identity 执行；新的同模型启动被宿主拒绝，实际模型/effort 元数据仍为 unknown。完整故障与中断恢复证据尚缺，不将协议/Git 实验等同于真实模型全流程。

给执行模型的任务说明：

> 阅读本索引、spec 和指定 issue；确认批次已批准，且该 issue 的 blockers 全部 done。只完成该 issue，遵守现有设计决定。列出实际修改范围，逐项验收并保留命令和结果。证据不足就 blocked，不能自行扩大范围。实现者报告结果，由 planner 更新 Status/Comments 并继续推进 frontier。不要写 plexus，不要 push 或发布。

这些票按 to-tickets 的本地模板编写，使用行为与文档模块定位，不把当前源文件布局变成票据契约。它们可以交给执行模型逐票处理；不是当前尚未修好的 grill-autopilot 的输入。不要用待修复的流程自举执行这批修复。

这是以说明书为产品的仓库，多张票会编辑同一份 skill。执行者先按下方导航查当前内容，再圈定本票范围。文档整体可读性检查不能替代每票的行为验收。

## 当前源码导航（可变化，票据行为不变）

| 名称 | 当前入口 |
| --- | --- |
| 主 skill | [SKILL.md](../../skills/grill-autopilot/SKILL.md) |
| Implement loop / packets | [loop.md](../../skills/grill-autopilot/loop.md) |
| Runtime adapters | [runtimes.md](../../skills/grill-autopilot/runtimes.md) |
| Worker-grade tickets | [tickets.md](../../skills/grill-autopilot/tickets.md) |
| 默认配置 | [config.yaml](../../skills/grill-autopilot/config.yaml) |
| 用户说明 | [README.md](../../README.md) |
| 审查来源 | [architecture-review.md](../../docs/reviews/2026-10-13-architecture-review.md) |

本索引位于两层子目录，以上相对导航均以本文件所在目录为基准。

## 审查建议覆盖

| 审查发现 | 对应 issue |
| --- | --- |
| 1 默认 ref 冲突 | 01 |
| 2 blocked 工作丢失风险 | 05 |
| 3 最终修复绕过 review | 10 |
| 4 缺运行终态与恢复 | 07、08、09 |
| 5 跨 worktree 输入定位 | 02 |
| 6 新 worktree 测试环境 | 04 |
| 7 runtime 能力与容量 | 06 |
| 8 companion 版本一致性 | 03 |
| 9 收益对比基线 | 12 |
| 需求覆盖建议 | 11 |
| 完整试运行建议 | 13 |

公司开源政策仍由用户确认，不生成可由模型“完成授权”的实现票。英文版、大规模 benchmark、发布与重绘 PNG 均在本批范围之外。

## 验证记录

01–12 已实现并逐票验收，包含真实临时 Git/worktree 实验、安装/卸载操作、文档图渲染及明确标记的协议演练。真实模型验证单独记录于 13；完整运行状态以该 issue 和验证报告为准。

integration 分支固定基线的 Standards / Spec 两轴审查及最终验证记录保存在分支外的 `grill-autopilot.autopilot-worktrees/execution-notes/`，最终结果以其中的 `brief.md` 为准，避免写入报告后使已审查提交失效。未满足的验收项保持未勾选，不声称整份规格完成。
