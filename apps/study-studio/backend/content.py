"""Original, bounded teaching material. Not an official university handout."""
import copy
import uuid

UNIT = {
    'title': 'From ramps to waveforms',
    'course': 'ELEC270 · Week 1',
    'summary': 'Understand what changes at each event. Build a signal, explain its shape, and check it independently.',
    'scope': 'One focused Week 1 unit: shifted steps and ramps, plateau construction, endpoints and a short energy extension. Not the entire lecture or problem sheet.',
    'objectives': ['Evaluate a shifted ramp', 'Distinguish slope from height', 'Construct a pulse from timed events'],
    'prerequisites': 'Substitution into functions, straight-line slope, and simple algebra. Integration is needed only for the optional extension.',
    'sections': [
        {'id': 'shifts', 'title': 'Read the argument first', 'eyebrow': '01 · Build the foundation', 'minutes': 5,
         'source_refs': ['source-1'], 'body': r'''A ramp is a signal that starts at zero and then grows at a constant rate. We write

$$r(t)=\max(t,0).$$

For negative time its value is zero. For positive time its value equals the time itself. The input is what matters: **replace the whole argument before deciding whether the ramp is active.**

Consider $r(t-2)$. At $t=1$, its argument is $-1$, so the value is zero. At $t=2$, the argument is zero and the value is still zero. At $t=5$, the argument is $3$, so the value is $3$.

The shift changes when growth begins. It does not give the ramp a nonzero starting height:

$$r(t-a)=(t-a)u(t-a).$$

Here the unit step $u(t)$ is zero when $t<0$ and one when $t\geq0$. We use **$u(0)=1$ throughout this unit**. Solve $t-a\geq0$ to find when the shifted ramp becomes active.

### A small foundation bridge

If function substitution feels unfamiliar, treat $r(\square)$ as an instruction: calculate the number in the box, then take the larger of that number and zero. For $r(5-2)$, the two operations are $5-2=3$ and $\max(3,0)=3$.

This distinction will matter when two ramps start at different times. They can later have the same slope while still having different heights.'''},
        {'id': 'plateau', 'title': 'A flat signal need not be zero', 'eyebrow': '02 · Connect expression and shape', 'minutes': 7,
         'source_refs': ['source-2'], 'figure': 'ramps', 'body': r'''Take two ramps with the same slope, one starting two time units later:

$$x(t)=r(t)-r(t-2).$$

Before zero, neither ramp is active, so the difference is zero. Between zero and two, only the first ramp contributes. The result therefore grows as $x(t)=t$.

After two, both ramps are active. Expand the actual values before subtracting:

$$x(t)=t-(t-2)=2,\qquad t\geq2.$$

The first ramp has accumulated a head start of two. Both now grow at the same rate, so that separation stays constant. **The second ramp cancels further growth, not the height already reached.**

### Read the two views together

The graph below shows the two inputs and their difference. At $t=5$, the heights of the individual ramps are $5$ and $3$. Their slopes match, but their values do not. Subtracting the values leaves $2$.

More generally, $m[r(t-a)-r(t-b)]$ with $b>a$ grows for $b-a$ time units. Its final height is

$$H=m(b-a).$$

The duration and slope determine the height. A negative slope produces a negative plateau; the same reasoning still applies.

### Check what your explanation actually claims

“The slope is zero” means the value is no longer changing. “The value is zero” identifies one particular height. These statements are different. Test your explanation at one time and then use the interval expression to show why it remains true.'''},
        {'id': 'events', 'title': 'Build a signal from its events', 'eyebrow': '03 · Use the idea independently', 'minutes': 6,
         'source_refs': ['source-3'], 'body': r'''We have built a plateau, but sometimes the signal must return to zero. A step changes the height instantly; a ramp changes the slope from its starting time.

For the preceding signal, the plateau height is two. To remove it at $t=4$, subtract a step of height two:

$$y(t)=r(t)-r(t-2)-2u(t-4).$$

There are three events. At zero the slope increases by one. At two the slope decreases by one, leaving a constant height. At four the height decreases by two, returning the signal to zero.

### Why the last coefficient is two

The signal grew with slope one for two time units, so it reached $1\times2=2$. The final step removes exactly this accumulated height. Its coefficient comes from the height, not merely from the earlier ramp coefficients.

At the switching time itself, $u(0)=1$, so $y(4)=4-2-2=0$. Just before four the value is two. Checking the endpoint makes the convention visible.

### A reusable method

Mark the event times. Work out the slope on each interval. Add a ramp for each change in slope, then a step for each jump in height. Finally substitute a time from each interval and every switching endpoint.

### Optional extension: connect shape and energy

For this real continuous-time pulse, energy is the integral of its square. The growing part occupies $0\leq t<2$; the plateau occupies $2\leq t<4$:

$$E=\int_0^2t^2\,dt+\int_2^4 2^2\,dt=\frac{8}{3}+8=\frac{32}{3}.$$

A single endpoint does not change this integral. For a discrete sequence, an individual sample contributes to the energy sum and cannot be ignored. This extension is not required for the construction check in this unit.'''}
    ]
}

