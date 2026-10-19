# Study Studio · 本地学习空间

React 前端 + FastAPI 后端 + SQLite 数据库，将课程阅读、诊断、不同讲法、纸笔作答与个人记录接在一起。当前支持 **ELEC270、COMP201、COMP207**，可在左侧顶部「切换课程」中选择。

[English setup guide](GETTING_STARTED.en.md) · [仓库首页与 Skill](../../README.md) · [验证记录](VALIDATION.md) · [可选云端部署](DEPLOYMENT.md)

## 第一次体验：不需要私人资料或模型密钥

1. 下载本仓库 ZIP 并解压，或 `git clone https://github.com/sh1ranY/stem-study-vault.git`。
2. 安装 Python（推荐 3.12；兼容 3.9+）和 Node.js（推荐 22.12+，包含 npm）。首次安装需要联网下载依赖。
3. 进入 `apps/study-studio`，运行演示启动器：

| 系统 | 启动方式 |
|---|---|
| macOS | 双击 `demo.command`；或终端运行 `python3 start.py --demo` |
| Windows | 双击 `demo.cmd`；或 PowerShell 运行 `py -3 start.py --demo` |
| Linux | 终端运行 `python3 start.py --demo` |

浏览器会打开 **http://127.0.0.1:5177/**。保持启动窗口打开；按 Ctrl+C 停止。

启动器自动建立虚拟环境、安装依赖、初始化数据库、加入三门原创演示课并构建网页。首次进入时，创建自己的本机账号（密码至少 10 位）。**不需要 Obsidian、学校课件、邀请码、OpenAI 密钥或云端账户。** 后续账号由本机所有者在设置中生成邀请码。

演示模式使用独立的 `data-demo/`，关闭模型调用，不读取或导入你的知识库，不使用 `.env` 中的 API key 或数据库地址。它与普通本地版使用不同的会话 Cookie。内置内容是原创入门示例，不是大学官方课程或完整试卷。

安装完成后，阅读、诊断、关键答案检查、手工录入、照片保存、笔记和导出都能离线运行。演示模式不会假装识别照片：上传后请手动输入过程与关键答案。

## 五分钟体验路线

1. 在左上角选择课程，例如 COMP207。
2. 在「我的学习路线」点「检查当前起点」，或直接阅读讲义。
3. 根据需要选择补基础、图示与直觉、规则与推导。ELEC270 的斜坡另有交互图形和三步引导教学。
4. 写下解题过程，填写数值或选择答案。也可先纸笔作答，再上传 JPEG、PNG 或 WebP 照片（不超过 10 MB）。
5. 核对过程与关键答案，勾选确认后提交。看过解答或用了外部帮助，请如实标记；提示后的同题改正不作为新题独立证据。
6. 在「我的学习记录」回看反馈；在「设置与导出」导出**当前课程**的 ZIP。

草稿自动保存，切换课程前还会保存当前单元笔记。关闭/刷新页面前请确认草稿显示已保存；一般讲义切换前用「保存并记住当前位置」保存笔记。切换课程不会清空其他课程的记录。

右上角可切换简体中文与 English；界面、原创练习与演示讲义支持双语。导入的个人资料保留原语言，不会自动翻译。选择教学路径不会把你归类为固定的学习风格。

## ELEC270 图像处理探索

在 ELEC270 首页点击「开始图像探索」，或在侧栏选择「探索图像处理」。也可直接打开 `/?course=ELEC270&unit=image-filtering`。普通本地版和原创演示模式都包含这个单元，无需导入私人资料。

学习流程为：预测 → 交互图像实验 → 原理与按需补基础 → 四类小检查 → 回看与课程练习。实验使用原创灰度测试图、固定噪声和三点平滑，图像与亮度曲线来自同一计算；边界处理与空间频率单位在页面说明。像素、卷积、欧拉公式、频率和恢复局限可随时展开。界面、正文、图注、提示、解答及反馈均提供中英版本。

