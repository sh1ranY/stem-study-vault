# STEM Study Vault

**把本地课件、习题和试卷，变成适合自己理解、练习和复习的 Obsidian 知识库。**

面向理工科及其他定量课程学生的 Codex skill。默认把资料写成**可作为主教材自学的讲义**：保留原课件中的实质内容，连贯解释概念、原因和联系，展开关键推导，并安排独立练习。后续可以加入新课件、补充薄弱概念，或根据自己的做题反馈调整复习路线。

[English](README.en.md) · [查看完整学习示例](examples/demo-vault/Lessons/01%20RC%20charging.md) · [检查范围](VALIDATION.md)

## 本次修订：从提纲到主教材

2026-09-22 的修订针对整门课试用中出现的内容遗漏、讲解过简和碎片化表达。新版增加了三项具体要求：

- **按实质内容核对来源**：概念、适用条件、推导、图表、不同类型的例题和子问都有去向；不能用一个同名标题宣称已经覆盖。
- **把推理写出来**：解释为什么建立这个模型、为什么可以这样变形，以及结果意味着什么。数学公式使用正常的 LaTeX 排版。
- **整门课分批写完整**：按前置关系完成有教学深度的单元，记录已完成与待完成范围，不能为了“整门课一次交付”把各章压成摘要。

可以先看 [教材级讲解样章](skills/stem-study-vault/references/teaching-standard.md)。它用普通需求、补偿需求与 Hicks 分解展示所要求的解释深度；这是原创方法示例，实际课程仍以使用者提供的资料为内容依据。篇幅与题数没有统一配额，质量要看具体内容是否被讲通。另有一次 [独立生成试跑记录](tests/results/2026-09-22-forward-test.md)：用三讲原创资料检查真实产出，记录观察结果与适用限制。

## 你会得到什么

- **一条能走下去的学习路线**：先解决什么问题、需要哪些基础、接下来练什么。
- **能跟着理解的讲解**：解释符号、条件与推导依据，必要时补足前置知识。
- **有出处的练习**：原题、改编题和自拟题分清楚；提示和解答默认折叠。
- **属于自己的积累**：保留个人笔记和学习记录，新增资料时更新受影响的内容。
- **可检查的知识库**：知识点和题目去向有记录，能检查链接和受保护文件的变化。

知识库的价值需要通过实际学习来检验。项目提供工具和工作方法；目前没有关于提分或节省时间的实测结论。

## 开始前

准备能读取本地文件的 Codex 环境，以及你的课程资料文件夹。使用 Obsidian 阅读生成的知识库，无需社区插件。辅助脚本需要 Python 3.9+；PDF/PPTX 提取的可选依赖可由 Codex 按需要配置。无需为本项目另配模型 API key。

首版输入以 PDF、PPTX、Markdown、TXT 为主。扫描件、手写页和图片需要环境中可用的视觉阅读或 OCR；旧版 `.ppt`、视频、网页接收和学校账户接入没有包含在自动提取工具中。材料不齐时仍可建出有明确范围的内容，不会假称完整覆盖课程。

## 安装

在 Codex 中发送：

```text
请使用 $skill-installer，从 https://github.com/sh1ranY/stem-study-vault
安装 skills/stem-study-vault 目录中的 skill。
```

也可以下载本仓库，将 `skills/stem-study-vault` 整个文件夹复制到用户级的 `~/.agents/skills/`，最终应存在 `~/.agents/skills/stem-study-vault/SKILL.md`。Windows 中 `~` 指你的用户主目录。若未出现，重启 Codex。