SOURCES = [
    {'id': 'source-1', 'name': 'Original teaching brief · §1', 'locator': 'Shifted ramp and step conventions', 'text': r'r(t)=max(t,0); u(t)=0 for t<0 and 1 for t>=0. r(t-a) starts at zero at t=a. Evaluate the entire argument before applying the function.'},
    {'id': 'source-2', 'name': 'Original teaching brief · §2', 'locator': 'Plateau from a ramp difference', 'text': r'r(t)-r(t-2) is 0 for t<0, t for 0<=t<2, and 2 for t>=2. Equal slopes do not imply equal values. General plateau height m(b-a).'},
    {'id': 'source-3', 'name': 'Original teaching brief · §3', 'locator': 'Timed construction and endpoints', 'text': r'y(t)=r(t)-r(t-2)-2u(t-4). Final step removes height 2. y(4)=0 with u(0)=1. Energy: 8/3+8=32/3. Original adaptation, not official lecture text.'}
]

REMEDIATIONS = {
    'substitution': {'title': 'Start with the input to each ramp', 'hypothesis': 'The shifted-ramp value needs another check. This could be substitution or a reading slip.',
        'body': r'''At $t=5$, the expression $r(t-2)$ becomes $r(3)$, not $r(5)-2$ as a general rule. Compute the argument, then apply $r(s)=\max(s,0)$. Try $t=1$ as well: $r(-1)=0$.

Make a two-column table: **argument first, ramp value second**. Once those values are clear, subtract the two ramp heights. Do not infer the difference from their slopes.''', 'section': 'shifts'},
    'height': {'title': 'Separate a zero slope from a zero height', 'hypothesis': 'Your substitution works, but the tail values suggest slope and height may have been mixed up. A subtraction slip is another possibility.',
        'body': r'''Compare the heights at one time: at $t=5$, the two ramps have values $5$ and $3$. Their difference is $2$. Both grow by one over the next time unit, so their difference stays $2$.

$$t-(t-2)=2.$$

Cancelling growth makes a flat tail. It does not erase the head start. Say what remains after subtraction, then explain why it stays unchanged.''', 'section': 'plateau'},
    'construction': {'title': 'Work through the three events', 'hypothesis': 'At least one coefficient or checkpoint differs from the task. Check the event timing before attributing it to a broader conceptual difficulty.',
        'body': r'''Use the slope specified by the task for the first ramp. At the end of growth, add the opposite slope. Work out the accumulated height as **slope × elapsed time**. The last step must remove that height.

At the final switching time, include the step because $u(0)=1$. Check one point on the rising interval, one on the plateau, and the switching endpoint.''', 'section': 'events'},
    'reasoning': {'title': 'Connect the calculation to a reason', 'hypothesis': 'The numerical checks pass, but the selected explanation does not yet match them.',
        'body': r'''Keep the correct numerical values. Now distinguish what each operation changes. A delayed ramp changes the slope from its start time. A step changes the height. Equal slopes preserve an existing separation; they do not make the two heights identical.

Your written step is saved for review. Prepared mode checks the numerical fields and the reasoning choice; it does not semantically grade free writing.''', 'section': 'plateau'},
    'ready': {'title': 'Now try a fresh construction', 'hypothesis': 'The numerical fields and reasoning choice match this task. This is narrow evidence about the checks you just completed.',
        'body': 'Continue to a new construction without hints if you want to check independence. Related teaching is allowed; seeing this exact question’s answer or feedback changes how its later attempts are described. Delayed retention remains unassessed.', 'section': 'events'}
}

