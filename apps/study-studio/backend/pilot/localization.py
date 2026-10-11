"""Authored presentation only. Task identity, answer keys and recorded evidence never depend on locale."""
import copy
from . import teaching, computing

VERSION = 'pilot-en-2026-10-11'
TOPICS_EN = {
 'ramps': {'title':'Basic signals and ramp construction','objective':'Distinguish height from slope and construct signals using shifted ramps and steps.',
 'routes': {
 'bridge':r'Evaluate the input first, then use $r(s)=\max(s,0)$. For example, $r(2-5)=r(-3)=0$. Negative input does not produce negative ramp height.',
 'visual':r'Imagine two lines of equal slope. The one starting later stays lower. Subtracting their slopes makes their height difference constant, not zero. Mark the breakpoints, then record the slope and initial height of each segment.',
 'algebra':r'Expand each interval. For $t\ge b>a$, $r(t-a)-r(t-b)=(t-a)-(t-b)=b-a$. To return to zero, subtract that height with a step. This task uses $u(0)=1$.'},
 'example':r'Example with different parameters: rise from $t=0$ at slope 1, stop rising at 2 and reset at 4. Then $y(t)=r(t)-r(t-2)-2u(t-4)$. The plateau height is 2; at 4 the last term immediately removes it.'},
 'convolution': {'title':'Convolution and overlapping intervals','objective':'Find integration limits from signal supports; distinguish overlap length from weighted area.',
 'routes': {
 'bridge':r'An intersection satisfies both sets of inequalities. The intersection of $0\le\tau\le2$ and $1\le\tau\le4$ is $[1,2]$. Take the larger lower limit and smaller upper limit. If the upper limit is no greater than the lower, the ordinary-function integral contributes zero area.',
 'visual':r'View $h(t-\tau)$ as a window sliding along the $\tau$ axis: reflect, then shift. Only the region where both signals are nonzero contributes. Find the overlap, then multiply its length by both rectangle heights.',
 'algebra':r'If $x(\tau)$ is supported on $[0,a]$, then $0\le t-\tau\le b$ gives $\tau\in[t-b,t]$. The limits are $L=\max(0,t-b)$ and $U=\min(a,t)$. For ordinary rectangles, convolution is the product of their heights times $\max(0,U-L)$.'},
 'example':r'Example: $x$ has height 1 on $[0,2]$ and $h$ has height 3 on $[0,1]$. At $t=1.5$, the overlap is $[0.5,1.5]$, of length 1, giving convolution 3. Values at isolated rectangle endpoints do not affect an ordinary continuous-time integral.'},
 'fourier': {'title':'Continuous-time Fourier series','objective':'Connect period to angular frequency and check real Fourier coefficient normalisation.',
 'routes': {
 'bridge':r'One cycle spans $2\pi$ radians, so $\omega_0T=2\pi$. Identify whether a given value is a period, a frequency or an angular frequency to avoid losing the factor $2\pi$.',
 'visual':r'For a periodic rectangle, the mean is its area per period divided by the period. A signal even about the chosen origin has no sine component. Check the origin before applying this symmetry argument.',
 'algebra':r'This unit uses $x(t)=a_0+\sum_{n\ge1}[a_n\cos(n\omega_0t)+b_n\sin(n\omega_0t)]$. Therefore $a_0=\frac1T\int_T x(t)dt$ and $a_n=\frac2T\int_T x(t)\cos(n\omega_0t)dt$. A convention with $a_0/2$ requires a corresponding change to the constant coefficient.'},
 'example':r'Example: an even rectangle of period 4 and height 2 on $[-0.5,0.5]$ in each period, zero elsewhere, has mean $a_0=2\times1/4=1/2$ and all $b_n=0$. Check the limits and normalisation separately.'}
}

def topic(key, language):
    if key in computing.PACKS: return computing.topics(language=language)[key]
    return {**teaching.TOPICS[key], **(TOPICS_EN[key] if language=='en' else {})}


