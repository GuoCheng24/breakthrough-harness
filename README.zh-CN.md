# breakthrough-harness

**让你的科研 agent 难以被欺骗——首先是难以被它自己欺骗。**

[![checks](https://github.com/GuoCheng24/breakthrough-harness/actions/workflows/test.yml/badge.svg)](https://github.com/GuoCheng24/breakthrough-harness/actions/workflows/test.yml) [![license](https://img.shields.io/badge/license-MIT-green)](LICENSE) [![deps](https://img.shields.io/badge/deps-numpy%20only-blue)](examples/toy_loop.py)
[![已收入 github/awesome-copilot](https://img.shields.io/badge/%E5%B7%B2%E6%94%B6%E5%85%A5-github%2Fawesome--copilot-1f6feb?logo=github&logoColor=white)](https://github.com/github/awesome-copilot/blob/main/agents/research-harness-engineer.agent.md)

[English](README.md) · 任何 agent 技术栈皆可用 · 纯方法论 + 两个可运行演示

![演示:作弊者在校准集登顶、在留出集崩塌;零模型踩在地板上](.github/assets/demo.gif)

这就是 `python examples/toy_loop.py`(30 秒内,只依赖 numpy):一个偷偷拟合了
校准集答案的候选看起来像个突破,留出集确认当场处决它。**这半屏输出就是整个
仓库的哲学。**

市面上的 agent harness 教 agent 怎么干活;这个仓库教科研 agent **怎么不骗自己**——
因为科研里的失败极少是"代码崩了",几乎总是"数字看起来很棒,但它是错的"。
每条规则都由真实失败付过学费;它也遵守自己的规则:页面所声称的,`tests/` 在每次
推送时检查。

## 核心主张

> **突破是一个吞吐量问题。**
> 突破 ≈ 大量廉价尝试 × 一个很难骗过的评分函数

串行手工实验一年只有几十次尝试;真正产出过构造性突破的系统(数学构造的程序搜索、
锦标赛式假设引擎)共享一副骨架:**并行廉价生成 + 自动化的难以欺骗的筛选**。
你复制不了它们的算力,但可以复制骨架——前提是评分函数按审稿人的严格程度建造。

还有一个更安静的推论:当每次尝试都很贵,理性选择永远是审计已有的而不是建造可能
失败的——审计有保证的交付物。总在"滑向阴性结果论文"的团队不是不自律,是在对
尝试的价格做理性反应。**把价格修好,滑坡自然停。**

![循环结构:生成-扫描-校准集选择;跨过"调参永不越线"进入留出集确认;每次失败变成新的 harness 检查](.github/assets/loop-diagram.png)

## 内容

| 目录 | 提供什么 |
|---|---|
| [`loop/`](loop/LOOP.md) | 突破循环:带理由生成 → 并行扫描 → 校准集选择 → **留出集确认** |
| [`harness/`](harness/CHECKLIST.md) | 评分引擎建造清单,含**反作弊四件套**:零模型踩地板;指标口径钉死并双报;校准/评估物理分离;基线荒谬即冻结 |
| [`gates/`](gates/GATES.md) | 立项闸门:靶子三问、**主张极性红线**、占位核查读到 claim 层 |
| [`rules/`](rules/RULES.md) | 11 条工程铁则,**每条附上它的真实学费** |
| [`examples/`](examples/) | 两个可运行演示:上面的作弊者,以及「平坦的扫描在说谎」(force_balance.py,规则 3 的现场版) |
| [`adapters/`](adapters/) | 接入**你的**技术栈——见下 |
| [`template/`](template/) | **可直接跑的 campaign 起步模板**:带零模型与实时冻结规则的入口 harness、留出集访问日志、轮次台账、含故意破坏测试的守卫——一个下午即可改造成你的任务 |

## 另一个演示:说谎的平坦扫描

```text
第一幕  lam 扫 {0.1, 1, 10, 100}  -> 得分 2.1, -0.0, -0.0, -0.0  「平坦,参数不起作用」
第二幕  测一次梯度范数力平衡      -> 每个值都碾碎了数据项;平衡点在 ~0.05
第三幕  围绕平衡点重扫            -> 干净内点峰 lam = 0.0015,22.6 dB
```

`python examples/force_balance.py`:数据项是"均值"、正则项是"求和",四个数量级
的扫描全落在力平衡同一侧,于是看起来平坦。一次梯度范数评估找到真实范围。
这是规则 3 的现场版。

## 接进你的 agent,不挑框架

方法论本体是纯 markdown,不依赖任何厂商。适配器只是把它装进你的 agent 读指令的地方:

| 你的技术栈 | 这样做 |
|---|---|
| **DeepSeek Harness** | **无需拷贝** —— 克隆本仓, DSH 直接就能找到 [`.agents/skills/breakthrough-loop/`](.agents/skills/breakthrough-loop/SKILL.md):它的文件系统 skill 提供者以 rank 200 扫描 `<项目根>/.agents/skills`。要用在你自己的项目里, 把那个目录拷过去, 或把 [`adapters/AGENTS.md`](adapters/AGENTS.md) 放到项目根 —— DSH 的 `agent-instructions` 插件会加载它 |
| **Codex、Gemini CLI、Cursor、GitHub Copilot、Devin Desktop** —— 以 skill 形式 | 把 [`.agents/skills/breakthrough-loop/`](.agents/skills/breakthrough-loop/SKILL.md) 拷进项目的 `.agents/skills/`;这五家现在都原生读取该目录,任务需要时才加载 |
| **OpenAI Codex** —— 以指令文件形式 | 同一个文件:把 [`adapters/AGENTS.md`](adapters/AGENTS.md) 拷进项目根目录(Codex 读 `AGENTS.md`) |
| **其它读 `AGENTS.md` 的工具**(Jules、Amp…) | 把 [`adapters/AGENTS.md`](adapters/AGENTS.md) 拷进项目根目录 |
| **Claude Code** | `/plugin marketplace add GuoCheng24/breakthrough-harness` 后 `/plugin install breakthrough-harness@breakthrough-harness`——或手动 `cp -r adapters/claude-code/breakthrough-loop ~/.claude/skills/` |
| **Cursor** | `mkdir -p 你的项目/.cursor/rules && cp adapters/cursor/breakthrough-loop.mdc $_` |
| **GitHub Copilot** | 一键安装:从 GitHub 官方的 [awesome-copilot](https://github.com/github/awesome-copilot) 收录中[装 Research Harness Engineer agent](https://aka.ms/awesome-copilot/install/agent?url=vscode%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fgithub%2Fawesome-copilot%2Fmain%2Fagents%2Fresearch-harness-engineer.agent.md)——或把 [`adapters/copilot/copilot-instructions.md`](adapters/copilot/copilot-instructions.md) 并入 `.github/copilot-instructions.md` |
| **Gemini CLI** | 把 [`adapters/gemini/GEMINI.md`](adapters/gemini/GEMINI.md) 拷进项目根目录为 `GEMINI.md` |
| **Devin Desktop**(原 Windsurf) | `mkdir -p 你的项目/.devin/rules && cp adapters/windsurf/breakthrough-loop.md $_` —— `.windsurf/rules/` 仍作为旧路径被读取 |
| **Cline** | `mkdir -p 你的项目/.clinerules && cp adapters/cline/breakthrough-loop.md $_` |
| **Aider** | 保存 [`adapters/aider/CONVENTIONS.md`](adapters/aider/CONVENTIONS.md),用 `aider --read CONVENTIONS.md` 启动 |
| **其它一切**(OpenAI/Gemini/Anthropic 裸 API、LangChain、自研循环、或者你本人) | 粘贴 [`adapters/SYSTEM_PROMPT.md`](adapters/SYSTEM_PROMPT.md) |

所有适配器承载同一套方法论;五个纯 markdown 适配器由单一源([`adapters/_core.md`](adapters/_core.md))生成,漂移即 CI 失败。你的工具若读 `AGENTS.md`,装它或专属文件二选一,别都装;skill 与规则文件同理,每个工具只走一条路,否则规则会被加载两遍。

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

## 骨架的出处

核心主张不是民间传说;点名的系统与已知失效模式:

- **FunSearch**(Romera-Paredes 等, Nature 625, 468–475, 2024,
  [doi:10.1038/s41586-023-06924-6](https://doi.org/10.1038/s41586-023-06924-6))——程序搜索 + 自动评估器,产出数学新构造。
- **AI Co-Scientist**(Gottweis 等, Google, [arXiv:2502.18864](https://arxiv.org/abs/2502.18864), 2025)——锦标赛式假设生成/排名 + 自动评审。
- **The reusable holdout**(Dwork 等, Science 349, 636–638, 2015,
  [doi:10.1126/science.aaa9375](https://doi.org/10.1126/science.aaa9375))——反复咨询留出集为何会把它
  悄悄变成第二个校准集(`loop/` 给留出集设生命周期与预算的依据)。
- **测试集过拟合实测**(Recht 等, ICML 2019, [PMLR 97](https://proceedings.mlr.press/v97/recht19a.html))——领域尺度上测得的"增益不迁移"分布。
- **Deep learning tuning playbook**(Godbole 等, 2023, [google-research/tuning_playbook](https://github.com/google-research/tuning_playbook))——本仓库扫参规则的来源之一。

## 同一张桌子上的其他东西

- [groundwork](https://github.com/GuoCheng24/groundwork) —— 给编码 agent 用的科研流水线,第一个阶段就可能返回 NO-GO;PyPI 上名为 `groundwork-research`
- [doubleblind](https://github.com/GuoCheng24/doubleblind) —— 让 README 或论文里的每个数字都能从已提交的文件重新算出来,并给一个什么都没被告知的审稿人写简报
- [batch-logprob-gap](https://github.com/GuoCheng24/batch-logprob-gap) —— 低精度训练中,同一个 token 的 log 概率会随 batch 形状而变;这里测量了它,以及它对 GRPO 有什么影响、没有什么影响

更多见 [github.com/GuoCheng24](https://github.com/GuoCheng24)。

## 许可

MIT。用它、fork 它、反驳它。
