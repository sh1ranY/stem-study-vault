"""Original bilingual image-filtering checks; no model calls or learner-type inference.

Answers and help remain server-side until explicitly checked/revealed. A successful
bounded check is not evidence of complete Fourier mastery or delayed retention.
"""
import math
from . import store
from ..assessment import numeric

UNIT_ID = 'image-filtering'
VERSION = 'image-filtering-1'
TRANSLATION_VERSION = '2026-10-19'
MAX_VARIANTS = 8
KINDS = ('smoothing', 'frequency', 'transfer', 'recovery')
BRIDGES = ('pixels', 'convolution', 'euler', 'frequency', 'recovery')


def pair(zh, en):
    return {'zh-CN': zh, 'en': en}


REASONS = {
    'weighted': pair('把相邻三个像素分别乘以权重再相加；权重和为 1。', 'Multiply the three neighbouring pixels by their weights, then add; the weights sum to 1.'),
    'minimum': pair('平滑总是选择这三个像素中最小的亮度。', 'Smoothing always selects the smallest of the three brightness values.'),
    'unweighted': pair('把三个亮度直接相加，不需要权重。', 'Add all three brightness values without weights.'),
    'detail-and-noise': pair('空间频率描述亮度变化快慢；高频可能是有用细节，也可能包含噪声。', 'Spatial frequency describes how quickly brightness varies; high frequencies may contain useful detail as well as noise.'),
    'always-noise': pair('所有高频成分都是噪声，应该全部删除。', 'Every high-frequency component is noise and should be removed.'),
    'brightness': pair('频率只表示平均亮度，不能描述条纹疏密。', 'Frequency only describes average brightness, not stripe spacing.'),
    'sample-units': pair('每个周期跨越若干样本；乘以每秒样本数，得到每秒周期数。', 'Each cycle spans several samples; multiplying cycles per sample by samples per second gives cycles per second.'),
    'same-hz': pair('周/像素、周/样本和 Hz 总是同一个单位，不需要换算。', 'Cycles per pixel, cycles per sample and Hz are always the same unit and need no conversion.'),
    'amplitude-hz': pair('提高输入幅度就会按同样比例提高频率。', 'Increasing input amplitude increases frequency by the same factor.'),
    'nonunique': pair('两个不同的原始输入能产生相同输出，所以只凭该输出无法唯一恢复原图。', 'Two different original inputs can produce the same output, so that output alone cannot uniquely recover the original.'),
    'sharpen-exact': pair('任意锐化强度都能准确恢复被滤掉的条纹。', 'Any sharpening strength can exactly restore the removed stripes.'),
    'unique': pair('只要知道滤波权重，所有输入都能由输出唯一确定。', 'Knowing the filter weights always makes every input uniquely recoverable from its output.'),
}


