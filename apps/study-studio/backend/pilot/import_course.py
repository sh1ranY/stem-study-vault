"""Read-only ELEC270 importer; content-addressed copies, provenance and gated callouts."""
import argparse
import os
import hashlib
import json
import re
import shutil
from pathlib import Path
from . import store

DEFAULT_VAULT = Path(os.getenv('STUDIO_VAULT_ROOT', str(Path.home() / 'Documents' / 'Obsidian')))
COURSE = Path('10 Y2上学期/ELEC270 信号与系统')
DEFAULT_DESKTOP = Path(os.getenv('STUDIO_ELEC270_SOURCES', str(Path.home() / 'Desktop' / 'ELEC270 课程资料')))
ALLOWED = {'.pdf', '.pptx', '.png', '.jpg', '.jpeg', '.webp', '.svg'}

def digest(data): return hashlib.sha256(data).hexdigest()
def stable(text): return digest(text.encode())[:24]
def slug(text): return re.sub(r'[^\w\-\u4e00-\u9fff]+', '-', text).strip('-')

def strip_front(text): return re.sub(r'\A---\n.*?\n---\n', '', text, flags=re.S)

class Importer:
    def __init__(self, vault, desktop):
        self.vault, self.desktop = Path(vault).resolve(), Path(desktop).resolve()
        self.root = self.vault / COURSE
        self.assets, self.warnings, self.lessons = {}, [], []
        self.by_path = {}
        self.files = list(self.root.rglob('*'))
        self.md_ids = {p.resolve(): 'elec270-' + stable(str(p.relative_to(self.root))) for p in self.root.glob('Weeks/*.md')}

    def asset(self, path):
        path = path.resolve()
        if not (path.is_relative_to(self.root) or path.is_relative_to(self.desktop)) or path.suffix.lower() not in ALLOWED or not path.is_file():
            self.warnings.append('不可读取附件：' + str(path)); return None
        if path in self.by_path: return self.by_path[path]
        data = path.read_bytes(); key = digest(data)
        if key not in self.assets:
            dest = store.DATA / 'course-assets' / (key + path.suffix.lower())
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists(): dest.write_bytes(data)
            self.assets[key] = {'id': key, 'name': path.name, 'sha256': key, 'suffix': path.suffix.lower(), 'bytes': len(data), 'locations': [], 'path': str(dest), 'format_group': re.sub(r'[^a-z0-9]+', '', path.stem.lower()), 'role': 'historical' if any(w in str(path) for w in ('往年','历史','Exams')) else 'course-source'}
        self.assets[key]['locations'].append(str(path)); self.by_path[path] = key
        return key

    def resolve(self, target, current):
        target = target.replace('\\|', '|').split('|')[0]
        name, _, fragment = target.partition('#')
        if not name: return current, fragment
        candidates = [self.vault/name, current.parent/name, self.root/name]
        for p in candidates:
            for q in (p, p.with_suffix('.md')):
                if q.is_file() and q.resolve().is_relative_to(self.root): return q.resolve(), fragment
        matches = [p for p in self.files if p.is_file() and (p.name == name or p.stem == name)]
        if len(matches) == 1: return matches[0].resolve(), fragment
        self.warnings.append(f'链接待核对：{current.name} → {target}')
        return None, fragment

    def convert(self, text, current, chain=()):
        def link(m):
            embedded = bool(m[1]); raw = m[2].replace('\\|','|'); target, _, alias = raw.partition('|')
            path, fragment = self.resolve(target, current)
            label = alias or target.split('/')[-1]
            if path is None: return f'〔待核对链接：{label}〕'
            if path.suffix.lower() in ALLOWED:
                key = self.asset(path)
                if not key: return f'〔附件待核对：{label}〕'
                # Private source files remain local; browser URLs are authenticated.
                url = '/api/pilot/assets/' + key
                if embedded and path.suffix.lower() in {'.png','.jpg','.jpeg','.webp','.svg'}:
                    return f'![{path.stem}]({url})'
                return f'[{label}]({url}' + (f'#page={fragment.split("=")[-1]}' if fragment.startswith('page=') else '') + ')'
            if path.suffix.lower() == '.md' and embedded:
                marker = (str(path), fragment)
                if marker in chain or len(chain) >= 8:
                    self.warnings.append('循环嵌入：'+str(marker)); return '〔循环嵌入未展开〕'
                body = strip_front(path.read_text())
                if fragment.startswith('^'):
                    blocks = re.split(r'\n\s*\n', body); body = next((b for b in blocks if fragment in b), '')
                elif fragment:
                    lines = body.splitlines(); start = next((i for i,l in enumerate(lines) if l.lstrip('# ').strip() == fragment), None)
                    if start is not None:
                        level = len(lines[start])-len(lines[start].lstrip('#')); end = next((i for i in range(start+1,len(lines)) if re.match(r'^#{1,'+str(level)+r'} ',lines[i])),len(lines)); body='\n'.join(lines[start:end])
                    else: body=''
                if not body: self.warnings.append('嵌入位置缺失：'+target); return f'〔待核对嵌入：{label}〕'
                return self.convert(body,path,chain+(marker,))
            if path in self.md_ids:
                return f'[{label}](?lesson={self.md_ids[path]}' + ('#'+slug(fragment) if fragment else '') + ')'
            # Do not expose personal/maintenance Markdown through a raw file route.
            return f'{label}〔原库参考〕'
        return re.sub(r'(!?)\[\[([^\]]+)\]\]', link, text)

    def blocks(self, text, lesson_id):
        # All top-level Obsidian callouts with answer-like roles are removed before publication/search.
        lines=text.splitlines(); blocks=[]; plain=[]; i=0
        def flush():
            if plain:
                body='\n'.join(plain).strip()
                if body: blocks.append({'id':lesson_id+'-b'+str(len(blocks)), 'role':'lesson', 'body':body})
                plain.clear()
        while i<len(lines):
            m=re.match(r'^>\s*\[!([^\]]+)\][+-]?\s*(.*)',lines[i])
            if not m: plain.append(lines[i]); i+=1; continue
            flush(); chunk=[]; label=m[2] or m[1]; kind=m[1].lower(); i+=1
            while i<len(lines) and (lines[i].startswith('>') or (not lines[i].strip() and i+1<len(lines) and lines[i+1].startswith('>'))):
                if re.match(r'^>\s*\[!',lines[i]): break
                chunk.append(re.sub(r'^> ?', '', lines[i])); i+=1
            role='hint' if kind=='hint' else ('solution' if kind in ('success','answer','solution') or re.search('解答|答案|解析',label) else 'lesson')
            blocks.append({'id':lesson_id+'-b'+str(len(blocks)), 'role':role,'title':label,'body':'\n'.join(chunk).strip()})
        flush(); return blocks

    def run(self):
        if not self.md_ids: raise ValueError('没有找到 ELEC270 Weeks 讲义，保留现有课程版本。')
        for path in sorted(self.md_ids):
            raw=path.read_bytes(); text=self.convert(strip_front(raw.decode()),path)
            key=self.md_ids[path]; title=next((l[2:] for l in text.splitlines() if l.startswith('# ')),path.stem)
            week=int(re.search(r'Week\s*(\d+)',path.name)[1])
            self.lessons.append({'id':key,'title':title,'week':week,'source_path':str(path),'source_hash':digest(raw),'blocks':self.blocks(text,key)})
        # Register both original roots; deduplication is by bytes, format relations by base name only (candidate).
        for root in (self.root/'Sources', self.desktop):
            for path in sorted(root.rglob('*')):
                if path.is_file() and path.suffix.lower() in {'.pdf','.pptx'}: self.asset(path)
        records=[]
        for path in sorted((self.root/'Practice').glob('*错题*.md')):
            text=path.read_text(); records.append({'id':stable(str(path)), 'title':path.stem, 'body':self.convert(strip_front(text),path),'source_hash':digest(path.read_bytes()),'note':'原库参考，未自动解释为已掌握或真实作答。'})
        fingerprint = digest(json.dumps({'lessons':self.lessons,'assets':sorted(self.assets),'records':records},ensure_ascii=False,sort_keys=True).encode())
        version='elec270-'+fingerprint[:16]
        course={'id':version,'title':'ELEC270 · 信号与系统','imported_at':store.now(),'lessons':self.lessons,'assets':list(self.assets.values()),'legacy_records':records,'warnings':sorted(set(self.warnings)),'content_hash':fingerprint,'schema_version':1}
        with store.engine.begin() as conn:
            if store.fetch('course','shared',version,conn) is None: store.save('course','shared',course,conn)
            store.save('config','shared',{'id':'current-course','version':version},conn)
        return {'version':version,'lessons':len(self.lessons),'assets':len(self.assets),'locations':sum(len(a['locations']) for a in self.assets.values()),'hidden_blocks':sum(b['role']!='lesson' for l in self.lessons for b in l['blocks']),'legacy_records':len(records),'warnings':course['warnings']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--vault',type=Path,default=DEFAULT_VAULT);p.add_argument('--desktop',type=Path,default=DEFAULT_DESKTOP);a=p.parse_args()
    print(json.dumps(Importer(a.vault,a.desktop).run(),ensure_ascii=False,indent=2))
