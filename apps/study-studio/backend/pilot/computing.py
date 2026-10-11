"""Original bilingual starter packs. These are bounded checks, not whole-course exams."""
from . import store


def pick(zh, en, language):
    return en if language == 'en' else zh

# Weeks refer to the local course reading plan. Content remains usable without that plan.
PACKS = {
    'requirements': ('COMP201', 2, {
        'title': ('需求与可验证的验收条件', 'Requirements and testable acceptance criteria'),
        'objective': ('区分系统行为与质量约束，把模糊要求改写成可观察的验收条件。', 'Distinguish behaviour from quality constraints and make acceptance criteria observable.'),
        'bridge': ('功能需求说明系统做什么；质量需求约束它做得怎样。先找行为、条件和可以测量的结果。安全要求也可能包含具体功能，不能只靠关键词分类。', 'A functional requirement specifies behaviour; a quality requirement constrains how well it is delivered. Identify the action, conditions and observable outcome. Security requirements can include concrete functions: do not classify by keywords alone.'),
        'visual': ('画出“用户动作 → 系统响应”的故事，再在箭头旁写时间、负载等约束。例如“查找订单 → 显示结果”是行为，“200名并发用户时95%的请求在2秒内返回”是质量约束。', 'Draw “user action → system response”, then annotate the arrow with constraints such as latency and load. “Find order → show result” is behaviour; “95% of requests return within two seconds with 200 concurrent users” is a quality constraint.'),
        'algebra': ('将要求写成 Given（前提）/ When（动作）/ Then（可观察结果）。百分位指标应说明采样范围、负载和阈值；检查通过数/总数是否达到约定比例。单次成功不能证明长期满足SLA。', 'Use Given (preconditions), When (action), Then (observable result). A percentile criterion needs a sample definition, load and threshold. Compare passing requests / total requests with the required proportion. One successful run does not establish a long-term SLA.'),
        'example': ('例：在固定测试环境采集100次请求，要求至少90%在1秒内完成。如果只有89次满足阈值，则本次验收不通过。改写“搜索要快”：指定数据量、并发数、阈值和测量窗口，而不是直接承诺一个未经测量的速度。', 'Example: in a fixed test environment, at least 90 of 100 requests must finish within one second. With 89 passing requests, this run fails acceptance. Replace “search should be fast” with a dataset, concurrency, threshold and measurement window, then measure it.'),
    }),
    'petri': ('COMP201', 4, {
        'title': ('Petri网：使能与发射', 'Petri nets: enabling and firing'),
        'objective': ('先判断每个输入库所是否满足弧权重，再计算一次发射后的标识。', 'Check every input-place requirement before calculating the marking after one firing.'),
        'bridge': ('库所存放token，变迁通过输入弧消耗token，并通过输出弧产生token。普通加权P/T网中，变迁使能要求每个输入库所的token都足够；总数足够并不代表每个库所都足够。', 'Places hold tokens. A transition consumes tokens through input arcs and produces them through output arcs. In an ordinary weighted P/T net, every input place must supply its required tokens; a sufficient total is not enough.'),
        'visual': ('先在每个输入库所圈出将被取走的token，再向输出库所添加token。若任何一个输入库所不够，就停下；不能先发射再出现负token。自环同样要先检查输入。', 'Circle the tokens to be removed from each input place, then add the output tokens. Stop if any input place has too few: firing cannot create a negative marking. A self-loop still requires the input check.'),
        'algebra': ('记当前标识为M，输入权重为Pre，输出权重为Post。只有M逐分量不小于Pre时，才允许计算 M′ = M − Pre + Post。token总数是否守恒由具体弧权重决定。', 'Let M be the marking, Pre the input weights and Post the output weights. Firing requires M ≥ Pre componentwise; then M′ = M − Pre + Post. Token conservation depends on the actual arc weights.'),
        'example': ('例：M=(3,1)，某变迁消耗P的2个token并给Q产生1个token，发射后M′=(1,2)。总数从4变3，说明该网的token总数并非自动守恒。若P只有1个token，该变迁不能发射。', 'Example: M=(3,1). A transition consumes two tokens from P and produces one in Q, giving M′=(1,2). The total falls from four to three: token counts are not automatically conserved. With only one token in P, this transition is disabled.'),
    }),
    'boundaries': ('COMP201', 8, {
        'title': ('边界值与等价类测试', 'Boundary-value and equivalence-partition testing'),
        'objective': ('从整数闭区间规范构造上下边界及相邻无效输入，并说明覆盖的范围。', 'Derive boundary and adjacent invalid inputs from an integer interval specification and state the coverage limits.'),
        'bridge': ('闭区间[L,U]包含L和U。整数输入的相邻无效值是L−1和U+1。“有效区间”是一种等价类，区间两侧是两种无效类；还可能有类型错误等其他类别。', 'The closed interval [L,U] includes L and U. For integers, the adjacent invalid values are L−1 and U+1. The valid range is one equivalence partition; the two outside ranges are two invalid partitions. Type errors may require additional partitions.'),
        'visual': ('在数轴标出L−1、L、L+1，以及U−1、U、U+1。把每个点画在允许/拒绝区域内，特别检查端点是否包含。真实测试还需要预期输出和可观察的测试结果。', 'Mark L−1, L, L+1, U−1, U and U+1 on a number line. Place them in the accepted or rejected region, paying attention to endpoint inclusion. Real tests also need expected outputs and observed results.'),
        'algebra': ('对于足够宽的整数区间，稳健边界检查可取{L−1,L,L+1,U−1,U,U+1}。如果规范是开区间、浮点数或多个字段互相约束，必须重新推导，不能机械套用六个数字。', 'For a sufficiently wide integer range, robust boundary checks can use {L−1,L,L+1,U−1,U,U+1}. Open intervals, floating-point values and constraints across fields require a different derivation; six numbers are not a universal recipe.'),
        'example': ('例：允许整数数量[5,12]，可检查4（拒绝）、5和6（接受）、11和12（接受）、13（拒绝）。这有助于发现把≤写成<的错误，但不能证明程序没有其他缺陷。', 'Example: for integer quantities [5,12], check 4 (reject), 5 and 6 (accept), 11 and 12 (accept), and 13 (reject). These checks can reveal < versus ≤ defects, but cannot prove the absence of other bugs.'),
    }),
    'joins': ('COMP207', 1, {
        'title': ('连接、主键与结果行数', 'Joins, keys and result cardinality'),
        'objective': ('根据具体表数据预测INNER JOIN与LEFT JOIN结果，区分COUNT(*)与COUNT(列)。', 'Predict INNER JOIN and LEFT JOIN results from concrete rows; distinguish COUNT(*) from COUNT(column).'),
        'bridge': ('主键唯一且不为NULL，外键可以在多行中重复。一个顾客有多张订单，因此连接结果不一定每个顾客只有一行。INNER JOIN只保留匹配行；LEFT JOIN还保留左表中没有匹配的行。', 'A primary key is unique and non-NULL; a foreign key may repeat in many rows. A customer can have multiple orders, so a join need not return one row per customer. INNER JOIN keeps matches; LEFT JOIN also retains unmatched left-side rows.'),
        'visual': ('给顾客和订单之间逐一连线，每条匹配线产生一行。LEFT JOIN给没有连线的顾客补上一行，订单列为NULL。COUNT(*)数这些行，COUNT(order_id)只数非NULL的订单ID。', 'Draw a line for each customer–order match. Each line produces a row. LEFT JOIN adds one NULL-extended row for a customer with no matches. COUNT(*) counts those rows; COUNT(order_id) counts only non-NULL order IDs.'),
        'algebra': ('如果顾客i有nᵢ张匹配订单，内连接行数是Σnᵢ，左连接行数是Σmax(1,nᵢ)。这要求连接条件是订单外键=顾客主键，且顾客主键唯一。SQL通常保留重复行，不能默认自动去重。', 'If customer i has nᵢ matching orders, INNER JOIN produces Σnᵢ rows and LEFT JOIN produces Σmax(1,nᵢ). This assumes the join matches an order foreign key to a unique customer primary key. SQL generally retains duplicates; do not assume implicit deduplication.'),
        'example': ('例：顾客A有2张订单，B没有订单。内连接有2行，左连接有3行。按顾客分组后，B的COUNT(*)为1，COUNT(order_id)为0。对右表列在WHERE中加过滤条件可能去掉补出的NULL行。', 'Example: A has two orders and B has none. INNER JOIN yields two rows, LEFT JOIN three. After grouping by customer, B has COUNT(*)=1 but COUNT(order_id)=0. A WHERE filter on the right table can remove NULL-extended rows.'),
    }),
    'aggregation': ('COMP207', 2, {
        'title': ('WHERE、GROUP BY与HAVING', 'WHERE, GROUP BY and HAVING'),
        'objective': ('按行过滤、分组、聚合和组过滤的顺序推导查询结果。', 'Trace row filtering, grouping, aggregation and group filtering to determine query results.'),
        'bridge': ('WHERE先筛选输入行，GROUP BY把剩余行分组，聚合函数计算每组结果，HAVING再筛选组。SELECT列必须符合所用数据库的分组规则；本练习只选择分组键和聚合值。', 'WHERE filters input rows; GROUP BY forms groups; aggregate functions compute group values; HAVING filters groups. SELECT expressions must follow the database’s grouping rules. This exercise selects only grouping keys and aggregates.'),
        'visual': ('用四个盒子表示流水线：原表 → 过滤后的行 → 每组的小堆 → 通过阈值的组。每一步都写下剩余数据。不要把已经被WHERE移除的行加回SUM中。', 'Draw four boxes: original rows → filtered rows → grouped piles → groups passing the threshold. Write down the remaining data at each step. Do not add rows removed by WHERE back into SUM.'),
        'algebra': ('查询 SELECT team,SUM(amount) FROM Sales WHERE amount>=k GROUP BY team HAVING SUM(amount)>h，先逐行比较amount>=k，再按team求和，最后比较组总和>h。注意两个条件的≥和>不同。', 'For SELECT team,SUM(amount) FROM Sales WHERE amount>=k GROUP BY team HAVING SUM(amount)>h, compare each amount with k, sum by team, then compare each total with h. Notice the inclusive row threshold and strict group threshold.'),
        'example': ('例：A组销售额为1、4、6，B组为2、3。WHERE amount>=3后，A保留4、6，总和10；B只保留3，总和3。HAVING SUM(amount)>5只留下A。', 'Example: A has sales 1,4,6; B has 2,3. WHERE amount>=3 keeps A’s 4 and 6 (sum 10) and B’s 3 (sum 3). HAVING SUM(amount)>5 retains only A.'),
    }),
    'serial': ('COMP207', 3, {
        'title': ('冲突与可串行化', 'Conflicts and serialisability'),
        'objective': ('识别跨事务同数据项且至少一次写入的冲突，建立先行图并检查环。', 'Identify cross-transaction same-item conflicts with at least one write; build a precedence graph and test for cycles.'),
        'bridge': ('两操作构成冲突需同时满足：属于不同事务、访问同一数据项、至少一个是写。两个读操作不冲突。本单元判断冲突可串行化，不据此推断可恢复性或其他串行化定义。', 'Operations conflict when they belong to different transactions, access the same item, and at least one is a write. Two reads do not conflict. This unit checks conflict serialisability, not recoverability or other definitions of serialisability.'),
        'visual': ('每个事务画成一个点。按执行顺序遇到冲突，就从较早操作的事务画箭头到较晚的事务。A→B和B→A同时存在会形成环；同向的多次冲突只形成一个有向边。', 'Draw a node for each transaction. For every conflict, draw an edge from the earlier operation’s transaction to the later one. A→B and B→A create a cycle. Repeated conflicts in one direction still contribute just one distinct edge.'),
        'algebra': ('完整检查每一对冲突操作，然后对先行图做环检测。图无环当且仅当该调度冲突可串行化，拓扑序给出一个等价串行顺序。只检查相邻操作会漏掉冲突。', 'Check every conflicting pair, then test the precedence graph for cycles. A schedule is conflict serialisable exactly when its graph is acyclic; a topological order gives an equivalent serial order. Checking only adjacent operations can miss conflicts.'),
        'example': ('例：rA(x), wA(x), rB(x), wB(x)只有A→B，等价于A后B。若顺序是rA(x), rB(x), wA(x), wB(x)，则rB在wA之前给出B→A，其他冲突给出A→B，因此有环。', 'Example: rA(x), wA(x), rB(x), wB(x) has only A→B and is equivalent to A then B. In rA(x), rB(x), wA(x), wB(x), rB before wA adds B→A while other conflicts add A→B, so the graph has a cycle.'),
    }),
}