进度、实验参数、预测、反思与练习草稿按账号保存；切换语言保留题目身份。四类检查分别涉及局部平滑、频率与细节、时间信号迁移、恢复的非唯一性，每类最多八个有界变式。数值与理由选择由本机核查，自由文字只保存供复看；这些检查不证明完整课程掌握或延迟保持。提示、解答及前次反馈的使用被保留，后续同类变式不会重新计为未经帮助的独立表现。

本单元不调用 AI。最后的「课程练习」入口连接现有卷积练习及纸笔照片流程；只有另行主动请求照片识别或 AI 过程反馈时才可能调用已配置的模型。个人导出包含本单元的活动与作答记录。刷新或关闭前，请确认保存成功。

## 当前课程覆盖

| 课程 | 内置可检查主题 | 自己导入后 |
|---|---|---|
| ELEC270 · 信号与系统 | 斜坡构造、矩形卷积、Fourier 归一化 | 阅读与搜索自己的各单元及课件 |
| COMP201 · 软件工程 I | 需求与验收条件、Petri 网、边界值测试 | 阅读与搜索软件过程、需求、设计、测试等原知识库内容 |
| COMP207 · 数据库开发 | JOIN 与 COUNT、WHERE/GROUP BY/HAVING、冲突可串行化 | 阅读与搜索关系模型、事务、恢复、分布式等原知识库内容 |

每个主题包含诊断、新练习与复查题，每类最多 24 个有界变式；变式不等同于考核覆盖或教学难度递进。自动判据只检查指定答案；自由文字、任意 SQL、程序、类图与完整证明不在确定性自动评分范围内。AI 过程反馈是另外标注的建议，不能据此认证整门课掌握或长期保持。

## 正常本地使用与可选 AI

运行 `python3 start.py`（Windows：`py -3 start.py`），或双击 `start.command` / `start.cmd`。普通本地版地址为 **http://127.0.0.1:8765/**，默认数据在 `data/`；已有课程和学习记录会保留，仅为尚未安装的课程加入演示。

如果需要真实照片识别与 AI 过程反馈：

1. 仅当 `.env` 尚不存在时，将 `.env.example` 复制为 `.env`。
2. 在本机填写 `OPENAI_API_KEY` 与你账号可用、支持图像及结构化输出的 `STUDIO_VISION_MODEL`。
3. 停止并重新启动普通本地版。不要使用 `--demo`，它会强制关闭 AI。

密钥只留在后端，不写进浏览器变量、聊天或 Git。只有主动点击照片转写/AI反馈时才发起模型请求，课程导入不会调用模型。每次操作最多一次请求，不自动重试；默认每账号每天 UTC 30 次调用。这不是金额上限，API 使用可能产生费用。识别后仍需本人确认。

## 接入自己的 Obsidian 课程

先完成正常本地启动并停止服务。准备下面的目录；`Weeks/` 可以包含学年子目录，讲义文件建议命名为 `Week 01 - 标题.md`。

```text
自己的课程/
  Weeks/
    Week 01 - 标题.md
    Week 02 - 标题.md
  Sources/                  # 可选 PDF/PPTX/DOCX 等附件
  Practice/                 # 可选旧错题记录（不计入掌握证据）
```

macOS / Linux（Windows 把 `.venv/bin/python` 换成 `.venv\Scripts\python.exe`）：

```sh
.venv/bin/python -m backend.pilot.import_course --course COMP201 --course-root "/absolute/path/to/自己的课程" --desktop "/absolute/path/to/原课件"
```

`--course` 可选 `ELEC270`、`COMP201`、`COMP207`。`--desktop` 可省略；省略时仅尝试本机 `~/Desktop/<课程代码> 课程资料`，不存在也可只导入 Markdown。

如果知识库使用本项目原有目录约定，也可以：

```sh
.venv/bin/python -m backend.pilot.import_course --course COMP207 --vault "/absolute/path/to/Obsidian" --desktop "/absolute/path/to/COMP207资料"
```

对应路径为 `10 Y2上学期/ELEC270 信号与系统`、`10 Y2上学期/COMP201 软件工程 I`、`10 Y2上学期/COMP207 数据库开发`。查看命令输出的单元数、附件数和链接警告，重启服务后选择课程。

