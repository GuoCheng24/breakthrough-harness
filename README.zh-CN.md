# breakthrough-harness

[![checks](https://github.com/GuoCheng24/breakthrough-harness/actions/workflows/test.yml/badge.svg)](https://github.com/GuoCheng24/breakthrough-harness/actions/workflows/test.yml) [![license](https://img.shields.io/badge/license-MIT-green)](LICENSE) [![deps](https://img.shields.io/badge/deps-numpy%20only-blue)](examples/toy_loop.py)

**让你的科研 agent 难以被欺骗——首先是难以被它自己欺骗。**

[English](README.md) · 任何 agent 技术栈皆可用 · 纯方法论 + 一个可运行演示

```text
校准集扫描(只许在这里调参)                     留出集确认(永不调参)
   240.00 dB  作弊者      <- 排名登顶              作弊者      240.00 ->  -1.34  崩塌
    23.31 dB  ista 5e-2                            ista 5e-2    23.31 ->  22.31  复现
    16.99 dB  ista 2e-2                            ista 2e-2    16.99 ->  14.87  复现
    -0.00 dB  零模型      <- 踩在地板上,理应如此
```

这就是 `python examples/toy_loop.py`(30 秒内,只依赖 numpy):一个偷偷拟合了
校准集答案的候选看起来像个突破,留出集确认当场处决它。**这半屏输出就是整个
仓库的哲学。**

市面上的 agent harness 教 agent 怎么干活;这个仓库教科研 agent **怎么不骗自己**——
因为科研里的失败极少是"代码崩了",几乎总是"数字看起来很棒,但它是错的"。
每条规则都由真实失败付过学费;它也遵守自己的规则:页面所声称的,`tests/` 在每次
推送时检查。

## 核心主张

> **突破是一个吞吐量问题。**
> 突破 ≈ 大量廉价尝试 × 一个骗不过去的评分函数

串行手工实验一年只有几十次尝试;真正产出过构造性突破的系统(数学构造的程序搜索、
锦标赛式假设引擎)共享一副骨架:**并行廉价生成 + 自动化的不可欺骗筛选**。
你复制不了它们的算力,但可以复制骨架——前提是评分函数按审稿人的严格程度建造。

还有一个更安静的推论:当每次尝试都很贵,理性选择永远是审计已有的而不是建造可能
失败的——审计有保证的交付物。总在"滑向阴性结果论文"的团队不是不自律,是在对
尝试的价格做理性反应。**把价格修好,滑坡自然停。**

## 内容

| 目录 | 提供什么 |
|---|---|
| [`loop/`](loop/LOOP.md) | 突破循环:带理由生成 → 并行扫描 → 校准集选择 → **留出集确认** |
| [`harness/`](harness/CHECKLIST.md) | 评分引擎建造清单,含**反作弊四件套**:零模型踩地板;指标口径钉死并双报;校准/评估物理分离;基线荒谬即冻结 |
| [`gates/`](gates/GATES.md) | 立项闸门:靶子三问、**主张极性红线**、占位核查读到 claim 层 |
| [`rules/`](rules/RULES.md) | 十条工程铁则,**每条附上它的真实学费** |
| [`examples/`](examples/) | 上面那个可运行演示 |
| [`adapters/`](adapters/) | 接入**你的**技术栈——见下 |

## 接进你的 agent,不挑框架

方法论本体是纯 markdown,不依赖任何厂商。适配器只是把它装进你的 agent 读指令的地方:

| 你的技术栈 | 这样做 |
|---|---|
| **任何读 `AGENTS.md` 的工具**——含 **DeepSeek Harness**(DSH 官方的 agent 指令文件就是 `AGENTS.md`)、Codex、Cursor、Jules、Amp… | 把 [`adapters/AGENTS.md`](adapters/AGENTS.md) 拷进项目根目录 |
| **Claude Code** | `cp -r adapters/claude-code/breakthrough-loop ~/.claude/skills/` |
| **Cursor** | `cp adapters/cursor/breakthrough-loop.mdc 你的项目/.cursor/rules/` |
| **GitHub Copilot** | 把 [`adapters/copilot/copilot-instructions.md`](adapters/copilot/copilot-instructions.md) 并入 `.github/copilot-instructions.md` |
| **其它一切**(裸 API、LangChain、自研循环、或者你本人) | 粘贴 [`adapters/SYSTEM_PROMPT.md`](adapters/SYSTEM_PROMPT.md) |

## 快速开始

```bash
git clone https://github.com/GuoCheng24/breakthrough-harness
cd breakthrough-harness
python examples/toy_loop.py     # 30 秒内,只依赖 numpy
```

## 五个习惯,一屏说完

1. **先跑零模型。** 相信任何分数之前,先问"一个什么都没学的方法会得几分"。
2. **校准与评估永不接触。** 留出集上不复现的增益不存在。
3. **打不过的基线 = 没读完的配方。** 优化器、损失、指标口径、算子——层层都会动数字。
4. **主张有极性。** 主句必须是"我们提出 X,解决 Y,数字是 Z";审计产出只作支撑。
5. **每个守卫都要亲眼看它失败一次。** 没触发过的检查只是装饰。

## 这是什么,不是什么

| | 编排框架 | **breakthrough-harness** |
|---|---|---|
| 教 agent | 怎么干活 | 怎么**不骗自己** |
| 形态 | 运行时 / SDK | 纯 markdown + 一个 numpy 文件 |
| 绑定 | 各自技术栈 | 零绑定——各栈都有适配器 |
| 守护的是 | agent 的能力 | agent 报告内容的**科学有效性** |

它插进你已有的任何东西,不替代任何东西。

## 许可

MIT。用它、fork 它、反驳它——如果某条规则帮你省下一个月,一颗 star 能帮别人也找到它。
