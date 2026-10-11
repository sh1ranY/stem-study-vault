"""Distributable authored course only; never copies private vaults into a hosted service."""
from . import store, teaching


def seed():
    if store.fetch('config','shared','current-course'): return False
    course={'id':'elec270-authored-pilot-v1','title':'ELEC270 · Authored pilot / 自编试点',
      'imported_at':store.now(),'lessons':[
        {'id':'authored-'+k,'week':v['week'],'title':v['title'],'source_hash':'authored-pilot-v1',
         'blocks':[{'id':'authored-core-'+k,'role':'lesson','body':'# '+v['title']+'\n\n'+v['objective']+'\n\n'+v['routes']['algebra']+'\n\n'+v['example']}]} for k,v in teaching.TOPICS.items()],
      'assets':[],'warnings':['自编试点内容，不含大学原始课件。 / Authored pilot; university source material is not included.'],'legacy_records':[]}
    with store.engine.begin() as conn:
        store.save('course','shared',course,conn);store.save('config','shared',{'id':'current-course','version':course['id']},conn)
    return True

if __name__=='__main__': print('Authored pilot seeded.' if seed() else 'Existing course preserved.')
