"""Versioned bilingual teaching; concept identities and numerical checks are language-neutral."""
import math
from . import store
from ..assessment import numeric

VERSION = 'ramps-guided-1'
TRANSLATION_VERSION = '2026-10-11'
LANGUAGES = ('zh-CN', 'en')
MODES = ('bridge', 'visual', 'algebra')
CONCEPTS = ('shifted-ramp', 'slope-cancellation', 'height-reset')


def pair(zh, en):
    return {'zh-CN': zh, 'en': en}


CONTENT = [
    {
        'title': pair('先读懂平移斜坡', 'Read a shifted ramp'),
        'goal': pair('先算函数的输入，再应用定义；分清时间 t 与输入 t−a。', 'Evaluate the input before applying the definition; distinguish time t from the input t−a.'),
        'routes': {
            'bridge': pair(
                r'斜坡函数的定义是 $r(s)=\max(s,0)$。这里的 $s$ 是占位符，可以换成任何表达式。先算括号里的数，再比较它和零，保留较大者。' '\n\n' r'例如 $r(t-1)$：在 $t=0$ 时，输入为 $-1$，所以输出为 $0$；在 $t=3$ 时，输入为 $2$，输出才是 $2$。不要把负的输入直接当成输出。',
                r'The ramp is defined by $r(s)=\max(s,0)$. The letter $s$ is a placeholder: it may be replaced by an expression. Evaluate that expression first, then keep the larger of its value and zero.' '\n\n' r'For $r(t-1)$, at $t=0$ the input is $-1$, so the output is $0$. At $t=3$ the input is $2$, so the output is $2$. A negative input is not a negative ramp output.'),
            'visual': pair(
                r'把 $t=1$ 看作斜坡的启动位置。在这之前，曲线贴着横轴；越过它以后，每向右移动一格，高度上升一格。$r(t-1)$ 是把启动位置向右移到 $1$，而不是把整条曲线向下移一格。' '\n\n' '拖动下方的时间滑块，分别停在启动点之前、启动点上、启动点之后。观察输入已经改变时，输出何时才开始增长。',
                r'Think of $t=1$ as the starting position. Before it, the graph stays on the horizontal axis. After it, each step to the right raises the height by one. In $r(t-1)$, the start moves right to $1$; the whole graph does not move down by one.' '\n\n' 'Move the time slider before, onto, and after the start. Notice when the output begins to grow as the input changes.'),
            'algebra': pair(
                r'由定义分两种情况：当 $t-1<0$，输出为零；当 $t-1\ge0$，输出为括号中的值。因此 $r(t-1)=0$（$t<1$），而 $r(t-1)=t-1$（$t\ge1$）。' '\n\n' r'断点来自 $t-1=0$，而不是凭外观猜测。边界 $t=1$ 处两种表达式都给出 $0$。对一般的 $r(t-a)$，用同样方法从 $t-a=0$ 找到断点。',
                r'Split the definition into two cases. If $t-1<0$, the output is zero. If $t-1\ge0$, the output equals the input. Thus $r(t-1)=0$ for $t<1$, and $r(t-1)=t-1$ for $t\ge1$.' '\n\n' r'The breakpoint comes from $t-1=0$. At $t=1$, both expressions give $0$. Apply the same reasoning to $r(t-a)$ by solving $t-a=0$.'),
        },
    },
    {
        'title': pair('消去斜率，保留高度', 'Cancel the slope, keep the height'),
        'goal': pair('说明为什么停止增长以后仍然留下平台。', 'Explain why a plateau remains after growth stops.'),
        'routes': {
            'bridge': pair(
                r'高度表示当前值，斜率表示它增长得有多快。这两个量不同。考虑 $y(t)=2r(t-1)-2r(t-4)$：第一项从 $1$ 开始增长；第二项在 $4$ 才启动，所以它无法抹掉之前已经累积的高度。' '\n\n' r'从 $1$ 到 $4$ 一共增长了 $3$ 个时间单位，每单位增长 $2$，已累积高度 $6$。第二项启动后抵消的是之后的增长速度，留下的高度仍然是 $6$。',
                r'Height is the current value; slope is how quickly it grows. These are different quantities. In $y(t)=2r(t-1)-2r(t-4)$, the first term starts at $1$, but the second starts only at $4$. It cannot erase the height accumulated earlier.' '\n\n' r'Between $1$ and $4$, the signal grows for $3$ time units at a rate of $2$, accumulating a height of $6$. The second term cancels subsequent growth, leaving that height unchanged.'),
            'visual': pair(
                '下图的虚线是第一条斜坡，点线是要减去的第二条斜坡的大小。第二条晚启动，始终比第一条低一段。实线表示两者的差。' '\n\n' r'把滑块拖到 $t>4$：两条斜坡一起增高，它们的竖直间距却固定为 $6$。实线因此是平台。停止增长表示实线变平，不表示它回到了横轴。',
                'The dashed line is the first ramp. The dotted line is the size of the second ramp being subtracted. It starts later and remains lower. The solid line shows their difference.' '\n\n' r'Move the slider to $t>4$: both ramps rise, but their vertical separation stays at $6$. Their difference is a plateau. Stopping growth makes the solid line flat; it does not bring it back to zero.'),
            'algebra': pair(
                r'对 $y(t)=2r(t-1)-2r(t-4)$ 分段展开。$t<1$ 时两项都为零；$1\le t<4$ 时第二项为零，所以 $y(t)=2(t-1)$。' '\n\n' r'当 $t\ge4$，两项都启动：$y(t)=2(t-1)-2(t-4)=2t-2-2t+8=6$。消掉的是含 $t$ 的项，常数项没有消失。一般地，$m r(t-a)-m r(t-b)=m(b-a)$（$t\ge b>a$）。',
                r'Expand $y(t)=2r(t-1)-2r(t-4)$ piece by piece. For $t<1$, both terms vanish. For $1\le t<4$, only the first is active, so $y(t)=2(t-1)$.' '\n\n' r'For $t\ge4$, both are active: $y(t)=2(t-1)-2(t-4)=2t-2-2t+8=6$. The terms containing $t$ cancel; the constants do not. In general, $m r(t-a)-m r(t-b)=m(b-a)$ for $t\ge b>a$.'),
        },
    },
    {
        'title': pair('用阶跃移除平台高度', 'Remove the plateau with a step'),
        'goal': pair('区分改变斜率和改变高度，并检查断点取值。', 'Distinguish a change in slope from a change in height, including the breakpoint value.'),
        'routes': {
            'bridge': pair(
                r'约定 $u(s)=0$（$s<0$），$u(s)=1$（$s\ge0$）。所以 $C u(t-c)$ 在 $c$ 之前不影响信号，从 $c$ 起给信号加上固定的 $C$。它改变的是高度。' '\n\n' r'示范中的平台高度为 $6$。要从 $t=6$ 起归零，需加上 $-6u(t-6)$：之前加零，之后减去 $6$。系数取决于平台高度，不是原先的斜率。',
                r'Use $u(s)=0$ for $s<0$ and $u(s)=1$ for $s\ge0$. Thus $C u(t-c)$ has no effect before $c$, then adds a constant $C$ from $c$ onwards. It changes height.' '\n\n' r'The example has a plateau of height $6$. To reset it at $t=6$, add $-6u(t-6)$: zero is added before that time, and $6$ is subtracted afterwards. The coefficient depends on plateau height, not the earlier slope.'),
            'visual': pair(
                r'看下图在 $t=6$ 的跳变：空心点表示归零前趋近的高度，实心点表示该时刻的实际取值。我们约定 $u(0)=1$，因此归零动作在断点当下已经生效。' '\n\n' '拖动滑块到断点两侧，再准确停在断点上。要把平台移到横轴，竖直变化量必须等于整个平台高度的相反数。图中的竖直虚线只表示跳变，不表示中间各高度都是信号取值。',
                r'Inspect the jump at $t=6$. The open circle marks the height approached from the left; the filled circle marks the actual value at the breakpoint. With $u(0)=1$, the reset has already taken effect at that instant.' '\n\n' 'Move the slider to either side, then exactly onto the breakpoint. Returning the plateau to zero requires a vertical change equal to the negative of its height. The vertical dashed line indicates a jump, not intermediate signal values.'),
            'algebra': pair(
                r'写成 $x(t)=2r(t-1)-2r(t-4)+C u(t-6)$。在 $4\le t<6$，阶跃仍为零，平台高度为 $6$；在 $t\ge6$，阶跃为 $1$，于是 $x(t)=6+C$。' '\n\n' r'要求归零就令 $6+C=0$，得到 $C=-6$。边界处直接代入：$x(6)=2(6-1)-2(6-4)-6=0$。一般的平台高度 $H=m(b-a)$ 需要 $C=-H$，并且必须注明所用的 $u(0)$ 约定。',
                r'Write $x(t)=2r(t-1)-2r(t-4)+C u(t-6)$. For $4\le t<6$, the step is zero and the plateau height is $6$. For $t\ge6$, the step is one, giving $x(t)=6+C$.' '\n\n' r'To reset to zero, impose $6+C=0$, hence $C=-6$. Check the boundary directly: $x(6)=2(6-1)-2(6-4)-6=0$. A plateau of height $H=m(b-a)$ requires $C=-H$; always state the convention for $u(0)$.'),
        },
    },
]

