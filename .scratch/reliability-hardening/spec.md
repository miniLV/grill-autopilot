# grill-autopilot reliability hardening

Status: ready-for-agent
Approval: 2026-10-13 用户授权当前会话从架构师角度决策；测试 seam、粒度与 blocking edges 已定稿。实施仍等待用户切换模型并发出执行指令。
Tracker: 本地 Markdown，用户于 2026-10-13 明确选择。
Source: 2026-10-13 架构审查与本次对话。
Baseline: 3f4c38ea509ae29e8aa574a108cb11f262cfe9e2

## Problem Statement

grill-autopilot 想让用户在需求澄清后只确认一次，再由不同角色的模型完成规格、任务、实现、审查和交付。当前协议在默认 Git 分支创建、失败工作保存、最终复审和异常终止上存在缺口；尚没有真实端到端成功记录支撑无人值守承诺。

用户准备使用更便宜的模型执行修复，因此规格必须提前确定行为、失败出口、验收输入和期望输出。执行者不应重新决定产品架构，也不能把临时 Git 实验或静态文档检查当作整个 skill 的测试通过。

## Solution

保留 Markdown skill、四个角色、本地 tracker、worktree 隔离和逐 ticket review。修复一次运行从准备、派发、验收、集成到 brief 的契约，使成功、部分完成和失败均可解释，并保留可恢复的现场。

第一版以协议修复和可复现实验为主，不新增生产执行引擎。把一次运行的输入、状态、证据、错误处理集中表达，让两个 runtime adapter 使用同一套语义。实际兼容性按已经取得的运行证据声明。

## User Stories

1. As an 使用者, I want 默认分支命名能够创建, so that 第一张 ticket 可以启动。
2. As an 使用者, I want 已存在的分支和 worktree 不被覆盖, so that 重复运行不会破坏已有工作。
3. As an worker, I want 从任何 worktree 读取同一份已确认 spec 和 ticket, so that 相对目录不影响任务理解。
4. As an 使用者, I want 原 checkout 的修改范围明确, so that 我知道本地运行资料与源代码的区别。
5. As an 使用者, I want companion 来自同一个可识别来源, so that 不会混用不兼容的版本。
6. As an 使用者, I want 缺失辅助文件或歧义依赖在 Go 前暴露, so that 不会实现到一半才发现安装不完整。
7. As an worker, I want 新 worktree 已完成约定的环境准备和基线检查, so that 环境故障不会被误判为实现错误。
8. As an 使用者, I want blocked ticket 保留未提交修改, so that 人工接手时仍有完整现场。
9. As an planner, I want 知道 runtime 的实际角色、容量和终态能力, so that 不会因 reviewer 无法启动而卡住。
10. As an 使用者, I want 配置值与实际观察值分开记录, so that 不会被错误的模型角色表误导。
11. As an 使用者, I want 超时、异常退出和无效结果有有限处理路径, so that 运行不会无限等待。
12. As an 使用者, I want 恢复时先核对现有进程与 Git 状态, so that 不会重复派发或重复合并。
13. As an reviewer, I want 审查结论绑定不可变的提交, so that PASS 不会被套用到后来修改的代码。
14. As an 使用者, I want 失败的集成验证恢复至已记录的提交且保全现场, so that 一次失败不会破坏其他 ticket。
15. As an 使用者, I want 最终修复再次经过 review, so that 最终交付版本也满足质量要求。
16. As an 使用者, I want 无论完成多少都能看到明确的运行结果, so that 我能区分 success、partial 与 failed。
17. As an 使用者, I want 文档中的安装、隔离和收益声明与证据一致, so that 可以正确判断是否采用。
18. As an 执行者, I want 每个验收项对应具体例子和独立完成条件, so that 便宜模型也能完成一个有界任务。
19. As an 维护者, I want 正常与失败路径的真实试运行证据, so that 发布声明不依赖推测。

## Implementation Decisions

### D1 保留架构和维护位置

继续由主会话解释 skill 并调用宿主工具。runtime adapter 负责宿主差异；编排循环负责 ticket 状态、验收和集成。仅在当前仓库维护源码，用户级安装直接指向仓库。此次修复不创建或修改 plexus 中的副本或链接。

### D2 分支命名与运行身份

默认集成分支为 `autopilot/<slug>/integration`，默认 ticket 分支为 `autopilot/<slug>/tickets/<NN>`。先验证 base 可解析为 commit，并保存 base SHA；验证实际分支的 Git 合法性、前缀冲突与已存在状态。