导入只读取原件，附件复制到应用自己的数据目录；同一内容重复导入不会创建重复版本。新导入替换该课程的当前版本，已有题目继续引用原版本，其他课程不受影响。导入器支持本项目常用的 Wiki 链接/嵌入/提示框，不是完整 Obsidian 解析器。`hint`、`solution`、`answer`、`success` 等指定提示框可单独展开；普通正文或下载的原件仍可能含答案，不能把隐藏提示框视为全面答案检测。

**导入自己的文件不等于自动生成新课程的诊断题库。** 任意科目、自助建课与自动题库编写尚未提供；当前自动检查仍限定上述九个原创主题。需要先生成系统讲义时，可使用仓库中的 [stem-study-vault Skill](../../skills/stem-study-vault/SKILL.md)。

## 数据与备份

- `data/`：本地课程副本、数据库、笔记、作答、照片。`data-demo/`：演示账号与记录。两者及 `.env` 都被 Git 和容器构建排除。
- 学习记录按账号保存，课程选择按账号记忆；每个浏览器页的课程请求有明确课程代码，避免多页切换混淆。
- 「导出」只包含当前课程，含 Obsidian Markdown、照片、原始 JSON 与 Skill V1 学习记录，不包含题目解答。清空账号前分别导出需要的课程。
- 「删除我的数据」会删除该账号**所有课程**的个人记录，保留账号与共享课程。
- 完整备份请在服务停止时运行：

```sh
.venv/bin/python -m backend.backup create --data data --output /absolute/path/private-backup.zip
.venv/bin/python -m backend.backup restore --archive /absolute/path/private-backup.zip --destination /absolute/path/restored-data
```

恢复要求一个尚不存在的目录。之后把 `.env` 的 `STUDIO_DATA_DIR` 指向恢复目录；若原来配置过 `STUDIO_DATABASE_URL`，同步修改或删除该项，再重新启动。恢复后需要重新登录。备份包含私人资料，请勿提交到公开仓库。该备份命令针对 SQLite；PostgreSQL 需要独立备份方案。

## 常见问题

- **提示没有 Python/npm**：安装对应运行环境，再打开新的终端重试。Windows 使用 `py -3`；只有 `python` 命令时可直接运行 `python start.py --demo`。
- **macOS 不允许双击启动**：可在终端进入此目录，执行 `python3 start.py --demo`。
- **端口被占用**：先停止旧启动窗口，再启动新版本。程序不会悄悄沿用旧服务。
- **安装失败**：保留终端报错，检查网络连接；下次运行会重试尚未完成的安装。
- **AI待配置**：演示模式下是预期行为。照片和手工作答仍可用。
- **手机打不开 127.0.0.1**：它指向手机自己。这一版只监听当前电脑，未启用跨设备托管。
- **更新后看不到切换入口**：停止旧服务，重新运行启动器并刷新页面。

## 开发与架构

```text
src/                         React UI、课程选择、阅读、草稿、记录
backend/pilot/catalog.py      课程注册、选课、按课程筛选记录
backend/pilot/import_course.py 只读导入与版本化附件
backend/pilot/demo_course.py  三门原创演示种子，不覆盖导入内容
backend/pilot/teaching.py     ELEC270 判据与统一题目接口
backend/pilot/computing.py    COMP201 / COMP207 双语内容与判据
backend/pilot/localization.py 展示翻译，保持题目/证据身份
backend/pilot/routes.py       登录、课程、作答、照片、导出 API
backend/pilot/store.py        SQLAlchemy 记录存储；本地默认 SQLite
```

```sh
.venv/bin/python -m unittest discover -s tests -v
npm run build
python3 start.py --demo --prepare-only
```

测试隔离数据库并模拟模型响应。SQL 题的判据另外对照实际 SQLite 查询结果；测试通过不证明 AI 转写质量或教学有效性。Windows 启动脚本已提供，但本轮现场验证平台为 macOS，Linux 由 CI 验证，Windows 仍需原生环境试用。

保留的早期原型位于 `/?prototype=1`，账号建立后仅所有者可访问；它不是多课程主入口。云端配置保留供以后使用，本地启动不会自动部署、开通付费服务或建立计费。PostgreSQL/Supabase 并未作为本次已验证的部署方案。