def task(t, language):
    out=copy.deepcopy(t)
    if t['topic'] in computing.PACKS:
        translated=computing.task(t['topic'],t['phase'],t['number'],language)
        for key in ('title','objective','source_note','prompt','fields','hint','solution'): out[key]=translated[key]
        return out
    if language!='en': return out
    key=t['topic']; phase=t['phase']; k=t['number']+1+(24 if phase=='review' else 0); d=phase=='diagnosis'
    out.update(language='en',translation_version=VERSION,title={'diagnosis':'Diagnostic check','practice':'Fresh independent practice','review':'Review check'}[phase]+' · '+TOPICS_EN[key]['title'],objective=TOPICS_EN[key]['objective'],source_note='Authored pilot problem based on course definitions; not an official exam question.')
    if key=='ramps':
        a,b,c,m=(k,k+3,k+6,2) if d else (k+2,k+6,k+9,3);h=m*(b-a)
        out.update(prompt=rf'Use $r(t)=\max(t,0)$ and $u(0)=1$. A signal is zero for $t<{a}$, rises from ${a}$ with slope ${m}$, stops rising at ${b}$, and resets immediately to zero at ${c}$. Write it as $x(t)=A r(t-{a})+B r(t-{b})+C u(t-{c})$. Give the key values and explain your construction.',hint='Handle the changes in slope first, then check accumulated height. The step changes height from its starting time.',solution=rf'$A={m}, B={-m}, C={-h}$. Plateau height is ${m}({b}-{a})={h}$. With $u(0)=1$, $x({c})=0$. A ramp with negative input is zero.')
        labels={'height':'Plateau height'}
    elif key=='convolution':
        a=k+2;b=2 if d else 3;t0=a+0.5;p=1 if d else 2;q=3;lo=max(0,t0-b);hi=min(a,t0)
        out.update(prompt=rf'$x(\tau)$ has height ${p}$ on $[0,{a}]$ and is zero elsewhere. $h(s)$ has height ${q}$ on $[0,{b}]$ and is zero elsewhere. Find $y(t)=\int x(\tau)h(t-\tau)d\tau$ at $t={t0}$. First identify the support of $h(t-\tau)$ and the overlap.',hint='Solve 0 ≤ t−τ ≤ b for τ. Only the shared nonzero interval contributes. Remember to multiply both heights.',solution=rf'The support of $h(t-\tau)$ is $[{t0-b},{t0}]$. Its intersection with $[0,{a}]$ is $[{lo},{hi}]$. Thus $y({t0})={p}\times{q}\times({hi}-{lo})={p*q*(hi-lo)}$.')
        labels={'left':'Lower limit of h(t−τ)','right':'Upper limit of h(t−τ)','L':'Overlap lower limit L','U':'Overlap upper limit U'}
    else:
        T=4+2*k;H=k+1 if d else k+3;w=T/4
        out.update(prompt=rf'A real periodic signal of period $T={T}$ has height ${H}$ on $[-{w/2},{w/2}]$ in each central period and is zero elsewhere. Use $x(t)=a_0+\sum_{{n\ge1}}[a_n\cos(n\omega_0t)+b_n\sin(n\omega_0t)]$. Give the values below and explain the normalisation and symmetry.',hint='Check whether the constant term is a₀ or a₀/2. Use area per period for the mean and symmetry about the origin for the sine terms.',solution=rf'$\omega_0/\pi=2/{T}$, area is ${H*w}$, and $a_0={H*w}/{T}={H/4}$. An even signal times an odd sine integrates to zero over a period, so $b_1=0$. The nonzero cosine coefficients use $2/{T}$.')
        labels={'omega':'ω₀ / π (enter a number)','area':'Area in one period','factor':'Factor 2/T before the aₙ integral'}
    for f in out['fields']: f['label']=labels.get(f['id'],f['label'])
    return out


def public_task(t, language):
    return teaching.public_task(task(t, language))