一次 run 使用唯一 run ID，slug 与 run ID 分开。相同 slug 的残留现场存在时不得自动覆盖或 reset。只有显式恢复同一个 run 才能复用，并执行 D8 核对；否则在执行前报告冲突。

### D3 运行资料与单一写入者

继续使用用户原 checkout 内的本地 tracker；它是允许写入的运行资料例外，源代码、原 checkout 的分支与 base ref 不变。planner 是 spec、ticket 状态和 run record 的唯一写入者。派发前由 planner 保存 spec 与 ticket 任务正文的只读快照，packet 指向快照；Status 与 Comments 留在可变 tracker 中。新增假设与事件单独记录；范围发生实质变化则 block，不能悄悄改题目。

所有 packet 使用 canonical 绝对路径定位 spec、ticket、工作目录、companion 和日志。子 agent 可以读取运行资料，但只能在自己的指定 worktree 修改生产文件。运行前和结束时比较原 checkout 的 ref、tracked diff 与非本次运行所有的 untracked 文件。

run record 至少包括 run ID、阶段与结果、原 checkout、base SHA、集成 ref/worktree、companion 来源指纹、请求/观察到的角色配置、初始化与验证命令、推送选择。每个 ticket 记录 branch/worktree、agent/process ID、attempt ID、各类尝试计数、时间、候选 SHA、reviewed SHA、合并前/后 SHA、verdict 和证据位置。先保存状态再执行对应外部操作；恢复时结合 Git/宿主事实核对，不能仅信状态行。

### D4 Companion 解析

以完整 companion 集合的根目录为选择单位，不逐个从不同缓存挑文件。候选按相邻 skills、项目 skills/plugin、用户 skills/plugin 顺序发现；取最高优先级中唯一完整且符合所需契约的集合。同级多个候选且来源指纹不同，Go 前让用户选；不得自行猜最新版。

检查六个依赖 skill、local tracker 辅助材料与 skill 实际引用的必要文件。记录来源 commit；没有 commit 时记录文件 hash。检查依赖步骤的语义和模板，不依靠“第 4 步”这种编号替换。找不到兼容集合时在 Go 前报告。已有选择的恢复运行校验指纹；发生漂移则停止恢复并保留现场。

### D5 Worktree 环境准备

grill 确认初始化命令、单票 Verify、full suite、typecheck；初始化命令允许显式为 None。新建集成或 ticket worktree 后先初始化并跑与该阶段相关的基线检查，再开始 TDD。安装 lockfile 中已有依赖是初始化；变更依赖声明仍受 ticket 范围限制。

初始化失败、缺少凭据和原始基线失败属于环境错误。环境修好之前不尝试代码修复，也不消耗 worker 实现次数。Go 前已知缺少能力时不能宣称已准备好；Go 后遇到新环境错误按 D7 记录，最终出 brief。

### D6 失败现场与清理

blocked 的 ticket 默认保留 worktree、branch、未提交 tracked/untracked 文件与诊断信息；停止该 run 拥有且仍运行的 agent 后再交还现场。仅当 ticket 已成功集成、没有活跃 agent、worktree clean 且确属本 run 时，才删除它并删除已合并 ticket branch。

失败 worktree 不强制删除；恢复不使用无条件 hard reset。集成 worktree在交付时保留供用户检查。清理失败记录为 cleanup warning，不改变已经有证据的验收结果，也不阻止 brief。

### D7 Runtime 能力和有限等待

adapter 统一提供启动、结果读取、存活查询、取消/停止、释放资源和能力报告的语义；使用宿主已有工具，不新建常驻服务。区分 worker STUCK/实现 FAIL、环境错误、路由拒绝、超时、异常退出、格式无效和不可观测结果。

只在工具不支持所需能力且 CLI 路径本身被允许时使用 fallback；宿主策略拒绝不能用 CLI 绕过。实际模型/effort 可观测时记录并核对；与选择不一致即停止该角色。不可观测时记录 unknown，并在 Go 前披露，不能写成已验证匹配。planner 保持当前会话模型，显示配置值与实际值的差异。

concurrency 继续表示 worker 上限。可用 slots 按所有子角色计算，完成的 worker 先释放 slot，再启动 reviewer；优先处理等待 review 的票，随后补 worker。容量不能探测时从一个 child 开始；容量拒绝进入队列等待现有 child 释放，不能无限重复 spawn。

