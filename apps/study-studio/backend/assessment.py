"""Narrow deterministic checks; no evaluation of untrusted Python or free prose."""
import ast
import math
import operator
from .content import REMEDIATIONS

def numeric(text):
    value = str(text).strip().replace('−','-').replace('×','*').replace('÷','/')
    if len(value)>80: raise ValueError('Keep each numerical answer short.')
    try: tree=ast.parse(value,mode='eval')
    except (SyntaxError, ValueError): raise ValueError('Use a number or simple arithmetic, such as 3/2.')
    ops={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv}
    def evaluate(node, depth=0):
        if depth>8: raise ValueError('Expression is too complex.')
        if isinstance(node,ast.Constant) and type(node.value) in (int,float): return float(node.value)
        if isinstance(node,ast.UnaryOp) and type(node.op) in (ast.USub,ast.UAdd):
            return (-1 if isinstance(node.op,ast.USub) else 1)*evaluate(node.operand,depth+1)
        if isinstance(node,ast.BinOp) and type(node.op) in ops:
            return ops[type(node.op)](evaluate(node.left,depth+1),evaluate(node.right,depth+1))
        raise ValueError('Use a number or simple arithmetic, such as 3/2.')
    try: result=evaluate(tree.body)
    except (ZeroDivisionError,OverflowError): raise ValueError('The expression must have a finite numerical value.')
    if not math.isfinite(result) or abs(result)>1e12: raise ValueError('The answer must be a finite number within the supported range.')
    return result

def assess(task, answers, choice, exposed=False, previous_attempts=0):
    if set(answers)!=set(f['id'] for f in task['fields']): raise ValueError('Complete every numerical field for this task.')
    if type(choice) is not int or not 0<=choice<len(task['choices']): raise ValueError('Choose an explanation before checking.')
    checks={f['id']: math.isclose(numeric(answers[f['id']]),f['answer'],rel_tol=1e-7,abs_tol=1e-7) for f in task['fields']}
    reasoning=choice==task['correct_choice']; correct=all(checks.values()) and reasoning
    if correct: strategy='ready'
    elif task['kind']=='checkpoint' and not checks.get('shift',True): strategy='substitution'
    elif task['kind']=='checkpoint' and not all(checks.values()): strategy='height'
    elif all(checks.values()) and not reasoning: strategy='reasoning'
    else: strategy='construction'
    status='needs_review'
    if correct:
        status='independent' if task['kind']=='transfer' and not exposed and previous_attempts==0 else 'supported'
    return {'correct':correct,'checks':checks,'reasoning_correct':reasoning,'status':status,'strategy':strategy,
            'support':REMEDIATIONS[strategy].copy(),
            'scope':'Numerical fields and selected explanation only. Written working is stored for review, not semantically graded.',
            'retention':'unassessed'}