def question(kind, variant):
    if kind not in KINDS or not isinstance(variant, int) or not 0 <= variant < MAX_VARIANTS:
        raise ValueError('Unsupported image check')
    k = variant + 1
    if kind == 'smoothing':
        left, centre, right = 20 + 8*k, 80 + 4*k, 160 - 8*k
        answer = .25*left + .5*centre + .25*right
        prompt = pair(
            rf'一个内部像素及其左右邻居为 $[{left}, {centre}, {right}]$（亮度范围 0–255）。只做一次三点平滑，权重为 $[1/4,1/2,1/4]$。中心输出是多少？选择计算理由。',
            rf'An interior pixel and its neighbours have brightness values $[{left}, {centre}, {right}]$ on a 0–255 scale. Apply one pass of the three-point filter with weights $[1/4,1/2,1/4]$. What is the centre output? Choose the calculation reason.')
        hint = pair('把左、中、右三项分开写：左×1/4，中×1/2，右×1/4。只计算内部中心像素，不需要边界延拓。', 'Write the three terms separately: left × 1/4, centre × 1/2, right × 1/4. This interior centre pixel requires no boundary extension.')
        solution = pair(rf'$y=({left}+2\times{centre}+{right})/4={answer:g}$。权重和为 1，因此对常量输入保持亮度；这不是取最小值，也不是无权相加。', rf'$y=({left}+2\times{centre}+{right})/4={answer:g}$. The weights sum to 1, so a constant input keeps its brightness. This is neither a minimum nor an unweighted sum.')
        label = pair('中心输出亮度', 'Centre output brightness')
        choices, correct, bridge = ['minimum', 'weighted', 'unweighted'], 'weighted', 'convolution'
    elif kind == 'frequency':
        amplitude = 8 + 4*k
        answer = amplitude/2
        prompt = pair(
            rf'无噪声条纹的一行是 $x[n]=128+{amplitude}\cos(\pi n/2)$。在无限序列或周期延拓条件下，用三点滤波 $[1/4,1/2,1/4]$ 平滑一次。条纹的输出幅度是多少（不是平均亮度）？同时选择对高频的正确解释。',
            rf'A row of noise-free stripes is $x[n]=128+{amplitude}\cos(\pi n/2)$. Apply one pass of $[1/4,1/2,1/4]$ to an infinite or periodically extended sequence. What is the output stripe amplitude (not its mean brightness)? Also choose the correct statement about high frequencies.')
        hint = pair(r'把 $\omega=\pi/2$ 代入 $H(e^{j\omega})=(1+\cos\omega)/2$，再用输入幅度乘以响应。题目中的条纹是刻意设计的清晰细节。', r'Substitute $\omega=\pi/2$ into $H(e^{j\omega})=(1+\cos\omega)/2$, then multiply the input amplitude by the response. These stripes are intentionally designed clean detail.')
        solution = pair(rf'$H(e^{{j\pi/2}})=1/2$，所以输出为 $128+{answer:g}\cos(\pi n/2)$，条纹幅度是 ${answer:g}$。平均亮度保持 128。减弱高频会同时减弱某些细节，不能把高频直接等同于噪声。', rf'$H(e^{{j\pi/2}})=1/2$, so the output is $128+{answer:g}\cos(\pi n/2)$, with stripe amplitude ${answer:g}$. Mean brightness remains 128. Attenuating high frequencies also attenuates some detail; high frequency does not mean noise.')
        label = pair('输出条纹幅度', 'Output stripe amplitude')
        choices, correct, bridge = ['always-noise', 'brightness', 'detail-and-noise'], 'detail-and-noise', 'frequency'
    elif kind == 'transfer':
        rate = 800 + 200*k
        answer = rate/4
        prompt = pair(
            rf'现在把同样的四样本周期用于时间信号：$x[n]=3\cos(\pi n/2)$，采样率 $f_s={rate}$ 样本/秒。这里 $n$ 是时间样本编号，不是像素位置。它对应的基带频率是多少 Hz？选择单位换算的理由。',
            rf'Now use the same four-sample period for a time signal: $x[n]=3\cos(\pi n/2)$, sampled at $f_s={rate}$ samples/s. Here $n$ is a time-sample index, not a pixel position. What is its baseband frequency in Hz? Choose the unit-conversion reason.')
        hint = pair(r'先用 $\omega=2\pi f_{\mathrm{sample}}$ 把弧度/样本转换为周/样本，再乘采样率。幅度 3 不决定频率。', r'First use $\omega=2\pi f_{\mathrm{sample}}$ to convert radians/sample to cycles/sample, then multiply by the sampling rate. The amplitude 3 does not determine frequency.')
        solution = pair(rf'$f_{{\mathrm{{sample}}}}=(\pi/2)/(2\pi)=1/4$ 周/样本，因此 $f={rate}/4={answer:g}$ Hz。图像里对应的是每 4 像素一个周期；时间信号的 Hz 必须结合采样率。这里取基带代表，离散采样并不唯一确定所有可能的连续频率。', rf'$f_{{\mathrm{{sample}}}}=(\pi/2)/(2\pi)=1/4$ cycles/sample, so $f={rate}/4={answer:g}$ Hz. The image analogue has one cycle per 4 pixels; Hz for a time signal requires the sampling rate. This is the baseband representative: discrete samples do not uniquely specify every possible continuous frequency.')
        label = pair('基带频率（Hz）', 'Baseband frequency (Hz)')
        choices, correct, bridge = ['same-hz', 'sample-units', 'amplitude-hz'], 'sample-units', 'frequency'
    else:
        c, amplitude = 96 + 4*k, 8 + 4*k
        answer = 0
        prompt = pair(
            rf'在无限序列或偶数长度周期延拓条件下，比较 $x_1[n]={c}$ 与 $x_2[n]={c}+{amplitude}(-1)^n$。对第二个输入做一次三点平滑 $[1/4,1/2,1/4]$，输出中交替条纹的幅度是多少？再选择这对“只凭模糊结果恢复原图”意味着什么。',
            rf'For an infinite sequence or an even-length periodic extension, compare $x_1[n]={c}$ and $x_2[n]={c}+{amplitude}(-1)^n$. After applying one pass of $[1/4,1/2,1/4]$ to the second input, what alternating-stripe amplitude remains? Then choose what this means for recovering an original from its blurred output alone.')
        hint = pair(r'对交替项来说，两个邻居的符号都与中心相反。分别计算三个加权项的总和，再比较两个输入的输出。这里没有使用最初清晰图像作为恢复信息。', r'For the alternating component, both neighbours have the opposite sign to the centre. Add its three weighted terms, then compare the two outputs. The original sharp image is not available as recovery information.')
        solution = pair(rf'交替项系数为 $-{amplitude}/4+{amplitude}/2-{amplitude}/4=0$，也就是 $H(e^{{j\pi}})=0$。两个输出都是常量 ${c}$，因此只凭输出和滤波器无法知道原来是哪一个输入。锐化可以增强剩余变化，不能凭空唯一找回被消除的条纹。', rf'The alternating coefficient is $-{amplitude}/4+{amplitude}/2-{amplitude}/4=0$, equivalently $H(e^{{j\pi}})=0$. Both outputs are the constant ${c}$, so the output and filter alone cannot identify which input was used. Sharpening can enhance remaining variation; it cannot uniquely recover the removed stripes from nothing.')
        label = pair('剩余交替条纹幅度', 'Remaining alternating-stripe amplitude')
        choices, correct, bridge = ['sharpen-exact', 'nonunique', 'unique'], 'nonunique', 'recovery'
    return {'kind': kind, 'variant': variant, 'prompt': prompt, 'number_label': label,
            'choices': choices, 'correct': correct, 'answer': answer, 'hint': hint,
            'solution': solution, 'bridge': bridge}


