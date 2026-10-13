---
title: grill-autopilot 架构审查
subtitle: 先修可执行性，再验证无人值守承诺 · 2026-10-13
template: doc
lang: zh
---
## A 核心判断
```callout err 默认 Codex 路径无法派发第一张 ticket
集成分支与 ticket 分支互为前缀，Git 拒绝创建。
方向值得保留，但还不能保证 Go 后自动跑到 brief。
```
这是协议审查与临时 Git 复现。未运行真实模型的完整流程。

## B 默认路径在哪里中断
```flow LR
确认需求 -> 写spec和ticket -> 创建集成分支
创建集成分支 -> 创建ticket分支: 同名前缀冲突
创建ticket分支 --> 并行实现: 当前无法到达
并行实现 -> 逐票审查 -> 集成验证 -> 最终审查 -> 交付brief
```
`autopilot/demo` 已存在时，不能创建 `autopilot/demo/01`。
建议采用独立的 integration 与 tickets 名称。

## C 优先处理的四个问题
| 编号 | 问题 | 最小修正 |
| --- | --- | --- |
| P1-1 | 默认分支创建失败 | 消除 ref 前缀冲突 |
| P1-2 | blocked 清理不能保存未提交工作 | 保留失败 worktree 和路径 |
| P1-3 | 最终修复提交未复审 | reviewer 审查最终 SHA |
| P1-4 | 异常退出没有终止路径 | 有限重试，失败也写 brief |

## D 哪些已有实证
| 场景 | 临时 Git 观察 |
| --- | --- |
| 默认 ticket 分支 | 创建失败，退出码 255 |
| 原 checkout 的未提交 spec | 不会出现在新 worktree |
| 原 checkout 的 ignored 依赖 | 不会复制到 worker |
| 删除 dirty worktree | Git 拒绝，退出码 128 |
| 只保留 branch | 不包含未提交修改 |
| reset --hard | 未跟踪检查产物仍存在 |

## E 三个值得集中管理的 seam
```flow LR
- Planner -> 分散的Git指令
- Planner -> 分散的清理规则
- Planner -> 分散的异常处理
+ Planner -> Ticket尝试模块
+ Ticket尝试模块 -> Runtime适配
+ Ticket尝试模块 -> 现场与结果记录
+ Reviewer -> 固定SHA的验收
+ 固定SHA的验收 -> 串行集成验证
```
先统一协议与 fixture，再决定是否加小脚本。
不需要数据库、守护进程或通用工作流框架。

## F 对 Claude 留言的判断
| 项目 | 审查结论 |
| --- | --- |
| 依赖路径发现 | 有改善，还需固定兼容版本 |
| 无人值守 | 还缺失败终态与恢复 |
| 首次完整运行 | 先修分支，再跑成功与失败样本 |
| 收益图 | implement-spec 已并行，2.5 倍基线不成立 |
| 开源政策 | 用户待确认，本次未发布 |
| owner | 当前 remote 指向 miniLV |
| 英文版 | 协议验证后再同步 |
| 源码位置 | 当前仓库唯一维护，不放 plexus |

## G 下一步验收标准
- 默认安装与首张 ticket 能跑通。
- worker 失败时保留未提交工作。
- 异常退出也生成失败 brief。
- 最终 SHA 经过 reviewer 和测试。
- 相同 spec、验收和并发条件下记录成本。

[完整审查报告](2026-10-13-architecture-review.md) 包含九条发现、证据、修正建议和验证局限。
