# ledger-v2 基准：implement-spec vs grill-autopilot（Codex）

一个中等规模、难易混合的任务：给 80 行的记账库补 9 个故事，见 [spec](seed/docs/specs/ledger.md)。两组从同一个 commit、同一份 spec 出发，都跳过 grill 和 to-spec，各开一个全新的 Codex 会话：

| 组 | 流程 | 模型 |
| --- | --- | --- |
| A | to-tickets → implement-spec（子代理、worktree、code-review） | 全部 gpt-6.1-sol high |
| B | grill-autopilot（本仓库当前 commit 的 `skills/grill-autopilot`） | planner / reviewer / escalate sol high，worker luna medium |

prompt 不提预算，并要求不许为省 token 跳步骤。验收用另一套隐藏测试，不在本仓库里。

## 运行

前提：已登录 Codex CLI；`~/.codex/skills/` 下有 grilling、to-spec、to-tickets、tdd、code-review、setup-matt-pocock-skills、implement-spec。

```bash
git fetch origin && git switch codex/reliability-hardening/integration && git pull
bash bench/ledger-v2/run.sh
```

脚本先在 `~/autopilot-bench-ledger-v2`（必须不存在）建好种子仓库和两个 clone，再依次跑 A 组和 B 组，最后把结果写到 `docs/verification/codex-bench-ledger-v2/<机器>-<时间>/`：

- `summary.json`：每组的起止时间、退出码、按模型统计的 token（从 `~/.codex/sessions` 里按目录筛出主会话和子代理）
- 每组：`last.md`（最终报告）、`repo.bundle`（全部分支）、`git-graph.txt`、`scratch/`（tickets、brief）、主会话的 context 报告

不会复制原始会话记录。跑完后按脚本最后一行提示 commit 并 push。

默认仍使用 `workspace-write`。Codex 会保护仓库的 `.git`，仅授权父目录不能让 Git 创建分支或提交。脚本在启动每组会话前，额外用 `--add-dir <该组仓库>/.git` 显式授权该组的共享 Git 元数据；worktree 的提交也写入这个目录。A、B 使用相同授权，不需要复制 Git 元数据或关闭整个沙箱。权限仍被拒时保留失败结果，不自动扩大权限或重跑。

可选环境变量：`ARMS="b"` 只跑一组；`BENCH_ROOT` 换目录；`MODEL`、`EFFORT` 换模型；`SANDBOX` 换沙箱。如果 commit 因 `.git` 不可写而失败，在一次性机器上用 `SANDBOX=danger-full-access` 重跑（换一个新的 `BENCH_ROOT`）。