FEEDBACK = {
    'pass': pair('本题的数值和所选理由都符合判据。这个结果只反映本次限定检查，不代表整门课掌握或长期保持；文字笔记没有被自动评分。', 'The number and selected reason meet this check’s criteria. This result covers only this bounded check, not whole-course mastery or long-term retention; written notes were not automatically graded.'),
    'arithmetic': pair('所选理由符合概念，但数值尚不一致。先检查权重、幅度或单位，再决定是否查看提示。文字笔记保留供你复看，没有被自动评分。', 'The selected reason fits the concept, but the number does not yet match. Check weights, amplitude or units before choosing whether to reveal a hint. Written notes are saved for review, not automatically graded.'),
    'smoothing': pair('局部平滑是带权求和。先列出三个像素各自的贡献，再检查权重之和；它既不是取最小值，也不是把亮度直接相加。', 'Local smoothing is a weighted sum. List each pixel’s contribution and check the sum of the weights; it is neither a minimum operation nor a direct sum of brightness values.'),
    'frequency': pair('先区分平均亮度、条纹幅度和条纹疏密。高频可能描述清晰细节，也可能包含噪声；仅凭频率高低不能判断是否应该删除。', 'Separate mean brightness, stripe amplitude and stripe spacing. High frequencies may describe clean detail or noise; frequency alone cannot decide what should be removed.'),
    'transfer': pair('时间频率需要时间尺度。先得到每个样本对应的周期数，再结合采样率；像素位置本身没有秒这个单位，幅度也不决定频率。', 'A temporal frequency needs a time scale. Find cycles per sample, then use the sampling rate; a pixel position alone carries no seconds, and amplitude does not determine frequency.'),
    'recovery': pair('先比较两个不同输入是否能得到同一输出。如果信息已被这个滤波器消除，知道权重或增强剩余对比度都不足以唯一恢复原输入。', 'First compare whether two different inputs can give the same output. If this filter removes information, knowing its weights or enhancing remaining contrast is not enough to uniquely recover the original.'),
}


