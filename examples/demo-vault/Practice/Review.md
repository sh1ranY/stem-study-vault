# 练习与复习路线

[[Start|课程入口]]

1. 首次学习后做 [[Lessons/01 RC charging#^q-s02-p1|P1(a–c)：参数与单位]]。
2. 能独立解释 $RC$ 后做下面的 P2。
3. 学会 [[Topics/Choosing the model#非零初始电压|非零初始条件]] 后做 [[Topics/Choosing the model#^q-s02-p3|P3(a–c)：初始条件迁移]]。

## P2 到达指定比例

来源：S02 P2，原创示例题。目的：从“给时间求电压”迁移到“给电压求时间”。

For $R=1\,\mathrm{k\Omega}$, $C=100\,\mu\mathrm F$ and a $5\,\mathrm V$ step with zero initial capacitor voltage, find the first time the output reaches $90\%$ of its final voltage. Does it ever reach exactly $5\,\mathrm V$ at a finite time in this model?

^q-s02-p2

> [!hint]- 提示
> 先把目标写成 $v_C/V_s$ 的比例，整理到指数单独位于一边，再使用自然对数。

> [!success]- 分步解答与检查
> $\tau=0.1\,\mathrm s$。由 $0.9=1-e^{-t/0.1}$，得 $e^{-t/0.1}=0.1$，所以
>
> $$t=-0.1\ln(0.1)\approx0.23026\,\mathrm s.$$
>
> 时间为正，约为 $2.303\tau$；代回公式得到目标比例 $0.9$。由于响应在这里严格上升，这就是首次到达的时刻。
>
> 任何有限时间的指数都大于零，故电压小于 $5\,\mathrm V$；只在 $t\to\infty$ 的极限下趋近它。实际“充满”常指某个允许误差内，需先说明误差标准。
>
> 最终结果与原创 S02 答案一致；解释和检查为本知识库展开。

## 下一次复习

不看公式，先画出你预期的初始值、最终值和变化方向，再尝试一道变式。把真正卡住的一步记到 [[Personal/Learning log]]。这里没有预填任何“已掌握”记录。
