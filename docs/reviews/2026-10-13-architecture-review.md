# grill-autopilot 架构审查

日期：2026-10-13。范围：审查开始时暂存的整个仓库。当时仓库尚无首次提交，因此采用设计与协议审查，而不是两个提交之间的 diff review。结束时重新检查，原有文件无未提交修改，仅本次审查产物为未跟踪文件。

## 结论

这个仓库把一次需求访谈、明确的 ticket、角色模型配置和逐 ticket 审查组合成了一份可执行的 agent 协议。产品方向清楚，拆分成 SKILL、tickets、loop、runtimes、config 五部分也合理。

**当前可以作为实验性流程分享，但还不足以承诺“Go 后无人值守跑到 brief”。最先要修的是默认 Git 分支命名，它使 Codex 在第一张 ticket 派发时必然失败。** 其次是失败状态、工作保存和最终修复的复审。

按一个用户、一次运行、最多三个并行 worker 评估。未假设多租户、分布式服务或长期后台守护进程，也不建议为此引入数据库或通用工作流框架。

本次只增加审查报告和可视化，没有修改 skill、README、安装链接或 plexus 配置。ask-matt 及本机 companion 文件仅作为只读材料。当前仓库应是后续维护的唯一源码位置；安装可以直接链接这里。

## 必须修复

### 1. [P1] 默认集成分支与 ticket 分支不能同时存在——已复现

位置：[SKILL.md:38](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/SKILL.md:38)、[runtimes.md:20](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/runtimes.md:20)。

集成分支推荐 `autopilot/<slug>`，Codex ticket 分支固定为 `autopilot/<slug>/<NN>`。Git 的 ref 名称存在前缀冲突：前者存在时无法创建后者。

临时仓库采用 `slug=demo`，第二条 worktree 创建命令退出码为 255：

```text
fatal: cannot lock ref 'refs/heads/autopilot/demo/01':
'refs/heads/autopilot/demo' exists; cannot create 'refs/heads/autopilot/demo/01'
```

最小修复：使用不互为前缀的名称，例如 `autopilot/<slug>/integration` 与 `autopilot/<slug>/tickets/<NN>`，或两个独立顶层前缀。同步生成、清理和 README 示例，并在运行前校验实际 ref 冲突。否则默认 Codex 路径根本进不了实现阶段。

### 2. [P1] blocked 清理无法保全未提交工作——已复现

位置：[loop.md:25](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/loop.md:25)、[loop.md:44](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/loop.md:44)、[runtimes.md:27](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/runtimes.md:27)。

worker 在 Verify 全绿之后才提交。若它改了一半就 STUCK，或最后一次修复仍失败，worktree 可以带有未提交改动。协议却要求删除 worktree、只保留分支。实测普通 `git worktree remove` 以 128 退出；分支不包含那份未提交修复。如果 agent 为完成清理自行加 `--force`，这些工作就会丢失。

最小修复：blocked 默认保留完整 worktree，并在 brief 写明路径、branch 和 dirty 状态。成功且 clean 的 worktree 才自动删除。不要把强制删除当作恢复办法。

### 3. [P1] 最终修复绕过 reviewer，最后交付的代码未必被审过——协议可直接推导

位置：[SKILL.md:72](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/SKILL.md:72)。

逐 ticket 流程明确要求 worker 和 escalate 都经过 reviewer，但最终 review 把所有 findings 交给一个 escalate agent 在集成分支直接修复，随后只重跑测试。测试无法替代 scope、规范和 spec 审查；例如修复通过删弱断言让 suite 变绿，收尾阶段没有再次检查它。

最小修复：最终修复提交也必须交给 reviewer 复核。把 verdict 绑定到被审查的 commit SHA；代码继续变化就失效。限定修复轮数，仍有 findings 时在 brief 明确记录，不能把“review 曾经运行过”视为最终产物获准。

### 4. [P1] 只有业务失败，没有完整的运行失败与终止路径——协议可直接推导

位置：[loop.md:17](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/loop.md:17)、[loop.md:29](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/loop.md:29)、[SKILL.md:68](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/SKILL.md:68)、[SKILL.md:94](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/SKILL.md:94)。

