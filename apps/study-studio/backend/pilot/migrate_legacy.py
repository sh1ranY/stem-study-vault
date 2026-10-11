"""Archive legacy Studio evidence as unverified provenance, never infer learner mastery."""
import json
import sqlite3
from . import store

def import_legacy(owner, db_path=None):
    path=db_path or store.DATA/'studio.sqlite3'
    if not path.exists(): return 0
    with sqlite3.connect('file:'+str(path)+'?mode=ro',uri=True) as connection:
        rows=connection.execute("SELECT id,body FROM records WHERE kind='session'").fetchall()
    with store.engine.begin() as conn:
        for key,body in rows:
            if store.fetch('legacy-session',owner,key,conn) is None:
                value=json.loads(body)
                store.save('legacy-session',owner,{'id':key,'origin':'legacy-unverified','imported_at':store.now(),'snapshot':value,'note':'旧版会话保留原始观察；可能包含演示，不参与本版能力判断。'},conn)
    return len(rows)
