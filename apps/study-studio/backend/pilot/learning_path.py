"""Deterministic next actions; a suggestion is not a mastery judgement."""
from datetime import datetime, timezone
from . import teaching


def overview(tasks, attempts, sessions, drafts, now=None):
    now = now or datetime.now(timezone.utc)
    active = sorted((a for a in attempts if a['active']), key=lambda a: a['at'])
    rows=[]
    for key, topic in teaching.TOPICS.items():
        evidence=[a for a in active if a['topic']==key]
        latest=evidence[-1] if evidence else None
        topic_tasks=sorted((t for t in tasks if t['topic']==key),key=lambda t:t['created_at'])
        pending=next((t for t in reversed(topic_tasks) if not any(a['task_id']==t['id'] for a in attempts)),None)
        session=next((s for s in sessions if s['id']==key),None)
        due=bool(latest and latest['result']['passed'] and datetime.fromisoformat(latest['review_due'])<=now)
        if pending: action='resume'; task_id=pending['id']
        elif latest and not latest['result']['passed']: action='revisit';task_id=latest['task_id']
        elif due: action='review';task_id=None
        elif session and session['step']<3: action='guided';task_id=None
        elif latest or (session and session['step']==3): action='practice';task_id=None
        else: action='diagnosis';task_id=None
        rows.append({'topic':key,'week':topic['week'],'action':action,'task_id':task_id,'due_at':latest['review_due'] if latest and latest['result']['passed'] else None,
          'attempts':len(evidence),'independent':sum(a['result']['status']=='independent' for a in evidence),
          'guided_steps':session['step'] if session else 0,'guided_available':key=='ramps',
          'draft_saved':bool(task_id and any(d['id']==task_id for d in drafts)),
          'retention':'unassessed','latest_attempt_id':latest['id'] if latest else None})
    return {'topics':rows,'scope':'numerical-checks-only','generated_at':now.isoformat()}
