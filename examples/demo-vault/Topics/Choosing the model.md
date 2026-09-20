# 如何选择 RC 模型

[[Start|课程入口]] · [[Lessons/01 RC charging|首次学习]]

来源：[[Sources/Original/01 Lecture#General initial condition|S01 非零初始条件]]。以下推导、模型选择解释为示例编写。

## 非零初始电压

电容原先已有电压 $V_0$ 时，我们仍然从 $RC\,dv_C/dt+v_C=V_s$ 出发。先试一个保持不变的特解 $v_C=V_s$；剩余差值满足指数衰减，所以写成 $v_C=V_s+Ae^{-t/(RC)}$。代入初始条件 $v_C(0)=V_0$，可得 $A=V_0-V_s$：

$$v_C(t)=V_s+(V_0-V_s)e^{-t/\tau},\qquad \tau=RC.$$

你也可以直接对这个式子求导并代回方程，验证“剩余差值按指数衰减”并非猜测。$V_0=V_s$ 时，指数项系数为零，电压保持不变；$V_0>V_s$ 时，电压从上方下降接近最终值。

选择模型时先问：电源在这段时间里是否保持常数？只有一个独立储能状态吗？初始电压是什么？如果开关改变了电路，就需要在新的时间段重新写方程，不能只替换一个数字。

## P3 初始条件迁移

来源：S02 P3(a–c)，原创示例题。

An ideal series RC circuit has a constant $5\,\mathrm V$ source for $t\geq0$, time constant $0.1\,\mathrm s$, and initial capacitor voltage $2\,\mathrm V$. (a) Find $v_C(t)$. (b) Find $v_C(0.1\,\mathrm s)$. (c) If the initial voltage were $7\,\mathrm V$ instead, would the voltage initially rise or fall? Explain using the governing equation.

^q-s02-p3

> [!hint]- 提示
> 分别代入初始值和最终值。第(c)问可以先用导数的符号判断，无需计算整条曲线。

> [!success]- 分步解答与检查
> (a) $v_C(t)=5+(2-5)e^{-t/0.1}=5-3e^{-t/0.1}\,\mathrm V$，其中 $t$ 以秒计。代入 $t=0$ 得 $2\,\mathrm V$，符合初始条件。
>
> (b) $v_C(0.1)=5-3e^{-1}\approx3.896\,\mathrm V$，位于初始值与最终值之间。
>
> (c) 初始导数为 $(5-7)/0.1=-20\,\mathrm{V/s}$，所以电压下降。这里是电容向电路释放部分能量，不应强套“电压一定上升”的直觉。
>
> 最终结果与原创 S02 答案一致；推导与检查为本知识库展开。