def checkpoint():
    return {'id': 'checkpoint-v1', 'kind': 'checkpoint', 'title': 'Does cancelling growth cancel the height?',
        'prompt': r'Use $r(t)=\max(t,0)$. For $x(t)=r(t)-r(t-2)$, evaluate the fields below. Then choose the explanation that matches your calculation.',
        'fields': [{'id': 'shift', 'label': 'r(5 − 2)', 'answer': 3}, {'id': 'tail3', 'label': 'x(3)', 'answer': 2}, {'id': 'tail5', 'label': 'x(5)', 'answer': 2}],
        'choices': ['The tail is zero because the slopes cancel.', 'The tail stays at height 2: equal slopes preserve the accumulated separation.', 'The second ramp starts at height 2.'], 'correct_choice': 1,
        'hint': r'At $t=5$, find the two heights separately: what are $r(5)$ and $r(5-2)$? Then subtract.',
        'solution': r'$r(5-2)=3$, $x(3)=3-1=2$, $x(5)=5-3=2$. After two, $t-(t-2)=2$: the slope stops changing the height, but the height remains two.',
        'objective': 'Distinguish slope from height', 'source_refs': ['source-1', 'source-2']}

def transfer(number=0):
    # Six disjoint event patterns; no question is silently recycled.
    params = [(1,4,6,2),(2,6,9,3),(3,5,8,4),(1,6,8,3),(4,7,10,2),(2,5,7,4)]
    if number >= len(params):
        return None
    a,b,c,m=params[number]; h=m*(b-a)
    return {'id': 'transfer-'+uuid.uuid4().hex[:12], 'kind': 'transfer', 'title': 'Build a new pulse', 'variant': number,
        'prompt': f'A continuous-time signal is zero before $t={a}$. It grows with slope ${m}$ until $t={b}$, stays flat until $t={c}$, and is zero at and after $t={c}$. Use $u(0)=1$. Complete the coefficients and check its value at the final event.',
        'template': f'$x(t)=A\,r(t-{a})+B\,r(t-{b})+C\,u(t-{c})$',
        'fields': [{'id':'a','label':'A · first ramp','answer':m},{'id':'b','label':'B · delayed ramp','answer':-m},{'id':'c','label':'C · final step','answer':-h},{'id':'end','label':f'x({c}) · exact endpoint','answer':0}],
        'choices': ['Both the ramp and the step change only the slope.', 'Stopping growth also removes the accumulated height.', 'The delayed ramp stops growth; the final step removes the plateau height.'], 'correct_choice': 2,
        'hint': f'The growth lasts ${b-a}$ time units. First calculate slope × duration. The final step removes that height; it is active at $t={c}$.',
        'solution': f'$A={m}$, $B={-m}$, $C={-h}$, and $x({c})=0$. The plateau is ${m}({b}-{a})={h}$. At ${c}$, the two ramps leave ${h}$ and the step subtracts ${h}$.',
        'objective': 'Construct a pulse from timed events', 'source_refs': ['source-3']}

def prepared_unit():
    return copy.deepcopy(UNIT)

def public_task(task):
    value = copy.deepcopy(task)
    value.pop('correct_choice', None)
    value.pop('hint', None)
    value.pop('solution', None)
    for field in value['fields']: field.pop('answer', None)
    return value

TUTOR = {
    'substitution': {'question': 'How do I evaluate a shifted ramp?', 'body': REMEDIATIONS['substitution']['body'], 'source_refs':['source-1']},
    'height': {'question': 'Why does a flat tail have a nonzero value?', 'body': REMEDIATIONS['height']['body'], 'source_refs':['source-2']},
    'construction': {'question': 'When should I use a step rather than a ramp?', 'body': REMEDIATIONS['construction']['body'], 'source_refs':['source-3']}
}