现在只有收到 DONE/STUCK/PASS/FAIL 才转移状态。worker 进程退出却没有结果、reviewer 启动失败、输出格式错误或等待超时，都会留下无法按现有规则结束的 claimed/in-review。配置的 retry 约束收到 FAIL 后的重做次数，不约束一个永不返回的 attempt。

另一个断点是 step 4 要求 full suite 通过才算完成，但单 ticket Verify 没覆盖到的集成回归恰好可能让最终 suite 变红；这里没有明确下一步。step 5 允许红色结果写 brief，step 4 却没有相同的失败出口。模型不可用时的“立即停下”也没有规定先保存现状、处理已运行 children 并写失败 brief。

最小修复：为 spawn failure、timeout、child exit、malformed result 和 suite failure 写明有限处理路径；每次运行最终都生成 success/partial/failed brief。持久化 agent/process ID、worktree、尝试次数和 SHA，重启后先核对现场。合并和回滚串行，记录合并前 SHA；不要只依赖会变化的 ORIG_HEAD。

## 应当修复

### 5. [P2] spec、ticket 与 worktree 之间没有明确的文件交接契约——部分已复现

位置：[SKILL.md:49](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/SKILL.md:49)、[SKILL.md:60](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/SKILL.md:60)、[loop.md:37](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/loop.md:37)、[README.md:93](/Users/tyrion/Github/grill-autopilot/README.md:93)。

先在当前 checkout 写 `.scratch`，之后才从 base 创建集成 worktree。新 worktree 不包含未提交的 spec/ticket。实测原 checkout 出现 `?? .scratch/`，集成和 worker worktree 都没有对应文件。若 packet 填相对路径，worker 无法读取；填原 checkout 的绝对路径可以解决读取，但目前没有强制这一约定。

这也使“自己的 checkout 不会被改动”不准确，至少会新增运行资料。不要把这个问题夸大为源代码一定会被修改。

最小修复：选一个运行资料的唯一位置，packet 一律传绝对路径；planner 独占状态写入，worker/reviewer 读取稳定的 ticket/spec。可以把资料放在运行根目录，也可以明确允许原 checkout 下的 `.scratch`，但 README 必须说明例外。`spec.md#section` 这类指针也应有相同的解析基准。

### 6. [P2] 新 worktree 没有测试环境准备，代码失败和环境失败混在一起——文件行为已复现

位置：[loop.md:10](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/loop.md:10)、[loop.md:43](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/loop.md:43)、[tickets.md:12](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/tickets.md:12)。

原 checkout 能运行测试，不代表新 worktree 能运行。Git 不复制被忽略的 node_modules、虚拟环境或本地配置；临时目录验证了这种差异。当前 worker packet 直接进入 TDD，未规定安装/初始化命令，也未先证明新 worktree 的 baseline 可测试。

安装已有 lockfile 里的依赖不等于给项目新增依赖，不能依靠 ticket 中“禁止 add dependencies”替代环境准备。

最小修复：grill 时同时确认 worktree 初始化命令；在初始化后的基线运行检查。环境失败单独记录，不消耗实现重试预算。需要密钥或外部服务却尚未准备时，在 Go 前报告。

### 7. [P2] runtime adapter 只定义启动，未覆盖能力验证与资源释放——静态审查

位置：[runtimes.md:3](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/runtimes.md:3)、[runtimes.md:7](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/runtimes.md:7)、[runtimes.md:19](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/runtimes.md:19)、[config.yaml:8](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/config.yaml:8)。

三个 worker 的上限没有纳入 reviewer 占用的 agent slots，也没有定义何时释放已完成 agent。受限宿主可能无法再启动 reviewer。还需区别“缺少模型参数能力”和“上层策略拒绝该路由”：后者不能通过 CLI fallback 绕过去。

