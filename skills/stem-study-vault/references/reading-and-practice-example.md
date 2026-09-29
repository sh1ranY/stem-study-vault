# Reading continuity and progressive practice

Read this when designing a new practice sequence or repairing a difficulty jump. This original miniature example demonstrates local inputs, intermediate states and increasing independence. It is not a source lecture, an official problem, a measured learning result or a required five-stage template. For source-image placement and interpretation, follow [teaching.md](teaching.md#use-source-screenshots-where-they-help-explain); the illustrated [teaching standard](teaching-standard.md) provides a separate worked visual example.

## What the design changes

A weak sequence might give the formula, solve one substitution, then ask for an arbitrary-length closed form without teaching how to derive it. Labeling those questions “easy / medium / hard” does not connect them. This sequence instead keeps one capability in view: **track a state correctly, then use the same relation to choose an input and interpret a changed model**.

The learner knows substitution and simple linear equations. General recurrence solutions and calculus are not prerequisites. The Chinese teaching below can be adapted to another language; its numbers and problem count are illustrative.

---

## 每一步到底用哪个状态？

设一个离散过程在第 $n$ 步开始时的状态为 $s_n$，这一轮施加的输入为 $u_n$，状态更新规则为

$$s_{n+1}=a s_n+u_n.$$

这里的 $a$ 是保留比例，本例先取 $a=1/2$。它表示每轮先保留当前状态的一半，再加上这一轮的输入。$s_n$、$u_n$ 使用相同的量纲，$a$ 无量纲；这个简化模型不额外假定具体的物理装置。下标 $n$ 表示轮次，不是指数。

关键是：算 $s_1$ 用 $s_0,u_0$，算 $s_2$ 用刚得到的 $s_1,u_1$。不能每轮都重新拿 $s_0$ 代入，也不能把尚未施加的 $u_1$ 提前加到第一轮。

例如给定 $s_0=4$，输入依次为 $u_0=2,u_1=0$。第一轮先把 $4$ 保留一半，再加 $2$，所以 $s_1=4$。第二轮从这个新状态开始，保留一半且没有新输入，得到 $s_2=2$。

| 轮次 $n$ | 本轮开始 $s_n$ | 本轮输入 $u_n$ | 本轮计算 | 下一状态 $s_{n+1}$ |
| --- | ---: | ---: | --- | ---: |
| 0 | 4 | 2 | $4/2+2$ | 4 |
| 1 | 4 | 0 | $4/2+0$ | 2 |

按列读，这张表区分了状态和输入；按行读，它显示前一行的“下一状态”怎样成为后一行的“本轮开始”。可以用第二轮反查：没有新输入时，状态应减半，$4\to2$ 与规则相符。

### A｜先把状态传递接起来

这是原创练习。重新开始：$a=1/2,s_0=8$，输入为 $u_0=0,u_1=3$。求 $s_1,s_2$。请写出两行“本轮开始 → 保留部分 → 加入输入 → 下一状态”，并说明第二行从哪个数开始。

> [!hint]- 提示
> 完成第一行后，把它的输出作为第二行的起点；不要继续使用初始状态。

> [!success]- 解答与检查
> 第一轮 $s_1=8/2+0=4$；第二轮 $s_2=4/2+3=5$。第二轮从 $4$ 开始。反查第二轮，$s_2-u_1=5-3=2=s_1/2$。
>
> 若得到 $s_2=7$，检查是否误把第二轮起点又写成了 $s_0=8$。回到正文表格，追踪前后两行连接的位置。

### B｜独立重建同一种过程

这是原创练习，与 A 独立。给定 $a=1/2,s_0=0$，输入依次为 $2,0,2$，求 $s_1,s_2,s_3$，并解释为什么第二轮状态下降、第三轮又上升。自行选择合适的记录方式。

> [!hint]- 提示
> 将每一轮的输入与开始状态对应。解释升降时，把保留下来的部分和新加入的部分分开看。

> [!success]- 解答与检查
> $s_1=0/2+2=2$，$s_2=2/2+0=1$，$s_3=1/2+2=2.5$。第二轮没有输入，状态减半；第三轮虽然只保留原状态的一半，但输入 $2$ 大于这一轮失去的 $0.5$，所以状态增加。
>
> 一般地，$s_{n+1}-s_n=u_n-s_n/2$。这直接来自把更新式两边减去 $s_n$；它解释升降的条件，不表示任何正输入都必然使状态增加。

## 从“给输入算状态”到“为了目标选输入”

刚才输入已知，现在把同一关系反过来使用。若已知当前状态和希望达到的下一状态，移项得到

$$u_n=s_{n+1}-a s_n.$$

含义是：目标状态减去已经能保留的部分，才是这一轮需要补入的量。移项并没有创造一条新模型，求出的输入仍需代回原更新式检查。如果实际问题要求输入非负，算出负数意味着这个目标无法仅靠允许的非负输入在该轮实现；不能把负号擅自删掉。

### C｜增加一个设计决定

这是原创练习，与前题独立。取 $a=1/2,s_0=0$。要求连续两轮使用相同的非负输入 $u_0=u_1=c$，使 $s_2=6$。求 $c$，并用前向计算检查。

> [!hint]- 提示
> 先用 $c$ 表示第一轮状态，再把它代入第二轮。相同输入不表示两轮状态相同。

> [!success]- 解答与检查
> 第一轮 $s_1=c$，第二轮 $s_2=c/2+c=3c/2$。令 $3c/2=6$，得 $c=4$，满足非负限制。前向检查为 $0\to4\to6$。
>
> 若算出 $c=3$，可能把两轮输入直接相加，忘了第一轮形成的状态在下一轮只保留一半。回到更新规则，而不要把这题当成单纯的平均分配。

## 换了系数，怎样判断升降

要比较下一状态与当前状态，可以从原更新式两边减去 $s_n$：

$$s_{n+1}-s_n=(a-1)s_n+u_n.$$

左边为正表示上升，为零表示不变，为负表示下降。当 $0\leq a<1$ 且状态非负时，$(1-a)s_n$ 就是这一轮没有保留下来的部分；输入要超过这部分，状态才会上升。这给出判断方法，而不必把每个新系数都当作一种全新题型。

### D｜改变条件并检验解释

这是原创练习，与前题独立。现在 $a=4/5,s_0=10$，连续两轮输入均为 $1$。求两个新状态，判断“只要每轮输入为正，状态就一定上升”是否正确，并给出从任一状态 $s_n$ 开始、下一轮上升所需的输入条件。

> [!hint]- 提示
> 先代入新的 $a$，再比较 $s_{n+1}$ 与 $s_n$。可以像 B 的解释一样，从更新式两边减去当前状态。

> [!success]- 解答与检查
> $s_1=(4/5)10+1=9$，$s_2=(4/5)9+1=8.2$。输入为正仍可能下降，因为输入小于本轮失去的状态部分。
>
> $s_{n+1}-s_n=u_n-s_n/5$，所以下一轮上升当且仅当 $u_n>s_n/5$；相等时状态保持不变，小于时下降。初始状态 $10$ 需要输入大于 $2$ 才会上升，而题中只有 $1$。这既核对了数值，也说明不能继续套用旧系数的一半规则。

---

## Why these steps form a progression

| Step | Capability already taught | Added demand | Support or recovery |
| --- | --- | --- | --- |
| Worked example → A | Forward update and state/input distinction | Perform the same reasoning rather than read it | Explicit trace format; hint points to the state handoff |
| A → B | Repeated state update | Organize the trace independently and explain the direction | No prefilled trace; complete new inputs; return to the worked state table |
| B → C | Forward substitution, plus the intervening reverse-input explanation | Choose one unknown shared input under a target constraint | A symbolic first step in the hint; verify by forward execution |
| C → D | State changes and the original general coefficient | Recognize a changed coefficient and reject an overgeneralized claim | All new inputs stated; sign argument uses algebra already shown |

D could be scheduled as a later mixed revisit, or used immediately when suitable. An actual learner struggling at A needs a focused state-handoff explanation, not an automatic jump to D. A learner who can already reconstruct and explain the process may not need every drill. No mastery status can be assigned from this designed sequence alone.

The problems share a concept without sharing an unprovided numerical answer: each resets its initial conditions. Hints and answers are separate, while inputs remain available before either is opened. New reasoning needed for C is taught before C. Difficulty increases through independence, reverse reasoning and a changed assumption, rather than just bigger numbers. In a real course, preserve all supplied question identities and cases; this authored example does not authorize replacing them with these exercises.
