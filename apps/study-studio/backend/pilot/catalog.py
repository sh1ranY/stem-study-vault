"""Course registry and per-request selection, compatible with the original single course."""
from . import store

COURSES = {
    'ELEC270': {'title': '信号与系统', 'title_en': 'Signals and Systems', 'folder': 'ELEC270 信号与系统'},
    'COMP201': {'title': '软件工程 I', 'title_en': 'Software Engineering I', 'folder': 'COMP201 软件工程 I'},
    'COMP207': {'title': '数据库开发', 'title_en': 'Database Development', 'folder': 'COMP207 数据库开发'},
}


def code(course):
    return course.get('code') or next((key for key in COURSES if course['id'].upper().startswith(key) or course.get('title','').upper().startswith(key)), 'ELEC270')


def versions(conn=None):
    entries = {r['id']: r['version'] for r in store.listing('course-entry', 'shared', conn)}
    legacy = store.fetch('config', 'shared', 'current-course', conn)
    if legacy:
        course = store.fetch('course', 'shared', legacy['version'], conn)
        if course: entries.setdefault(code(course), course['id'])
    return entries


def register(course, conn):
    course_code = code(course)
    if store.fetch('course', 'shared', course['id'], conn) is None:
        store.save('course', 'shared', course, conn)
    store.save('course-entry', 'shared', {'id': course_code, 'version': course['id']}, conn)
    legacy = store.fetch('config', 'shared', 'current-course', conn)
    previous = store.fetch('course', 'shared', legacy['version'], conn) if legacy else None
    # Keep legacy clients on their original course when another course is added.
    if previous is None or code(previous) == course_code:
        store.save('config', 'shared', {'id': 'current-course', 'version': course['id']}, conn)


def selected(user=None):
    entries = versions()
    if not entries: return None
    explicit = (user or {}).get('_course')
    preference = store.fetch('course-preference', user['id'], 'active') if user else None
    chosen = explicit or (preference or {}).get('code')
    if explicit and explicit not in entries: return None
    if chosen not in entries:
        legacy = store.fetch('config', 'shared', 'current-course')
        chosen = next((key for key, version in entries.items() if legacy and version == legacy['version']), next(iter(entries)))
    return store.fetch('course', 'shared', entries[chosen])


def summaries(language='zh-CN'):
    result = []
    for key, version in versions().items():
        course = store.fetch('course', 'shared', version)
        if not course: continue
        names = COURSES.get(key, {})
        result.append({'code': key, 'id': version, 'title': key + ' · ' + names.get('title_en' if language == 'en' else 'title', course['title']), 'mode': course.get('mode', 'imported'), 'lesson_count': len(course['lessons'])})
    return sorted(result, key=lambda c: list(COURSES).index(c['code']) if c['code'] in COURSES else 99)


def groups(owner, course):
    """Filter personal records using stable topic/lesson identities, including older imports."""
    from . import teaching
    keys = teaching.topics(code(course))
    tasks = [t for t in store.listing('task', owner) if t['topic'] in keys]
    task_ids = {t['id'] for t in tasks}
    attempts = [a for a in store.listing('attempt', owner) if a['task_id'] in task_ids]
    attempt_ids = {a['id'] for a in attempts}
    photos = [p for p in store.listing('photo', owner) if p['task_id'] in task_ids]
    photo_ids = {p['id'] for p in photos}
    lesson_ids = {l['id'] for l in course['lessons']}
    # Stable ids retain notes across course imports. Old removed lessons are retained in export too.
    snapshots = [c for c in store.listing('course', 'shared') if code(c) == code(course)]
    course_versions = {c['id'] for c in snapshots}
    asset_ids = {a['id'] for c in snapshots for a in c['assets']}
    events = [e for e in store.listing('event', owner) if e.get('asset_id') in asset_ids or e.get('topic') in keys or e.get('task_id') in task_ids or e.get('attempt_id') in attempt_ids or e.get('lesson_id') in lesson_ids or e.get('version', e.get('course_version')) in course_versions or (code(course) == 'ELEC270' and e['kind'].startswith('guided_'))]
    result = {'task': tasks, 'attempt': attempts, 'photo': photos, 'event': events,
              'progress': [p for p in store.listing('progress', owner) if p['id'] in lesson_ids or p.get('version') in course_versions],
              'answer-draft': [d for d in store.listing('answer-draft', owner) if d['id'] in task_ids],
              'feedback': [f for f in store.listing('feedback', owner) if f['attempt_id'] in attempt_ids],
              'route': [r for r in store.listing('route', owner) if r['id'] in keys],
              'run': [r for r in store.listing('run', owner) if r['reference'] in attempt_ids | photo_ids],
              'teaching-preference': store.listing('teaching-preference', owner)}
    for kind in ('guided-session', 'guided-check', 'legacy-session', 'image-session', 'image-check'):
        result[kind] = store.listing(kind, owner) if code(course) == 'ELEC270' else []
    return result
