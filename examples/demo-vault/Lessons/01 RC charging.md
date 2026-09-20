---
type: lesson
course: rc-demo
status: reviewed-example
source_ids: [S01, S02]
---
# RC 充电：为什么电压不会瞬间到位

[[Start|课程入口]] · [[Practice/Review|练习路线]]

把电源接到电阻和电容上，电容两端的电压会立刻等于电源电压吗？这一讲要让你能解释“为什么需要时间”，从电路关系推导电压变化，并判断换电阻、换初始电压后该怎样计算。

来源：[[Sources/Original/01 Lecture#Circuit and assumptions|S01 电路与假设]]、[[Sources/Original/01 Lecture#Governing equation|控制方程]]、[[Sources/Original/01 Lecture#Solution and time constant|解与时间常数]]。下文的解释、展开推导和示范为本示例编写。

## 1 电容电压变化需要电流

电容会储存电荷。在这里，电容量 $C$ 是常数，电荷与电压的关系是 $q=Cv_C$。电流表示单位时间内流入多少电荷，所以

$$i=\frac{dq}{dt}=C\frac{dv_C}{dt}.$$

$v_C$ 是电容上端相对于接地端的电压，单位 V；$i$ 是流入上端的电流，单位 A；$C$ 的单位是 F。这采用 **passive sign convention（被动符号约定）**：电流进入所定义电压的正端。

这条关系可以直接读成：“电压变化得越快，需要的电流越大。”本例中串联电阻限制了电流，因此电容电压随时间逐渐改变。不要把“电容电压通常连续”扩展成无条件结论：理想冲激电流需要另外讨论，本讲不包含它。

我们的模型是理想电源经电阻 $R$ 接到输出节点，电容从该节点接地；电源负端也接地。对 $t\geq0$，电源保持 $V_s$ 不变。假设 $R,C>0$ 且不随时间变，忽略漏电、寄生参数和输出负载。最初 $v_C(0)=0$。

## 2 从电路写出方程

沿回路看，电源电压等于电阻和电容上的电压之和。用欧姆定律 $v_R=Ri$，得到

$$V_s=Ri+v_C=RC\frac{dv_C}{dt}+v_C.$$

把它改写为

$$\frac{dv_C}{dt}=\frac{V_s-v_C}{RC}.$$

右边告诉我们变化快慢来自哪里：当电容电压还低时，它与电源的差距大，变化较快；越来越接近电源时，差距变小，增长也变慢。因此它不是沿直线充电。

**先停一下：**当 $v_C=V_s$ 时，这个方程给出的变化率是多少？如果 $v_C$ 已经高于 $V_s$，变化率又是什么符号？这两个判断会帮你检查后面的公式。

## 3 推导电压随时间的变化

先定义差距 $u(t)=V_s-v_C(t)$。因为电源保持常数，$du/dt=-dv_C/dt$，于是

$$\frac{du}{dt}=-\frac{u}{RC}.$$

本例 $V_s>0$、初始电压为零，因此 $u(0)=V_s>0$。在差距仍为正的区间，把变量分开并做定积分：

$$\int_{V_s}^{u(t)}\frac{1}{u}\,du=-\int_0^t\frac{1}{RC}\,dt.$$

如果积分规则有点生疏，可以先反过来核对：$\ln u$ 的导数是 $1/u$（这里 $u>0$），而常数的定积分等于常数乘区间长度。所以

$$\ln\frac{u(t)}{V_s}=-\frac{t}{RC},\qquad
u(t)=V_se^{-t/(RC)}.$$

对数里使用无量纲的比值。这个解对所有有限 $t\geq0$ 都保持正值，与分离变量时的条件一致。把 $u=V_s-v_C$ 换回来：

$$\boxed{v_C(t)=V_s\left(1-e^{-t/(RC)}\right).}$$

这个公式的初始条件是零电压。遇到非零初始电压时，不要直接套用；到 [[Topics/Choosing the model#非零初始电压|非零初始电压]] 看它如何推广。

## 4 时间常数与完整示范

定义 **time constant（时间常数）** $\tau=RC$。因为 $\Omega\cdot\mathrm F=\mathrm s$，指数 $t/\tau$ 无量纲。时间常数决定变化有多快，不等于“充满所需时间”。

示范：$R=1\,\mathrm{k\Omega}$，$C=100\,\mu\mathrm F$，$V_s=5\,\mathrm V$，初始未充电。先统一单位：

$$\tau=(1000)(100\times10^{-6})=0.1\,\mathrm s.$$

经过 $0.1\,\mathrm s$，也就是一个时间常数：

$$v_C(0.1)=5(1-e^{-1})\approx3.161\,\mathrm V.$$

这约为最终电压的 $63.2\%$。如果忘记把微法换成法，就会得到完全错误的时间尺度。

可以用三个角度检查：代入 $t=0$ 得零，符合初始条件；$t\to\infty$ 时指数趋近零，电压趋近 $5\,\mathrm V$；对解求导得到 $dv_C/dt=(V_s/RC)e^{-t/(RC)}$，代回原方程，左边恰好是 $V_s$。这些检查比“结果看起来合理”更能发现错误。

## 5 独立练习 P1

目的：改变参数后，独立选择模型、换算单位，再解释参数的作用。来源：S02 P1(a–c)，原创示例题；题目与示范参数不同。

**Question.** A series RC circuit has $R=2\,\mathrm{k\Omega}$ and $C=50\,\mu\mathrm F$. A $12\,\mathrm V$ step is applied at $t=0$; the capacitor starts uncharged. (a) Find the time constant. (b) Find the capacitor voltage at $t=0.1\,\mathrm s$. (c) Explain what doubling $R$ does to the final voltage and the time taken to reach a fixed fraction of it.

^q-s02-p1

先合上示范完成这三问，再打开提示或解答。

> [!hint]- 提示
> 先算 $RC$，再比较题目给定时间与它的关系。第(c)问分别观察公式中的最终值和时间尺度；不要把两者混成一个“充电速度”。

> [!success]- 分步解答与检查
> (a) $\tau=2000\times50\times10^{-6}=0.1\,\mathrm s$。
>
> (b) 初始电压为零，使用刚推导的模型：$v_C(0.1)=12(1-e^{-1})\approx7.585\,\mathrm V$。一个时间常数后仍小于最终电压，且占最终值约 $63.2\%$。
>
> (c) 电阻加倍使 $\tau$ 加倍，最终值仍为 $12\,\mathrm V$。若目标比例为 $0<\alpha<1$，从 $\alpha=1-e^{-t/\tau}$ 解得 $t=-\tau\ln(1-\alpha)$，所以到达同一比例的时间也加倍。
>
> 最终结果与原创 S02 答案一致；上述展开过程是为学习编写的。这个结论依赖理想模型和未充电初始条件，不能忽略负载等实际变化后照搬。

## 6 怎样知道自己可以继续

闭卷解释三个问题：为什么充电越来越慢？$RC$ 为什么是时间？哪一个初始条件允许使用本讲的公式？然后到 [[Practice/Review#P2 到达指定比例|P2]] 反过来求所需时间。

如果只记住公式却说不清 $V_s-v_C$ 的含义，先回到第2节。是否掌握要结合自己的尝试判断；本页的完成状态只表示示例内容已编写和检查。