增加三个明确的默认值：`timeouts.attempt_seconds = 1800`、`retry.infrastructure = 1`、`retry.final_review = 2`。attempt 的计时包含初始化、实现或审查调用，不靠 worker 自觉输出 STUCK 结束；由宿主有界等待与 planner 的时间检查执行。若调用不可取消，停止新派发并保留所有可能仍被写入的现场，brief 标记资源未完全停止。

### D8 重试、恢复与结果

worker 先执行一次，`retry.worker = 2` 表示最多两次额外实现；之后 escalate 最多执行 `retry.escalate = 1` 次。每个候选提交均需 review。瞬时基础设施错误对同一个逻辑 attempt 最多额外重试一次，单独计数；权限拒绝、模型不可用或持续基线红色不自动重试。预算耗尽则 blocked，依赖它的票传播 blocked，其余独立票继续。

恢复先读取 run record，核对进程、worktree、候选提交和集成祖先关系。活跃 attempt 不重复启动；已合入且记录了通过验证证据的候选可补记 done；没有验证证据的重新验证，不能凭 branch 存在认定完成。状态或所有权无法确定则停止恢复并给出 failed brief，不重置或清理现场。进程被杀死或机器断电时无法保证立刻写 brief；下一次恢复应先记录中断再完成核对。

运行最终结果固定为：

- success：所有 ticket done，最终 suite/typecheck 通过，最终提交获得 review PASS。
- partial：至少一张 done、至少一张 blocked，剩余已集成范围的验证和最终 review 均通过；已知 blocked 对应的缺失单独列明，不伪装成完整 spec 实现。
- failed：无完成项，或最终验证失败，或最终仍有未解决 review findings，或无法安全恢复/停止资源。

所有可处理的停止路径都先保存状态并写 brief。full suite 红色也允许进入有限最终修复与报告，不作为永远进不了收尾的前置条件。只有 success 且用户事先选择推送才可自动 push/draft PR；partial/failed 默认本地交付。

### D9 按提交验收与串行集成

worker 返回候选 commit SHA，reviewer 针对该 SHA 和固定比较基点给结论。PASS 必须包含 reviewed SHA 与验证证据位置。验收后 ref 移动或内容变化就失效；Git 的普通合并提交本身在集成验证中确认，不要求单纯的 merge commit 重新做一次逐票 review。

一次只进行一个 merge→Verify→记录结果事务。合并前记录精确 integration SHA；验证通过才标记 done。冲突先保存诊断，再 abort；普通验证失败恢复到记录的 SHA，不依赖 ORIG_HEAD。发现不属于本事务的 tracked 修改或无法归属的 untracked 文件时保留现场并失败，不强制清理。只允许清理本事务明确记录拥有的生成产物。worker 在合并 tip 时发生冲突也需保存现场和报告，不能遗留冲突状态后继续盲目重试。

### D10 最终 review

对集成 tip 做 Standards 与 Spec 两轴 review；对于已知 blocked 需求，Spec 轴明确列为未交付范围，其他 findings 仍要修复。所有最终修复之后重新跑 suite/typecheck 并对新 SHA 复审，最多两轮修复。首轮无 findings 则无需调用修复角色。

只有当前 tip 同时持有有效的 review PASS 和测试证据才算通过。预算耗尽后仍有 findings 或 suite 红色则 failed，并在 brief 列出未解决项；不能因曾经 review 过而通过。

### D11 文档与证据

安装克隆地址使用已核实的 remote owner miniLV；先创建目标 skills 目录，对已存在且不属于本安装的目标明确报冲突，不覆盖。维护说明直接指向当前仓库。

纠正“checkout 完全不变”、无限无人值守、模型配置必定生效和未验证 runtime 的承诺。删除串行基线推导的 2.5 倍加速与未经实测的汇总省钱百分比。保留角色分工的定性理由，实际成本报告分开记录模型请求/观察值、输入输出、缓存、review、重试和耗时；拿不到的值为 unknown。

五张静态图不再承担协议与数字的权威来源。用一张可维护的 Mermaid 主流程和文本表格替换 README 中的旧图引用；旧图片本轮保留为历史素材，不另花成本重绘。英文版和正式对照 benchmark 延后。

### D12 需求覆盖与执行验证