def assess(q, number, choice, supported):
    if choice not in q['choices']:
        raise ValueError('invalid_choice')
    value = numeric(number)
    number_ok = math.isclose(value, q['answer'], rel_tol=1e-7, abs_tol=1e-7)
    choice_ok = choice == q['correct']
    passed = number_ok and choice_ok
    return {'passed': passed, 'number_ok': number_ok, 'choice_ok': choice_ok,
            'status': ('supported' if supported else 'independent') if passed else 'needs_review',
            'feedback_code': 'pass' if passed else ('arithmetic' if choice_ok else q['kind']),
            'suggested_bridge': None if passed else q['bridge'],
            'evidence': 'bounded-image-check', 'retention': 'unassessed', 'working_assessed': False}


def localized_result(result, language):
    if result is None:
        return None
    feedback = FEEDBACK[result['feedback_code']][language]
    if result['status'] == 'supported':
        feedback += pair(' 本题或同类题先前已有提示、解答或检查反馈，因此记录为得到支持后的练习。', ' Earlier hints, solutions or check feedback were available on this question or its family, so this is recorded as supported practice.')[language]
    return {**result, 'feedback': feedback}


def new_question(kind, variant=0):
    return {'id': store.uid(), 'kind': kind, 'variant': variant, 'result': None, 'help_exposed': []}


def new_session(course_version):
    return {'id': UNIT_ID, 'unit_id': UNIT_ID, 'course_code': 'ELEC270',
            'course_version': course_version, 'content_version': VERSION, 'revision': 1,
            'stage': 0, 'controls': {'passes': 1, 'row': 48, 'noise': .12, 'pattern': 'scene'},
            'prediction': '', 'reflection': '', 'opened_bridges': [], 'drafts': {},
            'supported_kinds': [], 'questions': [new_question(kind) for kind in KINDS],
            'at': store.now()}


def present(session, history, language):
    body = {k: session[k] for k in ('unit_id', 'course_version', 'content_version', 'revision',
                                   'stage', 'controls', 'prediction', 'reflection', 'opened_bridges', 'drafts', 'at')}
    body.update(language=language, translation_version=TRANSLATION_VERSION, max_variants=MAX_VARIANTS)
    body['questions'] = []
    for state in session['questions']:
        q = question(state['kind'], state['variant'])
        body['questions'].append({
            'id': state['id'], 'kind': state['kind'], 'variant': state['variant'],
            'prompt': q['prompt'][language], 'number_label': q['number_label'][language],
            'choices': [{'id': key, 'label': REASONS[key][language]} for key in q['choices']],
            'help': {key: q[key][language] for key in state['help_exposed']},
            'result': localized_result(state['result'], language),
            'retry_available': state['variant'] + 1 < MAX_VARIANTS,
        })
    body['history'] = [{k: r[k] for k in ('id', 'question_id', 'kind', 'variant', 'at', 'number', 'choice', 'working', 'language', 'exposure_before', 'family_support_before', 'origin')} |
                       {'result': localized_result(r['result'], language)}
                       for r in sorted(history, key=lambda r: r['at'])]
    return body