planner 配置也不是实际选模：runtimes 明确允许会话模型不一致后继续，而 README 的角色表容易让人以为配置已生效。Claude 官方文档还说明模型/effort 可能受环境变量覆盖，后台 agent 仍可能触发宿主权限交互。因此“传了参数”和“实际按该角色运行”不是同一个事实。[Claude 官方 subagent 文档](https://code.claude.com/docs/en/sub-agents)。

最小修复：adapter 返回实际能力、实际模型/effort（无法观测就记 unknown）、agent ID 和终态；对所有角色统一计算容量并释放 slots。Go 前报告已验证的路径和权限限制。不存在受支持的启动路径时结束并出 brief，不静默降级或改变授权。

本机只检查了 `codex-cli 0.156.0` 的 `exec --help`，确认文中的参数形式存在；这不证明远程模型可用、联网可行或完整 fallback 已跑通。

### 8. [P2] 找到同名 skill 不等于找到了兼容的一套依赖——静态审查

位置：[SKILL.md:25](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/SKILL.md:25)、[SKILL.md:59](/Users/tyrion/Github/grill-autopilot/skills/grill-autopilot/SKILL.md:59)、[README.md:150](/Users/tyrion/Github/grill-autopilot/README.md:150)。

插件安装路径发现确实比固定 `../to-spec` 更好。但在多个插件缓存版本或多个来源同时安装时，逐个查同名文件可能组合出混合版本。即使名称完全不变，上游改了 step 4 或模板语义，这里仍会错误覆盖；README 只描述“找不到文件就停止”，覆盖不了这种兼容性变化。

最小修复：先选择一个 companion 根目录，再从该根解析全部依赖；记录来源版本/commit 或文件 hash 和已验证组合。检查实际依赖的辅助文件，例如 `issue-tracker-local.md`，而非只检查六个 SKILL.md。无需做包管理器，也无需把上游复制进 plexus。

### 9. [P2] 收益图的加速基线与被比较方案不一致——已核对图文

位置：[README.md:27](/Users/tyrion/Github/grill-autopilot/README.md:27)、[README.md:129](/Users/tyrion/Github/grill-autopilot/README.md:129)、[benefits.png](/Users/tyrion/Github/grill-autopilot/docs/images/benefits.png)。

图声称对比 implement-spec，却用“10 轮串行 → 4 轮”推导约 2.5 倍加速。README 和本机 implement-spec 都已支持依赖图并行；这项速度增益不能由多 worker 本身证明。新增逐票 review 还可能增加关键路径。

成本估算的方向有依据：目前官方列价中，Haiku 5.5 在单次 prompt 不超过 100K 时为输入/输出 $0.10/$0.50，Opus 5.5 为 $4/$20，每百万 token 的比例为 1/40；超过 100K 的 Haiku 费率不同。[Haiku 官方价格](https://www.anthropic.com/claude/haiku)、[Opus 官方价格](https://www.anthropic.com/claude/opus)。

这不证明整项需求节省 68%。图中 review 30K/2K 是单次假设，worker 重试通常也产生额外 review；需要明确这部分是否计入，且应记录实际 token、缓存、重试与关键路径。最小修复：先移除无对等基线的加速数字；保留带公式与限制的成本情景，实跑后用相同 spec、验收和并发上限对比。

## 架构取舍：保留哪些，集中哪些

值得保留的是：清晰的角色、显式依赖图、Files 范围、验收示例、每票 review、默认本地交付。这些确实增加调用者获得的能力，也就是 codebase-design 所说的 leverage。

当前的主要成本是：安全状态转换分散在自然语言里，planner 必须同时解释状态、操作 Git、判断重试和解释宿主工具。runtimes 的 interface 看似只有三个能力，实际还泄漏了文件定位、依赖准备、权限、进程生命周期和结果有效性。

三个值得进一步设计的 seam：

| 候选 | 当前摩擦 | 最小方向 | 强度 |
| --- | --- | --- | --- |
| 一次 ticket attempt | worktree、packet、运行、清理分散 | 一个地方负责创建、定位输入、记录结果和保留失败现场 | Strong |
| 一次集成验收 | PASS、merge、验证、rollback、done 靠口头顺序 | 固定被审 SHA，串行合并验证，成功后才推进状态 | Strong |
| runtime adapter | 只声明 spawn，生命周期留给调度器猜 | 两个真实 runtime 使用相同结果与错误语义 | Worth exploring |

删除测试（deletion test）：删去几个解释性文档不会让复杂性消失，只会把它转嫁给 planner；真正应集中的是重复且机械的状态/Git规则，以提高 locality。先修协议并用临时 Git fixture 验证；若仍靠 agent 反复猜测，再把上述机械操作收进一个小脚本。不要先搭完整 orchestrator。

票数更多并不天然更便宜。每张票都有固定 review 成本；“最多三个生产文件”应继续是启发式，不能压倒可独立验收的完整行为。对“每个用户故事是否落到 ticket、out-of-scope 是否被侵犯”的检查，应加入整套 tickets 的自检，避免同一个 planner 生成的 Examples 被误当成需求完整性的证明。

## 对 Claude 留言逐条判断

| 留言 | 判断与下一步 |
| --- | --- |
| 补了插件安装路径发现 | 方向正确，修了固定相邻目录假设；尚未解决同名多版本与契约漂移。 |
| 说明和 implement-spec 的差别、上下文持平 | 更诚实；收益图的串行速度基线仍需修正。 |
| 快速开始仅使用验证过的步骤 | 目前 `<owner>` 尚未替换；新环境可能没有 `~/.claude/skills` 或 `~/.codex/skills`，应先 mkdir。安装成功与整个流程成功要分别验证。 |
| 先完整跑一次 | 是发布前最高优先级，但应先修第 1 条。验收至少覆盖成功、失败/保留现场和恢复，不只 happy path。 |
| 从未完整跑通过 | 这是用户转述的状态；仓库也没有端到端记录。README 的“还没有大规模验证”容易让人以为已有小规模成功，应如实标为“尚未完成端到端验证”。 |
| 公司开源政策 | 属于用户需要确认的发布条件；本次没有验证内部政策，也没有发布。MIT 文件不构成公司授权的证据。 |
| 替换 owner | 当前 Git remote 是 `https://github.com/miniLV/grill-autopilot.git`，可据此修正文档；本次未修改。 |
| 英文版 | 先把中文协议验证好，再同步英文；现在复制一套内容会增加需要一起修正的来源。 |
| 两份 skill 选主 | 以当前仓库为唯一源码。用户已明确不放 plexus；无需把本次产物或后续实现写入那里，也未改任何安装配置。 |

## 验证与局限

完整阅读了 README、所有六个 skill/config/metadata 文件、LICENSE、gitignore，以及五张图。只读核对了本机 ask-matt、to-spec、to-tickets、tdd、code-review、setup 的 local tracker 文档和 implement-spec；本机副本可能与他人安装的上游版本不同，未将其当作最新上游保证。

临时 Git fixture 的结果：

| 检查 | 观察 |
| --- | --- |
| 默认 ticket branch 创建 | 退出 255，ref 前缀冲突 |
| 运行文档写入原 checkout | status 出现 `?? .scratch/` |
| 相对 spec/ticket 在新 worktree 中可见 | 两者均不存在 |
| 原 checkout 独有的 ignored 依赖进入 worker | 不会复制 |
| 失败检查后 reset --hard ORIG_HEAD | 未跟踪的检查产物仍在 |
| 删除带未提交修改的 blocked worktree | 退出 128，拒绝删除 |
| 只保留 branch 能否保留未提交修改 | 不能 |

为测试后续故障路径，fixture 在复现默认分支冲突之后改用了 `ticket/demo/01`。这只是临时样本，产品文件没有相应改动。

未跟踪检查产物的实验只证明 Git reset 不会清理它们，不代表每个项目都会因此测试污染；若要清理，必须限定为本次运行拥有的产物，不能笼统强制清除用户文件。

证据目录：`/var/folders/v2/ckqz8nld0cj2s6xbr48rhvww0000gn/T/grill-review-evidence-sr6_6366/`，包含 `results.json` 与临时 worktrees。临时路径不保证长期存在，关键输出已收录在本报告。

`git diff --cached --check` 通过。没有运行真实模型的完整 grill-autopilot，没有验证 Claude Agent/Codex 模型端到端能力、真实成本/耗时、公司政策或用户账号权限。上述 Git 复现不能称为完整系统测试通过。