ticket 自检同时验证每个用户故事有交付 ticket 或明确 out-of-scope，每个验收项有具体例子，依赖图无缺失或环。Files 隔离不等于业务依赖正确；文件不重叠但行为互相依赖时仍要写 blocking edge。

完成协议修复后，用小型无网络业务逻辑 fixture 跑真实模型成功案例、失败保留案例和中断恢复案例。fixture 使用标准库测试，明确 typecheck 不适用并记录理由，不伪造通过。一次 run 配置允许显式 N/A 的检查，但关键行为必须有可执行测试。

首先选择一个实际可用且获授权的 runtime 验证。另一 runtime 未验证就如实标记未验证，不扩大兼容性结论。本阶段不执行大规模 benchmark，不自动发布。

## Testing Decisions

### 已确定的唯一产品 seam

**一次 skill run 的输入 → Git/worktree 最终状态、ticket 状态和 brief。** 测试观察外部行为，不断言内部措辞、文档行号或实现函数拆分。

验证分成三层，不改变产品 seam：

1. 文档契约核对：场景逐项对照明确规则，检查路径、终态与口径没有互相冲突。只能证明规则完整，不证明 agent 遵守。
2. 临时 Git 实验：使用 Python 标准库或 shell 调用真实 Git，验证 ref 冲突、资料可见性、dirty worktree 保存、固定 SHA 回滚等语义。每次在新临时仓库运行，保留输入、命令、退出码与观察；不依赖上次审查的临时目录。不用测试复刻一个并不存在的生产调度器。
3. 真实 runtime 小样本：通过 skill 的实际入口运行 fixture，检查外部状态与日志。成功、失败和恢复分别取证；报告实际模型与未知项，不能把 Git 实验替代这一层。

高风险检查包括：默认创建成功；已有 ref 不变；两个 worktree 读取相同输入；初始化失败不消耗实现次数；dirty blocked worktree 保留；超时能收尾；活跃 child 不重复派发；stale PASS 被拒绝；merge 验证红色恢复正确 SHA；最终修改必须复审；partial/failed 不自动推送。

先例来自本次架构审查的真实 Git 复现。仓库当前没有产品测试套件或执行器。对协议编辑使用场景证据；若某票新增有分支逻辑的可执行辅助代码，再为该代码补真实行为检查。不得通过逐字匹配说明书或生成一个影子 scheduler 宣称产品测试通过。

## Out of Scope

- 现在执行这些 issues；本轮只交付可审查的 spec 与拆分。
- 重写为通用 orchestrator、数据库、daemon 或新的包管理器。
- 修改 plexus、用户全局配置、安装路径或 companion 上游源码。
- 隐式换模型、绕过宿主策略、强制删除 dirty worktree。
- 英文版、重新生成五张宣传图、大规模成本 benchmark。
- GitHub Issues、push、PR、正式发布及公司开源授权判断。

## Further Notes

用户已授权架构决策，以下选择已定稿：新的分支命名、运行资料留在原 checkout 的明确例外、30 分钟 attempt 超时、一次基础设施重试、两轮最终修复、成功才自动推送、一个产品 seam 的三层验证。

本地 tracker 根目录为 `.scratch/reliability-hardening/`。spec 与全部 13 张票已标为 ready-for-agent；该状态表示规格已定稿，不表示已授权本轮开始实施。依赖未完成的票仍不可执行。此次使用 to-spec/to-tickets 的本地模板，不启动 grill-autopilot 自身，也不套用其自动跳过审批的 override。

恢复和超时能力取决于 runtime；不得声称在主进程崩溃后仍会自行运行。真实试运行需要用户开始执行阶段时的模型、权限和预算，缺少时报告 blocked，不伪造成功。

### 架构决策记录 · 2026-10-13

保留 13 张行为切片，默认按编号串行执行。每票可独立核对结果，失败处理、恢复和集成分别验收，减少便宜模型同时掌握的状态。多票修改同一说明书，因此不为并行增加合并成本。

保留一个产品 seam 的三层验证，既观察用户能获得的结果，也区分 Git 语义证据与真实模型行为。先修现有 Markdown 协议，不引入生产执行引擎；只有真实试运行证明协议无法可靠执行时，再提出有证据的后续设计票。

30 分钟超时、1 次基础设施额外重试、2 轮最终修复作为可配置的起始保护值，不宣称它们是实测最优参数。第 13 票收集证据后，再据实际失败分布校准。
