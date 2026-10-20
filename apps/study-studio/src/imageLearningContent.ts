export type BridgeId =
  "pixels" | "convolution" | "euler" | "frequency" | "recovery";
export type Bridge = {
  id: BridgeId;
  title: string;
  relation: string;
  reason: string;
  body: string;
  check: string;
  answer: string;
};
const raw = String.raw;
const zh = {
  eyebrow: "探索应用 · ELEC270 × 图像处理",
  title: "去掉噪声，为什么也丢了细节？",
  subtitle:
    "从一张自己能操作的图片，走到像素、卷积与频率。理解一次工程选择背后的得与失。",
  stages: ["先提出问题", "亲手观察", "解释与补基础", "独立检查", "应用与回看"],
  intro:
    "你正在做一个相机应用。照片有噪声，用户却还想看清小字和细纹。把图像平滑一点会怎样？这次先预测，再用同一份像素数据检验。",
  goals: [
    "把图像的一行读成亮度信号",
    "解释平滑对细节与噪声的取舍",
    "计算三点滤波，并把观察连接到课程公式",
  ],
  limits:
    "本单元：原创灰度图、简单线性滤波与空间频率。操作完成与题目通过分别记录；不代表已掌握完整图像处理或傅里叶理论。",
  start: "开始这个单元",
  resume: "继续学习",
  loading: "正在读取学习位置…",
  save: "已保存",
  saving: "正在保存…",
  saveError: "保存尚未确认，请查看下方提示",
  retry: "重试保存",
  reload: "使用已保存版本（替换未保存编辑）",
  back: "上一步",
  next: "下一步",
  stage: "学习阶段",
  predictionLabel: "先写下你的预测",
  predictionPlaceholder:
    "平滑更强时，噪声、小字的边缘和细条纹会分别怎样？你最想保留什么？",
  predictionNote:
    "这是你的起点，不计分，也不要求现在就答对。可以之后回来对照。",
  predictionQuestion: "如果噪点变少了，这张图一定更有用吗？",
  labTitle: "让眼睛的判断，遇到可测量的变化",
  labIntro:
    "选择图案、添加固定的噪声，再增加平滑次数。移动取样行，比较同一位置的三条亮度曲线。先观察细条纹，再看字形边缘。",
  scene: "边缘与粗细条纹",
  stripes: "两种频率的正弦条纹",
  pattern: "测试图案",
  passes: "平滑次数",
  row: "取样行",
  noise: "噪声幅度",
  clean: "原创基准图",
  noisy: "含噪输入",
  filtered: "处理结果",
  zero: "0 次表示保持含噪输入不变。",
  imageAlt: "96 × 96 灰度测试图；彩色横线标记亮度曲线的取样行。",
  profile: "同一行的亮度曲线",
  position: "横向位置（像素）",
  brightness: "亮度",
  table: "查看数值样本（每隔 8 个像素）",
  sample: "像素位置",
  method:
    "每次平滑先逐行、再逐列使用 [¼, ½, ¼]。边界使用周期延拓：图像左右及上下相接。含噪输入裁剪到 [0, 1]；噪声由固定种子生成，改参数时可以公平比较。取样行来自当前显示的完整二维结果。",
  observeTitle: "试三个小实验",
  experiments: [
    "噪声设为 0：增加平滑次数。清晰的细条纹也会减弱吗？",
    "切换正弦条纹：左边周期为 12 像素，右边为 4 像素。哪一侧更快变平？",
    "回到边缘图：把取样行移过字形。边缘过渡如何改变？",
  ],
  labMeaning:
    "图像亮度沿空间变化，而音频幅度沿时间变化。这里的频率是每像素多少周，不是每秒多少赫兹。高频可以是噪声，也可以是你希望保住的纹理。",
  theoryTitle: "一次局部平均，为什么会挑选频率？",
  core: raw`把某一行记为 $x[n]$。三点滤波让每个输出像素接收左右邻居各四分之一、当前位置二分之一：

$$y[n]=\tfrac14x[n-1]+\tfrac12x[n]+\tfrac14x[n+1].$$

例如相邻亮度为 $0.2,\;0.8,\;0.4$，中心输出是 $0.25\times0.2+0.5\times0.8+0.25\times0.4=0.55$。系数之和为 1，所以常量亮度不会改变。边缘两边的亮度被混合，过渡会变宽。

对复指数输入 $x[n]=e^{j\omega n}$，三个移位共享同一个 $e^{j\omega n}$ 因子：

$$H(e^{j\omega})=\tfrac14e^{-j\omega}+\tfrac12+\tfrac14e^{j\omega}=\tfrac12+\tfrac12\cos\omega=\cos^2(\omega/2).$$

令空间频率为 $f$（周/像素），则 $\omega=2\pi f$。在 $0\le f\le 0.5$ 上，变化越快，增益越小。这描述的是**幅度比**，不直接等同于所有图片的“质量”。`,
  frequencyPlot: "一次三点滤波的幅度增益",
  frequencyAxis: "空间频率（周/像素）",
  gain: "幅度增益",
  frequencyCaption:
    "常量 f = 0 保持不变；f = 0.25 的振幅变为一半；逐像素交替的 f = 0.5 成分被完全消去。曲线是滤波器公式，不是当前图片的频谱。",
  twoD: raw`图像演示把同一个滤波器沿两个轴分别应用。对周期延拓的二维复指数，单次增益为 $H(\omega_x)H(\omega_y)$；重复 $p$ 次后为 $[H(\omega_x)H(\omega_y)]^p$。一行曲线只展示这张二维图的一部分，不能代替完整二维分析。这里使用离散信号的空间频率响应，与离散时间系统共享数学结构；它不是 FFT，也不是连续傅里叶变换。`,
  bridgesTitle: "卡在哪一步，就在这里补一座桥",
  bridgesIntro:
    "随时展开；回顾和推导都可访问。打开基础不会把你归为某一类学生，也不会自动记为掌握。",
  checkTitle: "换一个情境，检验自己的判断",
  checkIntro:
    "每题都有数值与理由选择。可写关键步骤；当前自动反馈只核对数值和理由选项，不评分自由文字。先试一次，再按需查看提示。读过帮助后的通过会单独标记。",
  number: "数值答案",
  choose: "选择理由",
  working: "关键步骤（可选，暂不自动评分）",
  submit: "检查这次作答",
  hint: "给我一点提示",
  solution: "查看完整解答",
  fresh: "换一道检验题",
  hintTitle: "提示",
  solutionTitle: "解答",
  numberError: "请填写数值或简单算式（如 1/4），并选择一个理由。",
  checked: "这道题的判据已通过",
  supported: "使用帮助后通过",
  needsReview: "还需要核对",
  notChecked: "尚未检查",
  assessmentLimit:
    "这些是有限目标的检查，不是课程总评分。阅读、兴趣与独立表现互不替代。",
  recommend: "建议先看：",
  noFresh: "本组变式已用完；可回看过程或进入课程练习。",
  finishTitle: "从滤镜参数，走向工程判断",
  finishIntro:
    "没有一种平滑强度对所有任务都最好。决定要保护什么，再选择处理方式，并在真实条件下检验。",
  lenses: [
    {
      title: "CSEE · 图像算法",
      body: "为文字识别准备图像：降噪与保住笔画哪个更紧迫？比较同一输入、明确边界条件，并记录参数，才能复现结果。",
    },
    {
      title: "机电 · 机器人视觉",
      body: "机器人靠边缘定位目标：平滑可能减少噪声，也可能改变边缘位置的估计。把定位误差和运行速度一起检验；这里没有模拟运动模糊。",
    },
    {
      title: "EEE · 成像信号链",
      body: "噪声从传感器到后处理都可能产生。先区分采样、噪声与滤波：增加平滑不能保证恢复采集时已经丢失的细节。",
    },
  ],
  crossCourse:
    "连接其他课：COMP201 可把“看清小字”写成可验收需求与测试；COMP207 可保存图像版本、参数和来源。这是项目中的应用联系，不是它们的正式先修关系。",
  reflection: "用自己的话收尾",
  reflectionPlaceholder:
    "现在你会怎样回答最初的问题？你愿意继续探索什么？如果要保住细小文字，你会怎样检验处理是否有用？",
  reflectionNote: "这份自述用于回看兴趣与判断，不作为理解已被验证的证据。",
  coursePractice: "进入 ELEC270 课程练习",
  courseNote:
    "继续练习卷积与频率相关题目，可使用现有文字或纸笔拍照流程。返回本单元时保留学习位置。",
  recap: "本单元检查记录",
  independent: "独立检查通过",
  open: "待检查或需复查",
  source:
    "文本、测试图与交互由本项目原创。无课程图片上传，也无需模型调用。内容版本：",
  returnToTheory: "回到当前解释",
  miniCheck: "停一下，自己想一想",
  showAnswer: "查看这个补桥问题的解释",
  bridges: [
    {
      id: "pixels",
      title: "像素、亮度与一行信号",
      relation: "必要前置 · 离散信号",
      reason: "用于把图像中的细节转换为能计算的输入。",
      body: raw`灰度图是一个二维数组 $I[r,c]$。本例用 0 表示黑、1 表示白；它是归一化的亮度模型，不是完整的相机物理模型。8 位灰度也常用 0–255 表示；除以 255 可转换到本例的归一化标度。固定一行 $r=r_0$，就得到 $x[n]=I[r_0,n]$。

常量行没有亮暗变化。正弦条纹可写成 $x[n]=c+A\cos(2\pi fn+\phi)$：$c$ 是平均亮度，$A$ 决定对比度，$f$ 决定疏密，$\phi$ 决定条纹位置。它们是不同参数。周期 $T$ 的单位是像素/周，$f=1/T$。`,
      check: "一条亮度曲线每 8 个像素重复一次，空间频率是多少？",
      answer: "f = 1/8 = 0.125 周/像素。它不是 8 Hz；横轴是空间位置。",
    },
    {
      id: "convolution",
      title: "为什么要移位、相乘、再求和？",
      relation: "必要前置 · 离散卷积",
      reason: "用于解释局部平均怎样从输入得到输出。",
      body: raw`线性移不变系统把每个输入样本的贡献叠加，写作 $y[n]=\sum_k h[k]x[n-k]$。这里 $h[-1]=1/4,\ h[0]=1/2,\ h[1]=1/4$，其他系数为零。

固定一个输出位置，先找到对应邻居，再按各自权重相乘，最后求和。核在本例中对称，所以与直接的邻域加权平均相同；一般非对称核的卷积需要注意翻转，不能忽略索引。

像素越界时还需要约定。本演示用周期延拓：第 0 列左邻居是第 95 列。真实软件也可能使用镜像或补零，这会改变边缘结果。`,
      check: "如果三个输入样本都等于 c，输出是多少？为什么这个检查有用？",
      answer:
        "输出为 (1/4 + 1/2 + 1/4)c = c。它检查直流增益是否为 1；这个滤波器不会整体改变常量亮度。",
    },
    {
      id: "euler",
      title: "欧拉公式怎样把旋转连接到滤波？",
      relation: "推导依据 · 复数与工程数学",
      reason: "用于理解频率响应中的复指数，不要求先读完整章数学。",
      body: raw`复数 $a+jb$ 可画成平面上的点。单位圆上的角度 $\theta$ 对应 $\cos\theta+j\sin\theta$。欧拉公式是 $e^{j\theta}=\cos\theta+j\sin\theta$；这里 $j^2=-1$。

展开两边的幂级数：$e^{j\theta}=1+j\theta-\theta^2/2!-j\theta^3/3!+\cdots$。偶次项组成 $\cos\theta$，奇次项组成 $j\sin\theta$。这些级数对所有实数 $\theta$ 收敛。

于是 $e^{j\theta}+e^{-j\theta}=2\cos\theta$。滤波时，移位只给复指数乘上一个因子：$e^{j\omega(n-k)}=e^{j\omega n}e^{-j\omega k}$。提取公共因子后，剩下的加权和就是 $H(e^{j\omega})$。

这解释一个复指数如何通过该滤波器。完整 Fourier 分解还需要系数、正交性和适用条件，不能仅由欧拉公式一句话完成。`,
      check: "为什么对称的两个指数相加后，虚部消失？",
      answer:
        "因为 sin(−θ) = −sin(θ)，两个虚部相消，而 cos(−θ) = cos(θ)，实部相加为 2 cos θ。",
    },
    {
      id: "frequency",
      title: "空间频率与频率响应",
      relation: "共同结构 · 信号与系统",
      reason: "用于把细条纹减弱连接到定量的幅度变化。",
      body: raw`周期为 $T$ 像素的条纹有 $f=1/T$ 周/像素，角频率为 $\omega=2\pi f$ 弧度/像素。对本例在周期边界下的单一频率，输出振幅等于输入振幅乘以 $H=\cos^2(\pi f)$。

例如 $f=1/6$ 时，$H=\cos^2(\pi/6)=3/4$。振幅为 0.2 的条纹经过一次水平方向滤波后振幅为 0.15；平均亮度不变。若图像沿竖直方向恒定，竖直滤波的增益为 1。

回到时间采样：若采样率为 $f_s$ 样本/秒，同一角频率的基带代表为 $f_{\mathrm{Hz}}=(\omega/2\pi)f_s=f_s/T$，其中 $T$ 是每周期的样本数。例如 $T=10$、$f_s=2000$ 时，频率是 200 Hz。这里只取基带代表；由于混叠，样本不能唯一确定所有可能的连续时间频率。图像的周/像素不能直接写成 Hz。

高频描述变化快，不描述好坏。头发、笔画与噪声都可能包含高频。频率响应描述系统；频谱描述输入含有哪些成分，二者不要混淆。`,
      check: "一幅没有任何噪声的细条纹图，经平滑后会不会丢失对比度？",
      answer:
        "会。只要该频率的增益小于 1，条纹振幅就会减小。滤波器不会因为它是有用的细节就自动保留。",
    },
    {
      id: "recovery",
      title: "锐化为什么不等于找回原图？",
      relation: "深入探索 · 信息与可逆性",
      reason: "用于判断“更清楚”和“恢复信息”之间的区别。",
      body: raw`一种锐化方式是 $s=z+\alpha(z-b)$：$z$ 是当前输入，$b$ 是对它再平滑的结果，$\alpha\ge0$。它增加高频残差，可能同时增强噪声并产生过冲；显示时裁剪还会改变结果。它没有偷偷使用原来的清晰图。

考虑偶数长度的周期序列：$x_1[n]=c$ 与 $x_2[n]=c+a(-1)^n$，取 $c=0.5,\ a=0.2$，亮度都合法。三点滤波对 $f=0.5$ 的增益为 0，所以两个不同输入都变成常量 $c$。

只看相同的输出，不能唯一确定哪一个原图曾经输入。这不是算得不够精确，而是这个处理丢掉了区分它们的信息。更强的先验可能猜测原图，但不保证猜中。`,
      check: "如果平滑结果都是 0.5，锐化程序能仅凭它证明原图含有交替条纹吗？",
      answer:
        "不能。常量图和交替条纹都能产生这个结果。没有额外信息，就不能唯一确定输入；提高对比度不构成恢复证明。",
    },
  ] as Bridge[],
};
const en: typeof zh = {
  eyebrow: "EXPLORE AN APPLICATION · ELEC270 × IMAGE PROCESSING",
  title: "Less noise. Why less detail, too?",
  subtitle:
    "Start with an image you can change. Connect pixels, convolution and frequency to a real engineering trade-off.",
  stages: [
    "Ask & predict",
    "Try the image lab",
    "Explain & connect",
    "Check independently",
    "Apply & reflect",
  ],
  intro:
    "You are building a camera app. A photograph is noisy, but the user still needs small lettering and fine texture. What happens if you smooth the image? Predict first, then test your idea against the same pixel data.",
  goals: [
    "Read one image row as a brightness signal",
    "Explain the trade-off between noise and useful detail",
    "Calculate a three-point filter and connect the observation to course mathematics",
  ],
  limits:
    "Scope: original grayscale images, simple linear filtering and spatial frequency. Exploration and successful checks are recorded separately; neither demonstrates mastery of all image processing or Fourier theory.",
  start: "Start this unit",
  resume: "Continue learning",
  loading: "Loading your learning position…",
  save: "Saved",
  saving: "Saving…",
  saveError: "Save not confirmed; see the message below",
  retry: "Retry saving",
  reload: "Use saved version (replace unsaved edits)",
  back: "Previous",
  next: "Next",
  stage: "Learning stages",
  predictionLabel: "Write your prediction first",
  predictionPlaceholder:
    "As smoothing increases, what happens to noise, letter edges and fine stripes? What would you most want to preserve?",
  predictionNote:
    "This is your starting idea, not a graded answer. You can return to compare it with your explanation.",
  predictionQuestion:
    "If there are fewer noisy pixels, is the image necessarily more useful?",
  labTitle: "Connect what you see to what you can measure",
  labIntro:
    "Choose a pattern, add reproducible noise, then increase smoothing. Move the selected row and compare three brightness profiles at exactly the same location. Start with fine stripes, then examine the letter-like edges.",
  scene: "Edges, coarse and fine stripes",
  stripes: "Two sinusoidal stripe frequencies",
  pattern: "Test pattern",
  passes: "Smoothing passes",
  row: "Selected row",
  noise: "Noise amplitude",
  clean: "Original reference",
  noisy: "Noisy input",
  filtered: "Filtered output",
  zero: "0 passes leaves the noisy input unchanged.",
  imageAlt:
    "96 × 96 grayscale test image; the coloured line marks the row used in the brightness profile.",
  profile: "Brightness profiles of the same row",
  position: "Horizontal position (pixels)",
  brightness: "Brightness",
  table: "Inspect numerical samples (every 8 pixels)",
  sample: "Pixel position",
  method:
    "Each pass applies [¼, ½, ¼] along rows, then columns. Boundaries are periodic: opposite image edges join. Noisy input values are clipped to [0, 1]. Noise uses a fixed seed for fair comparisons. The selected row comes from the full two-dimensional output shown above.",
  observeTitle: "Try three small experiments",
  experiments: [
    "Set noise to 0 and add smoothing. Do clean, fine stripes lose contrast too?",
    "Choose sinusoidal stripes: the left half has a period of 12 pixels; the right has a period of 4. Which fades faster?",
    "Return to the edge pattern and move the selected row through the letter-like shape. How does an edge transition change?",
  ],
  labMeaning:
    "Image brightness varies across space; audio amplitude varies over time. Frequency here means cycles per pixel, not hertz. High frequencies can represent noise or valuable texture.",
  theoryTitle: "Why does a local average treat frequencies differently?",
  core: raw`Represent one row as $x[n]$. A three-point filter gives the central sample half the weight and each neighbour a quarter:

$$y[n]=\tfrac14x[n-1]+\tfrac12x[n]+\tfrac14x[n+1].$$

For adjacent brightness values $0.2,\;0.8,\;0.4$, the central output is $0.25\times0.2+0.5\times0.8+0.25\times0.4=0.55$. The weights sum to 1, so a constant brightness is unchanged. Mixing brightness values across an edge spreads the transition.

For the complex exponential $x[n]=e^{j\omega n}$, all three shifted samples share a factor $e^{j\omega n}$:

$$H(e^{j\omega})=\tfrac14e^{-j\omega}+\tfrac12+\tfrac14e^{j\omega}=\tfrac12+\tfrac12\cos\omega=\cos^2(\omega/2).$$

With spatial frequency $f$ in cycles/pixel, $\omega=2\pi f$. For $0\le f\le0.5$, faster variation receives a smaller gain. This is an **amplitude ratio**, not a universal measure of image quality.`,
  frequencyPlot: "Amplitude gain of one three-point filtering pass",
  frequencyAxis: "Spatial frequency (cycles/pixel)",
  gain: "Amplitude gain",
  frequencyCaption:
    "A constant (f = 0) is unchanged; at f = 0.25 the amplitude halves; alternating pixels (f = 0.5) are eliminated. This curve describes the filter, not the spectrum of the current image.",
  twoD: raw`The image lab applies the same filter along both axes. For a two-dimensional complex exponential with periodic boundaries, one pass has gain $H(\omega_x)H(\omega_y)$; after $p$ passes it is $[H(\omega_x)H(\omega_y)]^p$. A row profile shows only part of this two-dimensional image. This is a discrete-signal spatial frequency response, sharing the mathematics of discrete-time systems. It is not an FFT or a continuous Fourier transform.`,
  bridgesTitle: "Build the bridge you need, right here",
  bridgesIntro:
    "Open a quick reminder or a derivation whenever it helps. Using a bridge does not assign you a learning type or automatically establish understanding.",
  checkTitle: "Try a new case without following the example",
  checkIntro:
    "Each check asks for a number and a reason. You may record your working; automatic feedback currently checks only the number and reason selection, not free text. Try first, then reveal help if needed. Success after help is recorded separately.",
  number: "Numerical answer",
  choose: "Choose a reason",
  working: "Key steps (optional; not automatically graded)",
  submit: "Check this answer",
  hint: "Give me a hint",
  solution: "Show the full solution",
  fresh: "Try another check",
  hintTitle: "Hint",
  solutionTitle: "Solution",
  numberError:
    "Enter a number or simple arithmetic (such as 1/4), and select a reason.",
  checked: "This question’s criteria are met",
  supported: "Passed after using help",
  needsReview: "Needs another look",
  notChecked: "Not yet checked",
  assessmentLimit:
    "These checks cover limited objectives, not the whole course. Reading, interest and independent performance are separate evidence.",
  recommend: "Suggested bridge:",
  noFresh:
    "You have used the available variants. Review your working or continue to course practice.",
  finishTitle: "From filter settings to engineering decisions",
  finishIntro:
    "No smoothing strength is best for every task. Decide what matters, choose a method, and test the trade-off under the conditions that matter to your application.",
  lenses: [
    {
      title: "CSEE · Image algorithms",
      body: "Prepare an image for text recognition: which matters more, reducing noise or preserving thin strokes? Use the same input, specify boundaries and save parameters so the result is reproducible.",
    },
    {
      title: "Mechatronics · Robot vision",
      body: "A robot locates objects using edges. Smoothing may reduce noise but alter the estimated edge location. Test localisation error alongside processing speed; this lab does not model motion blur.",
    },
    {
      title: "EEE · Imaging signal chains",
      body: "Noise can enter at the sensor and during processing. Distinguish sampling, noise and filtering: more smoothing cannot guarantee recovery of detail lost during acquisition.",
    },
  ],
  crossCourse:
    "Connections to other courses: COMP201 can turn “read small lettering” into testable requirements; COMP207 can store image versions, parameters and provenance. These are project connections, not claims about formal prerequisites.",
  reflection: "Close the loop in your own words",
  reflectionPlaceholder:
    "How would you answer the opening question now? What would you explore next? If small lettering matters, how would you test whether processing helped?",
  reflectionNote:
    "This reflection records your interests and reasoning for later review. It is not proof of demonstrated understanding.",
  coursePractice: "Continue to ELEC270 course practice",
  courseNote:
    "Continue with convolution and frequency-related questions using the existing typed or photographed paper-work flow. Your position in this unit is retained.",
  recap: "Checks in this unit",
  independent: "Independent checks passed",
  open: "Not checked or needs review",
  source:
    "Original text, test images and interactions created for this project. No course images are uploaded and no model call is needed. Content version:",
  returnToTheory: "Return to the explanation",
  miniCheck: "Pause and think",
  showAnswer: "See the explanation for this bridge check",
  bridges: [
    {
      id: "pixels",
      title: "Pixels, brightness and a row signal",
      relation: "Prerequisite · Discrete signals",
      reason:
        "Connect a visible image feature to an input you can calculate with.",
      body: raw`A grayscale image is a two-dimensional array $I[r,c]$. Here 0 represents black and 1 white: a normalised brightness model, not a complete physical camera model. An 8-bit grayscale representation commonly uses 0–255; divide by 255 to obtain this normalised scale. Fix a row $r=r_0$ to obtain $x[n]=I[r_0,n]$.

A constant row has no brightness variation. Sinusoidal stripes can be written as $x[n]=c+A\cos(2\pi fn+\phi)$: $c$ sets mean brightness, $A$ sets contrast, $f$ sets stripe density, and $\phi$ sets position. These are different parameters. A period $T$ has units of pixels/cycle, with $f=1/T$.`,
      check:
        "A brightness profile repeats every 8 pixels. What is its spatial frequency?",
      answer:
        "f = 1/8 = 0.125 cycles/pixel. It is not 8 Hz: the horizontal axis represents position, not time.",
    },
    {
      id: "convolution",
      title: "Why shift, multiply and add?",
      relation: "Prerequisite · Discrete convolution",
      reason: "Explain how a local average turns input samples into an output.",
      body: raw`A linear, shift-invariant system adds contributions from input samples: $y[n]=\sum_k h[k]x[n-k]$. Here $h[-1]=1/4,\ h[0]=1/2,\ h[1]=1/4$, with all other coefficients zero.

At each output location, identify the corresponding neighbours, multiply by their weights and add. This kernel is symmetric, so the calculation matches a direct weighted neighbourhood average. With a general asymmetric kernel, convolution requires careful indexing and reversal.

Out-of-range pixels require a boundary convention. This lab uses periodic extension: the left neighbour of column 0 is column 95. Other software may reflect the image or pad with zeros, changing edge results.`,
      check:
        "If all three input samples equal c, what is the output? Why is this a useful check?",
      answer:
        "The output is (1/4 + 1/2 + 1/4)c = c. This checks that the DC gain is 1: the filter preserves constant brightness.",
    },
    {
      id: "euler",
      title: "How does Euler’s formula connect rotation to filtering?",
      relation: "Derivation · Complex numbers and engineering mathematics",
      reason:
        "Understand the complex exponentials in the response without rereading a whole mathematics chapter.",
      body: raw`A complex number $a+jb$ is a point in a plane. Angle $\theta$ on the unit circle gives $\cos\theta+j\sin\theta$. Euler’s formula is $e^{j\theta}=\cos\theta+j\sin\theta$, where $j^2=-1$.

Expand the power series: $e^{j\theta}=1+j\theta-\theta^2/2!-j\theta^3/3!+\cdots$. The even powers form $\cos\theta$; the odd powers form $j\sin\theta$. These series converge for every real $\theta$.

Hence $e^{j\theta}+e^{-j\theta}=2\cos\theta$. A shift multiplies a complex exponential by a factor: $e^{j\omega(n-k)}=e^{j\omega n}e^{-j\omega k}$. Factor out the common exponential; the remaining weighted sum is $H(e^{j\omega})$.

This explains how one complex exponential passes through the filter. A complete Fourier decomposition also requires coefficients, orthogonality and applicability conditions; Euler’s formula alone is not a derivation of the full transform.`,
      check:
        "Why do the imaginary parts cancel when these two symmetric exponentials are added?",
      answer:
        "Because sin(−θ) = −sin(θ), their imaginary parts cancel; cos(−θ) = cos(θ), so the real parts add to 2 cos θ.",
    },
    {
      id: "frequency",
      title: "Spatial frequency and frequency response",
      relation: "Shared structure · Signals and systems",
      reason:
        "Connect fading fine stripes to a quantitative change in amplitude.",
      body: raw`Stripes with period $T$ pixels have $f=1/T$ cycles/pixel and angular frequency $\omega=2\pi f$ radians/pixel. For a single frequency compatible with the periodic boundaries, output amplitude equals input amplitude times $H=\cos^2(\pi f)$.

For $f=1/6$, $H=\cos^2(\pi/6)=3/4$. Stripes of amplitude 0.2 therefore have amplitude 0.15 after one horizontal pass; mean brightness is unchanged. If the image is constant vertically, the vertical filter has gain 1.

For time sampling at $f_s$ samples/second, the corresponding baseband frequency is $f_{\mathrm{Hz}}=(\omega/2\pi)f_s=f_s/T$, where $T$ is the number of samples per cycle. For $T=10$ and $f_s=2000$, this is 200 Hz. We choose the baseband representative: aliasing means the samples do not uniquely identify all possible continuous-time frequencies. Cycles/pixel cannot simply be relabelled Hz.

High frequency means fast variation, not poor quality. Hair, letter strokes and noise can all contain high frequencies. A frequency response describes the system; a spectrum describes the input’s components.`,
      check:
        "Can smoothing reduce the contrast of clean fine stripes, even if there is no noise?",
      answer:
        "Yes. Whenever the gain at their frequency is below 1, their amplitude decreases. A filter does not automatically recognise and preserve useful detail.",
    },
    {
      id: "recovery",
      title: "Why is sharpening not the same as recovery?",
      relation: "Optional extension · Information and invertibility",
      reason:
        "Distinguish a clearer-looking result from recovery of lost information.",
      body: raw`One sharpening method is $s=z+\alpha(z-b)$, where $z$ is the current input, $b$ is a smoothed version of it, and $\alpha\ge0$. It boosts a high-frequency residual, possibly amplifying noise or causing overshoot. Display clipping can further change results. It does not secretly use the original sharp image.

Consider even-length periodic sequences $x_1[n]=c$ and $x_2[n]=c+a(-1)^n$. With $c=0.5,\ a=0.2$, both have valid brightness values. The three-point filter has zero gain at $f=0.5$, so both different inputs become the constant $c$.

The same output cannot uniquely identify which original was supplied. This is lost distinguishing information, not insufficient arithmetic precision. Extra prior knowledge might suggest a guess, but cannot guarantee that guess is correct.`,
      check:
        "If all filtered values are 0.5, can a sharpening program prove from that output alone that the original contained alternating stripes?",
      answer:
        "No. Both a constant input and alternating stripes can produce that output. Without extra information, the input is not uniquely determined; boosting contrast is not proof of recovery.",
    },
  ],
};
export const imageLearningContent = { "zh-CN": zh, en };