REASONS = {
    'definition': pair('先计算输入，再按 max(输入, 0) 取值。', 'Evaluate the input, then apply max(input, 0).'),
    'identity': pair('斜坡输出始终等于括号内的数。', 'A ramp always returns the number inside its brackets.'),
    'absolute': pair('斜坡把括号内的数变成绝对值。', 'A ramp takes the absolute value of its input.'),
    'gap': pair('两项的斜率抵消，但晚启动留下固定高度差。', 'The slopes cancel, but the delayed start leaves a constant height difference.'),
    'zero': pair('斜率抵消后，信号高度也必定为零。', 'Once the slopes cancel, the signal height must also be zero.'),
    'first': pair('第二条斜坡启动后，可以忽略第一条斜坡。', 'After the second ramp starts, the first ramp can be ignored.'),
    'height': pair('阶跃系数应抵消已累积的平台高度。', 'The step coefficient must cancel the accumulated plateau height.'),
    'slope': pair('阶跃系数应抵消最初的斜率。', 'The step coefficient must cancel the initial slope.'),
    'time': pair('阶跃系数应抵消阶跃启动的时刻。', 'The step coefficient must cancel the step starting time.'),
}

FEEDBACK = {
    'definition': pair('先算括号内的输入，再用斜坡的分段定义。斜坡既不是恒等函数，也不是绝对值函数。建议先补定义，再检查一组新数值。', 'Evaluate the input, then apply the piecewise ramp definition. A ramp is neither the identity nor the absolute-value function. Review the definition, then check fresh values.'),
    'slope-height': pair('需要区分斜率与高度。两项增长速度相同，只能推出差值不再增长，不能推出差值为零。建议观察图中两条线的竖直间距。', 'Distinguish slope from height. Equal growth rates make the difference constant, not necessarily zero. Inspect the vertical gap between the two lines.'),
    'arithmetic': pair('你选择的解释符合这个概念，但数值还需核对。把两个斜坡分别展开，检查符号与减法；换一组参数再试。', 'Your chosen explanation fits the concept, but the number needs checking. Expand both ramps separately and check signs and subtraction, then try fresh parameters.'),
    'step-height': pair('阶跃负责一次高度变化。先求断点之前的平台高度，再考虑应该加上什么才能回到零；不要把斜率或启动时刻当成高度。', 'A step produces a change in height. Find the plateau height just before the breakpoint, then decide what must be added to reach zero. Neither slope nor starting time is a height.'),
    'shift-arithmetic': pair('你选对了定义，但数值不一致。先单独写出 t−a 的值，再决定使用零还是这个输入。', 'You chose the correct definition, but the number does not match. Write down t−a first, then decide whether the output is zero or that input.'),
    'pass': pair('本次小检查的数值和所选解释都符合判据。这是讲解后的检查，接下来仍需通过新题验证独立运用。', 'Both the number and the selected explanation meet this checkpoint’s criteria. This is a guided check; a fresh problem is still needed to test independent use.'),
}


