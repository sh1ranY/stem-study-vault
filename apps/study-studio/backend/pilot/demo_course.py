"""Idempotent original demos. Never reads a vault or replaces an imported course."""
from . import store, teaching, localization, catalog


def seed():
    added = False
    with store.engine.begin() as conn:
        existing = catalog.versions(conn)
        for code, meta in catalog.COURSES.items():
            if code in existing: continue
            lessons=[]
            for key, topic in teaching.topics(code).items():
                bodies={}
                for language in ('zh-CN','en'):
                    t=localization.topic(key,language)
                    headings=('学习目标','补一点基础','图示与直觉','规则与推导','换一组例子') if language=='zh-CN' else ('Learning objective','Build foundations','Visual intuition','Rules and reasoning','Worked example')
                    bodies[language]='# '+t['title']+'\n\n'+'\n\n'.join('## '+h+'\n\n'+v for h,v in zip(headings,(t['objective'],t['routes']['bridge'],t['routes']['visual'],t['routes']['algebra'],t['example'])))
                lessons.append({'id':code.lower()+'-authored-'+key,'week':topic['week'],'title':topic['title'],'title_en':localization.topic(key,'en')['title'],'source_hash':'authored-demo-v2','blocks':[{'id':code.lower()+'-core-'+key,'role':'lesson','body':bodies['zh-CN'],'body_en':bodies['en']}]})
            course={'id':code.lower()+'-authored-demo-v2','code':code,'mode':'demo','title':code+' · '+meta['title'],'imported_at':store.now(),'lessons':lessons,'assets':[],'warnings':['原创演示：每课三个入门主题；不含大学原始课件，也不代表全课程考核。 / Original demo: three starter topics per course; no university materials or full-course assessment.'],'legacy_records':[]}
            catalog.register(course,conn);added=True
    return added

if __name__=='__main__':
    print('Missing demo courses added.' if seed() else 'All existing courses preserved.')
