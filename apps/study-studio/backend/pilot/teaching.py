"""Bounded, authored ELEC270 task families. Model prose never changes numeric verdicts."""
import copy
import math
from . import store, computing
from ..assessment import numeric

TOPICS = {
 'ramps': {'title':'基本信号与斜坡构造','week':1,'focus':'单元7','objective':'区分高度与斜率，并用平移斜坡和阶跃构造信号。',
  'routes':{
   'bridge':r'先计算括号内的输入，再用 $r(s)=\max(s,0)$。例如 $r(2-5)=r(-3)=0$。负输入不会产生负的斜坡高度。',
   'visual':r'想象两条等斜率的直线：后开始的那条始终落后。斜率相减为零，表示高度差不再增长，并不表示高度差为零。先在图上标出各断点，再记录每段的斜率和开始高度。',
   'algebra':r'在每个断点分段展开。$r(t-a)-r(t-b)$ 在 $t\ge b>a$ 时等于 $(t-a)-(t-b)=b-a$。需要回到零时，再减去对应高度的阶跃；本题约定 $u(0)=1$。'},
  'example':r'示范（与检查题参数不同）：从 $t=0$ 以斜率1上升，到2停止增长，到4归零：$y(t)=r(t)-r(t-2)-2u(t-4)$。平台高度为2；在4处，最后一项立即扣除高度2。'},
 'convolution': {'title':'卷积与交叠区间','week':2,'focus':'单元5','objective':'从两段支撑区间得到卷积积分限，并区分交叠长度与面积。',
  'routes':{
   'bridge':r'区间交集同时满足两组不等式。例如 $0\le\tau\le2$ 和 $1\le\tau\le4$ 的交集是 $[1,2]$。下限取较大值，上限取较小值；上限不大于下限时，普通函数的积分面积为零。',
   'visual':r'把 $h(t-\tau)$ 看成沿 $\tau$ 轴平移的窗口。先翻转，再平移。只有它与 $x(\tau)$ 同时非零的部分贡献面积：先找交叠区间，再乘两矩形的高度。',
   'algebra':r'若 $x(\tau)$ 支撑为 $[0,a]$，$h(t-\tau)$ 的条件为 $0\le t-\tau\le b$，则 $\tau\in[t-b,t]$。积分下限 $L=\max(0,t-b)$，上限 $U=\min(a,t)$。普通矩形卷积为高度乘积乘以 $\max(0,U-L)$。'},
  'example':r'示范：$x$ 在 $[0,2]$ 高度为1，$h$ 在 $[0,1]$ 高度为3。取 $t=1.5$，交叠区间为 $[0.5,1.5]$，长度1，故卷积值为3。矩形边界单点不影响普通CT积分。'},
 'fourier': {'title':'连续时间 Fourier Series','week':3,'focus':'单元','objective':'理解周期、角频率以及实三角级数系数的归一化。',
  'routes':{
   'bridge':r'一个周期的角度是 $2\pi$ 弧度，所以 $\omega_0T=2\pi$。先确认题给的是周期、频率还是角频率，避免遗漏 $2\pi$。',
   'visual':r'把周期矩形看成每周期重复的面积。平均值是面积除以周期。关于原点对称的偶函数没有正弦分量；这是对称性的结论，需要先看所选原点。',
   'algebra':r'本单元使用 $x(t)=a_0+\sum_{n\ge1}[a_n\cos(n\omega_0t)+b_n\sin(n\omega_0t)]$，所以 $a_0=\frac1T\int_T x(t)dt$，$a_n=\frac2T\int_T x(t)\cos(n\omega_0t)dt$。使用 $a_0/2$ 的另一约定时，常数系数也必须换算。'},
  'example':r'示范：周期4、在每周期 $[-0.5,0.5]$ 高度为2，其余为0的偶矩形，平均值 $a_0=2\times1/4=1/2$，所有 $b_n=0$。对积分上下限和归一化分别核查。'}
}


def topics(code='ELEC270'):
    return TOPICS if code == 'ELEC270' else computing.topics(code)


def all_topics():
    return {**TOPICS, **computing.topics()}


def field(id, label, answer, route): return {'id':id,'label':label,'answer':answer,'route':route}