def topics(code=None, language='zh-CN'):
    result = {}
    for key, (course, week, content) in PACKS.items():
        if code and code != course:
            continue
        text = {k: pick(*v, language) for k, v in content.items()}
        result[key] = {'title': text['title'], 'objective': text['objective'], 'example': text['example'],
                       'week': week, 'focus': '', 'routes': {k: text[k] for k in ('bridge', 'visual', 'algebra')}}
    return result


def task(key, phase, number, language='zh-CN'):
    if key not in PACKS or phase not in ('diagnosis', 'practice', 'review') or not 0 <= number < 24:
        raise ValueError('这组已核查参数已用完，请复习记录或选择其他主题。')
    tr = lambda zh, en: pick(zh, en, language)
    k = number + 1 + (24 if phase == 'review' else 0) + (3 if phase == 'practice' else 0)
    code = PACKS[key][0]; topic = topics(code, language)[key]
    fields = []
    def field(id, zh, en, answer, route, choices=None):
        value = {'id': id, 'label': tr(zh, en), 'answer': answer, 'route': route}
        if choices: value['choices'] = [{'value': str(v), 'label': tr(z, e)} for v, z, e in choices]
        fields.append(value)
    yesno = [(1, '是', 'Yes'), (0, '否', 'No')]
    if key == 'requirements':
        quality = k % 2 == 1
        statement = tr(f'在指定负载下，至少90%的搜索请求在{k+1}秒内返回结果。', f'Under the specified load, at least 90% of search requests return within {k+1} seconds.') if quality else tr('用户提交订单编号后，系统显示该订单状态。', 'After a user submits an order ID, the system displays that order’s status.')
        count = 20 * (k + 1); minimum = count * 9 // 10; observed = minimum - (1 if quality else 0)
        prompt = tr(f'要求：“{statement}” 判断它主要表达功能还是质量约束。另一次固定环境验收要求至少90%的请求满足时间阈值，共测{count}次，其中{observed}次满足。给出最低通过次数并判断本次验收。写出还应控制的一项测量条件。', f'Requirement: “{statement}” Classify its primary meaning. Separately, an acceptance run requires at least 90% of requests to meet a latency threshold. Out of {count} requests, {observed} meet it. Give the minimum passing count and decide whether this run passes. Explain one measurement condition that must be controlled.')
        field('type', '需求类型', 'Requirement type', 2 if quality else 1, 'bridge', [(1, '功能需求', 'Functional requirement'), (2, '质量约束', 'Quality constraint')])
        field('minimum', '最低通过次数', 'Minimum passing count', minimum, 'algebra')
        field('passes', '本次验收通过？', 'Does this run pass?', int(observed >= minimum), 'visual', yesno)
        hint = tr('分类看陈述的核心含义；验收比例的分母是总请求数。', 'Classify the statement’s primary meaning; use all requests as the denominator.')
        solution = tr(f'类型为{"质量约束" if quality else "功能需求"}；最低次数={count}×0.9={minimum}。实际{observed}次，因此{"通过" if observed>=minimum else "不通过"}。还应固定数据规模、并发数等测量条件。', f'Type: {"quality constraint" if quality else "functional requirement"}. Minimum={count}×0.9={minimum}; observed={observed}, so the run {"passes" if observed>=minimum else "fails"}. Control conditions such as dataset size and concurrency.')
    elif key == 'petri':
        p, q, weight = k+2, k, 2
        prompt = tr(f'普通加权P/T网中，P有{p}个token，Q有{q}个token。变迁T从P消耗{weight}个token，向Q产生1个token，无其他弧。判断T现在能否发射、一次发射后P/Q的token数，以及最多能连续发射几次。解释为何总token数不必守恒。', f'In an ordinary weighted P/T net, P has {p} tokens and Q has {q}. Transition T consumes {weight} from P and produces one in Q; there are no other arcs. Is T enabled? Give P and Q after one firing and the maximum consecutive firings. Explain why total tokens need not be conserved.')
        field('enabled', '现在使能？', 'Enabled now?', 1, 'bridge', yesno)
        field('P', '一次发射后P', 'P after one firing', p-weight, 'visual')
        field('Q', '一次发射后Q', 'Q after one firing', q+1, 'visual')
        field('firings', '最多连续发射次数', 'Maximum consecutive firings', p//weight, 'algebra')
        hint = tr('每次从P减2、向Q加1；检查输入库所决定使能。', 'Each firing removes two from P and adds one to Q. Check the input place to determine enabling.')
        solution = tr(f'使能，因为{p}≥2。一次后标识为({p-2},{q+1})；最多⌊{p}/2⌋={p//2}次。每次总数减少1。', f'Enabled because {p}≥2. The next marking is ({p-2},{q+1}); maximum firings=⌊{p}/2⌋={p//2}. The total falls by one per firing.')
    elif key == 'boundaries':
        lo, hi = k+5, k+15
        prompt = tr(f'规范只允许整数数量在闭区间[{lo},{hi}]内。请设计六个边界及紧邻边界的测试输入（从小到大），并在过程说明中写出哪些应被拒绝。这里只判断整数边界，其他输入类型另需测试。', f'The specification accepts integer quantities in the closed interval [{lo},{hi}]. Give six boundary and adjacent inputs in ascending order and explain which must be rejected. This checks integer boundaries only; other input types need separate tests.')
        for id, z, e, answer in [('below','下界外侧','Just below lower bound',lo-1),('lower','下界','Lower bound',lo),('above','下界内侧','Just above lower bound',lo+1),('inside','上界内侧','Just below upper bound',hi-1),('upper','上界','Upper bound',hi),('outside','上界外侧','Just above upper bound',hi+1)]:
            field(id,z,e,answer,'bridge' if id in ('lower','upper') else 'visual')
        hint = tr('闭区间包含两端；相邻整数距离1。', 'A closed interval includes both endpoints; adjacent integers differ by one.')
        solution = tr(f'输入为{lo-1},{lo},{lo+1},{hi-1},{hi},{hi+1}。首尾拒绝，其余接受。', f'Inputs: {lo-1},{lo},{lo+1},{hi-1},{hi},{hi+1}. Reject the first and last; accept the others.')
    elif key == 'joins':
        a, c = k+1, k+2
        prompt = tr(f'Customers主键id，三位顾客A/B/C分别有{a}/0/{c}张订单。Orders.order_id为非NULL主键，customer_id为指向顾客的外键，无其他订单。按顾客id=订单customer_id连接：INNER JOIN和LEFT JOIN各几行？LEFT JOIN按顾客分组后，B的COUNT(*)与COUNT(order_id)各是多少？解释NULL补行。', f'Customers has primary key id. Customers A/B/C have {a}/0/{c} orders respectively. Orders.order_id is a non-NULL primary key and customer_id references Customers; there are no other orders. Join on customer id: how many rows do INNER JOIN and LEFT JOIN return? After LEFT JOIN and grouping by customer, what are B’s COUNT(*) and COUNT(order_id)? Explain the NULL-extended row.')
        for id,z,e,ans,route in [('inner','内连接行数','INNER JOIN rows',a+c,'algebra'),('left','左连接行数','LEFT JOIN rows',a+c+1,'visual'),('star','B的COUNT(*)','B: COUNT(*)',1,'bridge'),('column','B的COUNT(order_id)','B: COUNT(order_id)',0,'bridge')]: field(id,z,e,ans,route)
        hint = tr('没有订单的B在左连接中仍保留一行；COUNT(列)不数NULL。', 'LEFT JOIN retains B as one row even without orders. COUNT(column) excludes NULL.')
        solution = tr(f'内连接{a+c}行，左连接{a+c+1}行。B的COUNT(*)=1，COUNT(order_id)=0。', f'INNER JOIN: {a+c} rows; LEFT JOIN: {a+c+1}. B has COUNT(*)=1 and COUNT(order_id)=0.')
    elif key == 'aggregation':
        prompt = tr(f'Sales(team,amount)有五行：A:{k-1},{k+2},{k+4}；B:{k},{k-1}。执行下面查询。WHERE后剩几行？HAVING之前A与B各自总和是多少？最终返回几组？请写出中间表。', f'Sales(team,amount) has five rows: A:{k-1},{k+2},{k+4}; B:{k},{k-1}. Run the query below. How many rows survive WHERE? What are A’s and B’s sums before HAVING? How many groups are returned? Show the intermediate rows.') + f'\n\n```sql\nSELECT team, SUM(amount)\nFROM Sales\nWHERE amount >= {k}\nGROUP BY team\nHAVING SUM(amount) > {k};\n```'
        for id,z,e,ans,route in [('rows','WHERE后行数','Rows after WHERE',3,'bridge'),('A','A组总和','A sum',2*k+6,'algebra'),('B','B组总和','B sum',k,'algebra'),('groups','最终组数','Returned groups',1,'visual')]: field(id,z,e,ans,route)
        hint = tr('先删去小于阈值的行。HAVING使用严格大于，不是大于等于。', 'Remove rows below the threshold first. HAVING uses strictly greater than, not greater than or equal.')
        solution = tr(f'保留A的{k+2},{k+4}以及B的{k}，共3行。A总和{2*k+6}，B总和{k}。只有A严格超过{k}，最终1组。', f'Keep A’s {k+2},{k+4} and B’s {k}: three rows. A sums to {2*k+6}, B to {k}. Only A exceeds {k}, so one group remains.')
    else:
        cyclic = k % 2 == 1
        schedule = f'rA(x{k}), rB(x{k}), wA(x{k}), wB(x{k})' if cyclic else f'rA(x{k}), wA(x{k}), rB(x{k}), wB(x{k})'
        prompt = tr(f'调度为：{schedule}。r/w表示读/写，A/B表示事务，所有操作访问同一数据项x{k}。先行图有A→B吗？有B→A吗？有几条不同的有向边？是否冲突可串行化？过程说明中列出产生每条边的冲突操作。', f'Schedule: {schedule}. r/w mean read/write; A/B are transactions; every operation accesses x{k}. Does the precedence graph contain A→B? B→A? How many distinct directed edges are there? Is it conflict serialisable? Identify a conflicting pair for each edge in your working.')
        field('AB','存在A→B？','A→B exists?',1,'bridge',yesno)
        field('BA','存在B→A？','B→A exists?',int(cyclic),'visual',yesno)
        field('edges','不同有向边数','Distinct directed edges',2 if cyclic else 1,'algebra')
        field('serialisable','冲突可串行化？','Conflict serialisable?',int(not cyclic),'algebra',yesno)
        hint = tr('同项且至少一次写才冲突；检查所有跨事务操作对。', 'Same item and at least one write are required. Check every cross-transaction pair.')
        solution = tr('rA先于wB产生A→B。'+('rB先于wA产生B→A，共2条边，有环，因此不冲突可串行化。' if cyclic else 'A的所有操作先于B；只有A→B这一条边，无环，等价串行顺序为A再B。'), 'rA before wB gives A→B. '+('rB before wA gives B→A: two edges form a cycle, so the schedule is not conflict serialisable.' if cyclic else 'All A operations precede B: the only edge is A→B, with no cycle. Equivalent serial order: A then B.'))
    phase_name = {'diagnosis': tr('前置诊断','Diagnostic check'), 'practice': tr('新的独立练习','Fresh independent practice'), 'review': tr('延迟复查','Review check')}[phase]
    return {'id':f'{code.lower()}:{key}:v1:{phase}:{number}', 'course_code':code,'topic':key,'phase':phase,'number':number,'family':key+'-v1','version':'1','title':phase_name+' · '+topic['title'],'objective':topic['objective'],'origin':'authored-pilot','source_note':tr('原创入门检查；不是官方试题，不代表整门课的考核覆盖。','Original starter check; not an official question or full-course assessment.'),'fields':fields,'prompt':prompt,'hint':hint,'solution':solution,'created_at':store.now()}