def checkpoint(step, variant):
    if not 0 <= step < 3 or not 0 <= variant < 24:
        raise ValueError('Unsupported checkpoint')
    a=2+variant; b=a+3+variant%2; m=2+variant%3; c=b+2
    if step==0:
        t=a-(1+variant%3) if variant%2==0 else a+2+variant%3
        prompt=pair(rf'约定 $r(s)=\max(s,0)$。在 $t={t}$ 时，$r(t-{a})$ 等于多少？并选择理由。', rf'Let $r(s)=\max(s,0)$. At $t={t}$, what is $r(t-{a})$? Choose the reason as well.')
        label=f'r({t} − {a})';answer=max(t-a,0);choices=['identity','definition','absolute'];correct='definition'
    elif step==1:
        t=b+2
        prompt=pair(rf'对 $y(t)={m}r(t-{a})-{m}r(t-{b})$，求 $y({t})$，并选择理由。', rf'For $y(t)={m}r(t-{a})-{m}r(t-{b})$, find $y({t})$ and choose the reason.')
        label=f'y({t})';answer=m*(b-a);choices=['zero','first','gap'];correct='gap'
    else:
        prompt=pair(rf'$x(t)={m}r(t-{a})-{m}r(t-{b})+C u(t-{c})$。约定 $u(0)=1$。要使信号从 ${c}$ 起归零，$C$ 应是多少？并选择理由。', rf'$x(t)={m}r(t-{a})-{m}r(t-{b})+C u(t-{c})$, with $u(0)=1$. What coefficient $C$ resets the signal to zero from ${c}$ onwards? Choose the reason.')
        label='C';answer=-m*(b-a);choices=['slope','height','time'];correct='height'
    return {'prompt':prompt,'label':label,'answer':answer,'choices':choices,'correct':correct}