def task(topic, phase, number=0):
    """Different integer parameters across repeats; identity stable across sessions/imports."""
    if topic in computing.PACKS: return computing.task(topic, phase, number)
    if topic not in TOPICS or phase not in ('diagnosis','practice','review'): raise ValueError('未知题目类型。')
    if not 0 <= number < 24: raise ValueError('这组已核查参数已用完，请复习记录或选择其他主题。')
    d = phase=='diagnosis'; k=number+1+(24 if phase=='review' else 0); key=f'elec270:{topic}:v1:{phase}:{number}'
    base={'id':key,'topic':topic,'phase':phase,'number':number,'family':topic+'-v1','version':'1','title':('前置诊断' if d else '延迟复查' if phase=='review' else '新的独立练习')+' · '+TOPICS[topic]['title'],'objective':TOPICS[topic]['objective'],'origin':'authored-pilot','source_note':'基于课程定义编写的试点题；不是官方原题。','fields':[],'created_at':store.now()}
    if topic=='ramps':
        a,b,c,m=(k, k+3, k+6, 2) if d else (k+2,k+6,k+9,3)
        h=m*(b-a)
        base.update(prompt=rf'约定 $r(t)=\max(t,0)$、$u(0)=1$。信号在 $t<{a}$ 为零，从 ${a}$ 开始以斜率 ${m}$ 上升，到 ${b}$ 停止增长，在 ${c}$ 时立即归零。写为 $x(t)=A r(t-{a})+B r(t-{b})+C u(t-{c})$。请给出关键数值并解释构造过程。',
         fields=[field('shift',f'r({b-1} − {b})',0,'bridge'),field('height','平台高度',h,'visual'),field('A','A',m,'algebra'),field('B','B',-m,'algebra'),field('C','C',-h,'visual'),field('end',f'x({c})',0,'algebra')],
         hint='先处理斜率的变化，再核对已累积的高度。阶跃在指定时刻开始改变高度。',
         solution=rf'$A={m}, B={-m}, C={-h}$。平台高度 ${m}({b}-{a})={h}$；归零点采用 $u(0)=1$，因此 $x({c})=0$。负输入斜坡为0。')
    elif topic=='convolution':
        a=k+2;b=2 if d else 3;t=a+0.5;p=1 if d else 2;q=3;lo=max(0,t-b);hi=min(a,t)
        base.update(prompt=rf'$x(\tau)$ 在 $[0,{a}]$ 上高度为 ${p}$，其余为0；$h(s)$ 在 $[0,{b}]$ 上高度为 ${q}$，其余为0。求 $y(t)=\int x(\tau)h(t-\tau)d\tau$ 在 $t={t}$ 时的值。先写出 $h(t-\tau)$ 的非零区间和交叠区间。',
         fields=[field('left','h(t−τ) 的区间下限',t-b,'bridge'),field('right','h(t−τ) 的区间上限',t,'bridge'),field('L','交叠下限 L',lo,'visual'),field('U','交叠上限 U',hi,'visual'),field('y','y(t)',p*q*(hi-lo),'algebra')],
         hint='把 0 ≤ t−τ ≤ b 解成关于 τ 的不等式。两段都非零的区间才参与积分；别忘记两个高度相乘。',
         solution=rf'$h(t-\tau)$ 的区间为 $[{t-b},{t}]$，与 $[0,{a}]$ 相交得 $[{lo},{hi}]$；$y({t})={p}\times{q}\times({hi}-{lo})={p*q*(hi-lo)}$。')
    else:
        T=4+2*k;H=k+1 if d else k+3;w=T/4
        base.update(prompt=rf'周期为 $T={T}$ 的实信号，在每周期中心 $[-{w/2},{w/2}]$ 高度为 ${H}$，其余为0。采用 $x(t)=a_0+\sum_{{n\ge1}}[a_n\cos(n\omega_0t)+b_n\sin(n\omega_0t)]$。回答以下数值，并解释所用的归一化和对称性。',
         fields=[field('omega','ω₀ / π（填写数值）',2/T,'bridge'),field('area','一周期面积',H*w,'visual'),field('a0','a₀',H/4,'algebra'),field('b1','b₁',0,'visual'),field('factor','aₙ 积分前的系数 2/T',2/T,'algebra')],
         hint='先核对本题常数项是 a₀ 还是 a₀/2。平均值来自每周期面积；正弦项再用关于原点的对称性判断。',
         solution=rf'$\omega_0/\pi=2/{T}$，面积为 ${H*w}$，$a_0={H*w}/{T}={H/4}$。偶函数乘奇正弦的周期积分为零，故 $b_1=0$；非零余弦阶的积分系数为 $2/{T}$。')
    return base


def public_task(t):
    out=copy.deepcopy(t)
    out.pop('solution',None);out.pop('hint',None)
    for f in out['fields']: f.pop('answer',None);f.pop('route',None)
    return out


def evaluate(t, answers, exposure, prior):
    if set(answers) != {f['id'] for f in t['fields']}: raise ValueError('请补全每个关键数值；可在确认照片时修改。')
    checks={f['id']:math.isclose(numeric(answers[f['id']]), f['answer'],rel_tol=1e-7,abs_tol=1e-7) for f in t['fields']}
    bad=next((f for f in t['fields'] if not checks[f['id']]),None)
    route=bad['route'] if bad else 'algebra';passed=all(checks.values())
    status=('diagnostic_match' if t['phase']=='diagnosis' else 'supported' if exposure or prior else 'independent') if passed else 'needs_review'
    return {'checks':checks,'passed':passed,'status':status,'route':route,'focus':bad['label'] if bad else None,
            'feedback':f'先核对「{bad["label"]}」。这可能是计算、读题或概念上的问题；仅凭一次作答不作永久分类。' if bad else '本题关键答案均符合判据。接下来用不同参数检查迁移；这不等于已经掌握整个主题。',
            'teaching':all_topics()[t['topic']]['routes'][route],
            'scope':'指定答案判据已检查；自由解题过程另由 AI 提供建议或保留待核查。','retention':'unassessed'}