def attempt(a, t, language):
    """Translate deterministic explanation; keep student prose and original evidence intact."""
    if language!='en': return a
    out=copy.deepcopy(a);r=out['result'];display=task(t,language)
    bad=next((f for f in display['fields'] if not r['checks'][f['id']]),None)
    r.update(focus=bad['label'] if bad else None,
        feedback=f'First check “{bad["label"]}”. This could involve arithmetic, reading or the concept; one response does not define a permanent learner type.' if bad else 'All checked answers meet the criteria. Try a fresh problem to check transfer; this does not establish mastery of the whole topic.',
        teaching=topic(t['topic'],language)['routes'][r['route']],scope='Bounded answer criteria checked. Free-form reasoning needs separate review; AI provides suggestions only.')
    return out

ERRORS_EN = {
 '记录不存在或你没有访问权限。':'This record does not exist or is not accessible to your account.',
 '课程尚未导入，请运行 ELEC270 导入命令。':'The course owner needs to import ELEC270 before you can start.',
 '请先登录。':'Please sign in first.',
 '请输入用户名。':'Enter a username.',
 '这个用户名已存在。':'This username is already in use.',
 '需要有效的一次性邀请码。':'A valid single-use invitation is required.',
 '尝试次数过多，请十五分钟后再试。':'Too many sign-in attempts. Try again in fifteen minutes.',
 '用户名或密码不正确。':'Incorrect username or password.',
 '仅本机课程所有者可创建邀请。':'Only the local course owner can create invitations.',
 '仅所有者可以读取本机旧原型记录。':'Only the owner can access the legacy records on this computer.',
 '未找到这个学习单元。':'This learning unit was not found.',
 '附件不存在。':'Attachment not found.',
 '这个请求编号已用于其他操作。':'This request identifier has already been used for another operation.',
 '未知教学路径。':'Unknown teaching route.',
 '照片超过 10 MB，请压缩后重试。':'The photo exceeds 10 MB. Reduce its size and try again.',
 '照片像素过大，请裁切到解题区域。':'The image has too many pixels. Crop it to your answer.',
 '请使用 JPEG、PNG 或 WebP 照片。':'Use a JPEG, PNG or WebP photo.',
 '这张照片无法读取，请重新拍照或输入文字。':'This image cannot be read. Take another photo or enter text.',
 '尚未配置模型。照片已保存；可手动录入并确认解题过程，或先配置本机模型密钥。':'AI is not configured. Your photo is saved; enter and confirm your working manually or ask the owner to configure the model.',
 '已达到今天的模型调用上限。已有课程和离线检查仍可使用。':'Today’s model call limit has been reached. Course reading and offline checks remain available.',
 '已有模型任务正在运行，请稍后再试。':'A model operation is already running. Please try again later.',
 '请核对解题过程与关键公式，然后确认提交。':'Check your working and key formulas, then confirm submission.',
 '同一提交编号的内容不同，请刷新后重试。':'This submission identifier contains different content. Reload before submitting again.',
 '照片属于另一道题。':'The photo belongs to a different problem.',
 '这条作答已撤回。':'This attempt has been withdrawn.',
 '请写明更正原因。':'Enter a reason for the correction.',
 '请补全每个关键数值；可在确认照片时修改。':'Complete every numerical field. You can correct values when confirming the photo.',
 '这组已核查参数已用完，请复习记录或选择其他主题。':'All checked variants in this set have been used. Review your records or choose another topic.',
}

def error_message(message, status, language):
    if language!='en': return message
    if message in ERRORS_EN: return ERRORS_EN[message]
    if ' / ' in message: return message.split(' / ',1)[1]
    if not any('\u3400'<=c<='\u9fff' for c in message): return message
    return {401:'Please sign in again.',403:'This action is not allowed for your account.',404:'The requested record was not found.',409:'The operation could not continue. Reload your saved progress and check the current operation status before retrying.',422:'Check your input: use numbers or simple arithmetic in numerical fields and complete the required values.',429:'The usage limit has been reached. Try again later.',502:'The model did not return a valid result. No automatic retry was made.'}.get(status,'The request could not be completed. Your saved work is retained.')
