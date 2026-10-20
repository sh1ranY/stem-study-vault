"""Owner- and course-scoped image unit persistence, separate from course mastery."""
import hashlib
from typing import Literal, Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import update
from . import store, catalog, image_learning as lesson


class Body(BaseModel):
    model_config = ConfigDict(extra='forbid')


class Controls(Body):
    passes: int = Field(ge=0, le=8, strict=True)
    row: int = Field(ge=0, le=95, strict=True)
    noise: float = Field(ge=0, le=.35, allow_inf_nan=False)
    pattern: Literal['scene', 'stripes']


class Revision(Body):
    revision: int = Field(ge=1, strict=True)


class AnswerDraft(Body):
    number: str = Field(default='', max_length=80)
    choice: str = Field(default='', max_length=40)
    working: str = Field(default='', max_length=8000)


class PatchSession(Revision):
    drafts: Optional[dict[str, AnswerDraft]] = None
    stage: Optional[int] = Field(default=None, ge=0, le=4, strict=True)
    controls: Optional[Controls] = None
    prediction: Optional[str] = Field(default=None, max_length=4000)
    reflection: Optional[str] = Field(default=None, max_length=8000)
    bridge: Optional[Literal['pixels', 'convolution', 'euler', 'frequency', 'recovery']] = None


class Check(Revision):
    question_id: str = Field(min_length=1, max_length=80)
    request_id: str = Field(min_length=8, max_length=80)
    number: str = Field(min_length=1, max_length=80)
    choice: str = Field(min_length=1, max_length=40)
    working: str = Field(default='', max_length=8000)


class Reveal(Revision):
    question_id: str = Field(min_length=1, max_length=80)
    kind: Literal['hint', 'solution']


class Retry(Revision):
    question_id: str = Field(min_length=1, max_length=80)


