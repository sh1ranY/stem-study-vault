# 图像处理探索单元与兴趣教学规则 / Image exploration and interest-led teaching

2026-10-19 · Study Studio + STEM Study Vault skill

## 中文

本次增加一个完整的 ELEC270 应用单元：**去掉噪声，为什么也丢了细节？** 学生先预测，再改变图像并观察亮度曲线，随后连接卷积与频率原理，按需补基础，最后用练习与反思检验理解。

- **入口**：在 ELEC270 首页选择「开始图像探索」，或侧栏「探索图像处理」。直达路径为 `/?course=ELEC270&unit=image-filtering`。
- **中英双语**：讲解、图注、交互控件、题干、提示、解答与反馈均有配套版本。切语言保留题目和未提交输入，个人笔记保留原文。
- **交互图像实验**：原创灰度测试图，可调整噪声、平滑次数与取样行。原图、含噪图、处理结果及亮度曲线使用同一计算；页面说明周期边界与空间频率单位。
- **按需补基础**：像素信号、离散卷积、欧拉公式、频率响应、信息恢复局限。错误反馈可以指向相应讲解，再返回原题。
- **练习与记录**：四类检查，每类八个变式；保存预测、实验参数、答案草稿、反思与反馈。提示、解答和前次反馈保留为帮助记录，支持后通过不记作未经帮助的独立完成。支持续学、多窗口冲突保护和个人导出。
- **课程衔接**：保留原有系统学习路线，单元结束可进入卷积课程练习及现有文字／拍照作答流程。
- **Skill 更新**：加入兴趣与应用入口、不同类型的跨课联系、局部补基础与返回点、多媒体选择、双语一致性，以及兴趣、自评、表现和推断分开记录的规则。

普通本地版与独立演示模式都能使用这个单元，无需私人课件或 API 密钥。安装方式见 [中文说明](../../apps/study-studio/README.md)。

**验证与边界**：具体检查见 [验证记录](../../apps/study-studio/VALIDATION.md)。图像实验与自动反馈在本机运行；检查范围是数值与理由选项，文字推理只保存、不自动评分。照片识别仍属于另行主动请求的原有模型功能。本单元不代表完整图像处理课程，也尚未证明实际学习效果或长期保持。

## English

This release adds a complete ELEC270 application unit: **Less noise. Why less detail, too?** Learners predict, manipulate an image, inspect matching brightness profiles, connect the observations to convolution and frequency, open foundations when needed, and finish with checks and reflection.

- **Start** from the ELEC270 home card or **Explore image processing** in the sidebar; direct path: `/?course=ELEC270&unit=image-filtering`.
- **Bilingual throughout**: explanations, captions, controls, questions, hints, solutions and feedback. Switching language preserves question identity and unsubmitted input; personal writing retains its original language.
- **Deterministic image lab**: original grayscale patterns, reproducible noise, repeated smoothing and a selectable row. Displayed images and profiles share the same calculation, with explicit boundary and unit conventions.
- **Foundations on demand**: pixels, discrete convolution, Euler's formula, frequency response and recovery limits. Targeted feedback links to a bridge and back to the question.
- **Practice and continuation**: four families with eight variants each, saved drafts and reflection, help-aware feedback, conflict protection and personal export. The final link opens existing course practice and its typed/photo workflow.
- **Skill guidance** now covers interest-led entry points, typed cross-course relationships, local support, purposeful media, bilingual parity and separate evidence for interest, self-reports and demonstrated performance.

The unit works in normal local mode and standalone demo mode without private course files or an API key. See [installation and usage](../../apps/study-studio/GETTING_STARTED.en.md) and the [validation record](../../apps/study-studio/VALIDATION.md).

**Scope**: automatic feedback checks bounded numerical answers and selected reasons. Free-form reasoning is stored, not semantically graded. Photo recognition remains a separate, explicitly requested model feature. This is one teaching unit, not a complete image-processing course or evidence of improved learning or long-term retention.