def assess(step, variant, number, choice):
    q=checkpoint(step,variant)
    if choice not in q['choices']: raise ValueError('invalid_choice')
    try: value=numeric(number)
    except ValueError: raise ValueError('invalid_number')
    number_ok=math.isclose(value,q['answer'],rel_tol=1e-7,abs_tol=1e-7)
    reason_ok=choice==q['correct'];passed=number_ok and reason_ok
    if passed: code='pass';suggested=None
    elif step==0: code='shift-arithmetic' if reason_ok else 'definition';suggested='bridge'
    elif step==1: code='arithmetic' if reason_ok else 'slope-height';suggested='algebra' if reason_ok else 'visual'
    else: code='arithmetic' if reason_ok else 'step-height';suggested='algebra' if reason_ok else 'visual'
    return {'passed':passed,'number_ok':number_ok,'reason_ok':reason_ok,'feedback_code':code,'suggested_mode':suggested,'evidence':'guided-check','retention':'unassessed'}


def present(session, language):
    """Never publish expected answers or grading keys with an unanswered checkpoint."""
    step=session['step'];complete=step==3
    result=session.get('result')
    body={k:session[k] for k in ('id','step','mode','variant','check_id','course_version','content_version','at')}
    body.update(language=language,translation_version=TRANSLATION_VERSION,complete=complete,
                concepts=[{'id':CONCEPTS[i],'title':c['title'][language]} for i,c in enumerate(CONTENT)],
                result={**result,'feedback':FEEDBACK[result['feedback_code']][language]} if result else None,
                retry_available=session['variant']<23)
    if complete:
        body['review']=[{'title':c['title'][language],'body':c['routes'][session['mode']][language]} for c in CONTENT]
    if not complete:
        c=CONTENT[step];q=checkpoint(step,session['variant'])
        body.update(concept_id=CONCEPTS[step],title=c['title'][language],goal=c['goal'][language],body=c['routes'][session['mode']][language],
                    checkpoint={'prompt':q['prompt'][language],'label':q['label'],'choices':[{'id':k,'text':REASONS[k][language]} for k in q['choices']]})
    return body


def new_session(course_version,mode='visual'):
    return {'id':'ramps','step':0,'mode':mode,'variant':0,'check_id':store.uid(),'result':None,
            'course_version':course_version,'content_version':VERSION,'at':store.now()}