def create_router(user, required, fail, lock, current, teaching_language, event):
    router = APIRouter(prefix='/learning/images')

    def course_guard(u):
        c = current(u)
        if catalog.code(c) != 'ELEC270':
            fail(409, '这个应用单元属于 ELEC270，请先切换课程。 / This application unit belongs to ELEC270; switch courses first.')
        return c

    def get_session(u, conn, revision=None):
        course_guard(u)
        s = required('image-session', u['id'], lesson.UNIT_ID, conn)
        if s['content_version'] != lesson.VERSION:
            fail(409, '教学内容版本已改变；已保存记录保留，请联系课程所有者。 / Lesson content has changed; saved evidence is preserved. Contact the course owner.')
        if revision is not None and s['revision'] != revision:
            fail(409, '另一页面已更新进度，请重新载入。 / Progress changed in another tab; reload the saved version.')
        return s

    def present(u, s, conn):
        return lesson.present(s, store.listing('image-check', u['id'], conn), teaching_language(u['id'], conn))

    def save(u, s, conn):
        previous_revision = s['revision']
        s.update(revision=previous_revision + 1, at=store.now())
        # Database compare-and-swap protects against another server process too.
        written = conn.execute(update(store.records).where(
            store.records.c.kind == 'image-session', store.records.c.owner == u['id'],
            store.records.c.id == lesson.UNIT_ID,
            store.records.c.body['revision'].as_integer() == previous_revision).values(body=s))
        if written.rowcount != 1:
            fail(409, '另一页面已更新进度，请重新载入。 / Progress changed in another tab; reload the saved version.')

    def find_question(s, question_id):
        found = next((q for q in s['questions'] if q['id'] == question_id), None)
        if found is None:
            fail(409, '题目已变化或不属于当前学习记录，请重新载入。 / This question has changed or is not in your session; reload.')
        return found

    @router.get('')
    def get(u=Depends(user)):
        course_guard(u)
        with store.engine.connect() as conn:
            s = store.fetch('image-session', u['id'], lesson.UNIT_ID, conn)
            return {'session': present(u, get_session(u, conn), conn) if s else None,
                    'language': teaching_language(u['id'], conn)}

    @router.post('/start')
    def start(u=Depends(user)):
        c = course_guard(u)
        with lock, store.engine.begin() as conn:
            s = store.fetch('image-session', u['id'], lesson.UNIT_ID, conn)
            if s is None:
                s = lesson.new_session(c['id'])
                store.save('image-session', u['id'], s, conn)
                event(u['id'], 'image_unit_started', conn, course_version=c['id'], content_version=lesson.VERSION)
            else:
                s = get_session(u, conn)
            return present(u, s, conn)

    @router.patch('/session')
    def patch(body: PatchSession, u=Depends(user)):
        with lock, store.engine.begin() as conn:
            s = get_session(u, conn, body.revision)
            values = body.model_dump(exclude={'revision', 'bridge', 'drafts'}, exclude_none=True)
            if body.drafts is not None:
                for question_id, draft in body.drafts.items():
                    state = find_question(s, question_id)
                    if draft.choice and draft.choice not in lesson.question(state['kind'], state['variant'])['choices']:
                        fail(422, '草稿理由不属于当前题目。 / Draft choice is not valid for this question.')
                    s['drafts'][question_id] = draft.model_dump()
            s.update(values)
            if body.bridge and body.bridge not in s['opened_bridges']:
                s['opened_bridges'].append(body.bridge)
                event(u['id'], 'image_bridge_opened', conn, bridge=body.bridge,
                      course_version=s['course_version'], content_version=s['content_version'])
            save(u, s, conn)
            return present(u, s, conn)

    @router.post('/check')
    def check(body: Check, u=Depends(user)):
        signature = hashlib.sha256(body.model_dump_json().encode()).hexdigest()
        with lock, store.engine.begin() as conn:
            s = get_session(u, conn)
            previous = store.fetch('image-check', u['id'], body.request_id, conn)
            if previous:
                if previous['signature'] != signature:
                    fail(409, '请求编号已用于另一份作答。 / Request ID already used for a different submission.')
                return present(u, s, conn)
            if s['revision'] != body.revision:
                fail(409, '另一页面已更新进度，请重新载入。 / Progress changed in another tab; reload the saved version.')
            state = find_question(s, body.question_id)
            if state['result'] is not None:
                fail(409, '本题已检查，请查看反馈或换一道题。 / This question was checked; review feedback or try another question.')
            q = lesson.question(state['kind'], state['variant'])
            supported = state['kind'] in s['supported_kinds'] or bool(state['help_exposed'])
            try:
                result = lesson.assess(q, body.number, body.choice, supported)
            except (ValueError, TypeError, OverflowError):
                fail(422, '请输入有效数值或简单算式，并选择一个理由。 / Enter a valid number or simple arithmetic and select one reason.')
            record = {'id': body.request_id, 'signature': signature, 'question_id': state['id'],
                      'kind': state['kind'], 'variant': state['variant'], 'at': store.now(),
                      'course_code': 'ELEC270', 'course_version': s['course_version'],
                      'content_version': s['content_version'], 'translation_version': lesson.TRANSLATION_VERSION,
                      'language': teaching_language(u['id'], conn), 'number': body.number,
                      'choice': body.choice, 'working': body.working, 'result': result,
                      'exposure_before': list(state['help_exposed']), 'family_support_before': supported,
                      'origin': 'synthetic' if u.get('synthetic') else 'learner-submitted'}
            store.save('image-check', u['id'], record, conn)
            state['result'] = result
            s['drafts'][state['id']] = {'number': body.number, 'choice': body.choice, 'working': body.working}
            # Feedback is support on a later same-family variant; such variants are
            # useful practice, but do not become a claim of wholly independent transfer.
            if state['kind'] not in s['supported_kinds']:
                s['supported_kinds'].append(state['kind'])
            save(u, s, conn)
            event(u['id'], 'image_checked', conn, question_id=state['id'],
                  course_version=s['course_version'], content_version=s['content_version'],
                  passed=result['passed'], evidence='bounded-image-check')
            return present(u, s, conn)

    @router.post('/reveal')
    def reveal(body: Reveal, u=Depends(user)):
        with lock, store.engine.begin() as conn:
            s = get_session(u, conn, body.revision)
            state = find_question(s, body.question_id)
            if body.kind not in state['help_exposed']:
                state['help_exposed'].append(body.kind)
                if state['kind'] not in s['supported_kinds']:
                    s['supported_kinds'].append(state['kind'])
                event(u['id'], 'image_help_revealed', conn, question_id=state['id'],
                      help_kind=body.kind, course_version=s['course_version'], content_version=s['content_version'])
                save(u, s, conn)
            return present(u, s, conn)

    @router.post('/retry')
    def retry(body: Retry, u=Depends(user)):
        with lock, store.engine.begin() as conn:
            s = get_session(u, conn, body.revision)
            state = find_question(s, body.question_id)
            if state['result'] is None and not state['help_exposed']:
                fail(409, '请先尝试本题或查看帮助。 / Try this question or reveal help before requesting another.')
            if state['variant'] + 1 >= lesson.MAX_VARIANTS:
                fail(409, '本类已核查的小题已用完；可以复看讲解或进入课程练习。 / No unused checks remain in this family; review the lesson or use course practice.')
            s['drafts'].pop(state['id'], None)
            s['questions'][s['questions'].index(state)] = lesson.new_question(state['kind'], state['variant'] + 1)
            save(u, s, conn)
            event(u['id'], 'image_check_retried', conn, from_question=state['id'],
                  course_version=s['course_version'], content_version=s['content_version'])
            return present(u, s, conn)

    return router