安装位置与调用方式依据 [OpenAI 官方技能文档](https://learn.chatgpt.com/docs/build-skills)。不同宿主版本可能采用不同技能管理入口；优先让内置 `$skill-installer` 处理。此仓库是独立 skill，尚未发布到插件目录。

## 第一次建库

安装后，修改下面的路径并发送给 Codex：

```text
使用 $stem-study-vault，帮我建立“电路基础”的 Obsidian 知识库。
资料在：/我的课程资料/电路基础
目标在：/我的知识库
我想系统学懂并能独立做题，学过微积分但比较生疏。
请用中文解释，保留英文术语。
已有的个人笔记请保留。先做一个可学习的单元，根据反馈再推进。
```

不用一次想清楚所有设置。Codex 会先查看资料，再询问真正缺少的信息；也可以要求直接完成资料范围明确的小课程。整门课程通常按批次推进，建设进度会保留下来，方便下一次继续。每批会把原资料中的内容与讲义正文逐项对照；尚未完成的部分保留待办状态，不算作已经讲授。

完成后，在 Obsidian 中打开目标文件夹作为知识库；如果目标已经是现有知识库，直接进入新课程的 `Course.md` 或相应课程首页。开始读一节，尝试一道题，再展开解答。目录可以适应你的现有结构。

## 先看一个无需自带课件的示例

下载本仓库后，在 Obsidian 中把 `examples/demo-vault` 作为知识库打开，从 `Start.md` 开始。它包含原创 RC 电路资料、完整推导、参数变化练习、非零初始条件迁移，以及知识和题目映射。

想试着从原始资料重新建一次，可以对 Codex 说：

```text
使用 $stem-study-vault，读取这个仓库的 examples/demo-vault/Sources/Original。
在仓库外的新文件夹创建一份 RC 电路学习知识库。
我学过导数，但对积分比较生疏。请用中文解释，安排折叠提示和解答。
不要修改演示文件，也不要把现成演示讲义直接复制过去。
```

示例仅是一份微型课程，所有内容均为项目原创，不是任何大学的官方课件或真题。GitHub 本身不会完整呈现 Obsidian 的 wiki 链接和折叠 callout；请用 Obsidian 阅读。

## 学起来之后

```text
我新增了一份讲义，请更新相关内容，并保留我的个人笔记。
```

```text
这是我做这道题的过程。请找出我最先理解错的地方，再给一道变式。
```

```text
我还有两周复习。请根据我的错题和已有资料安排复习，保留这份试卷不拆题，留作模拟。
```

默认采用系统学习路线，也可以切换为考试复习。往年试卷用于训练和理解题型，不被用来保证未来考点。只有课件时会明确标注补充练习；只有试卷时会说明课程覆盖未知。

## 内容与隐私边界

辅助脚本在本地运行，不主动联网或上传材料；Codex 读取资料仍使用你的 Codex 服务环境，因此不能理解为模型处理完全离线。使用前遵守你所在课程和环境的数据使用要求。

建库不包含公开发布你的课程资料或个人笔记。MIT 许可证覆盖本仓库的代码、文档与原创示例；你自己的课件、试卷和笔记不会因为使用此 skill 而改变原有权利归属。公开示例请只提交原创或有权再分发的材料。

## 工具与贡献

日常可以让 Codex 调用工具，无需手工操作。需要开发或验证时，在仓库根目录运行：

```sh
python3 -m pip install -r skills/stem-study-vault/scripts/requirements-extract.txt
python3 -m unittest discover -s tests -v
python3 skills/stem-study-vault/scripts/vault_tools.py check --vault examples/demo-vault
```

建议把依赖装入虚拟环境。未安装提取依赖时，PDF/PPTX 集成测试会跳过，不能据此声称提取功能已经验证。详见 [工具说明](skills/stem-study-vault/references/tools.md)。

欢迎提交能复现的使用反馈：输入材料的类型、预期学习任务、实际卡住的步骤，以及脱敏后的最小示例。改动脚本时运行相关测试；改动教学流程时用 [行为评估场景](tests/behavioral-evaluation.md) 和 [教学内容验收表](tests/teaching-rubric.md) 检查实际输出。请勿把私人课程资料直接放进 issue 或 PR。

许可证：[MIT](LICENSE)。

## Optional formula checker / 可选公式检查

A read-only KaTeX syntax checker is now included. See [usage and limitations](skills/stem-study-vault/references/tools.md#optional-formula-syntax-check). Run `npm ci`, `npm run check:math` and `npm run test:math` from this repository.
