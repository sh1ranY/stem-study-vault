"""Offline SQLite backup/restore. Archives contain private records: keep them outside Git."""
import argparse
import hashlib
import json
import os
import sqlite3
import tempfile
import zipfile
from pathlib import Path, PurePosixPath


def snapshot(data, destination):
    data=Path(data).resolve();destination=Path(destination).resolve()
    if data in destination.parents: raise ValueError('Save backups outside the live data directory')
    if not (data/'pilot.sqlite3').is_file(): raise ValueError('No local pilot database found')
    with tempfile.TemporaryDirectory() as temporary:
        temp=Path(temporary);files={}
        for name in ('pilot.sqlite3','studio.sqlite3'):
            if not (data/name).exists(): continue
            with sqlite3.connect((data/name).as_uri()+'?mode=ro',uri=True) as source,sqlite3.connect(temp/name) as target:
                source.backup(target)
                if target.execute('PRAGMA integrity_check').fetchone()[0]!='ok': raise ValueError('Database integrity check failed')
            files[name]=temp/name
        for path in data.rglob('*'):
            if path.is_symlink(): raise ValueError('Symlinks are not supported in a backup')
            if not path.is_file() or path.name.endswith(('.sqlite3','.sqlite3-wal','.sqlite3-shm')): continue
            if path.parts[len(data.parts)] in ('photos','course-assets') or (path.parent==data and len(path.stem)==32 and all(c in '0123456789abcdef' for c in path.stem)):
                files[path.relative_to(data).as_posix()]=path
        # Snapshot references must exist. Concurrent deletion makes the backup fail rather than silently lose images.
        with sqlite3.connect(temp/'pilot.sqlite3') as db:
            for (body,) in db.execute('SELECT body FROM pilot_records'):
                def verify(value):
                    if isinstance(value,dict):
                        for key,item in value.items():
                            if key in ('path','original_path') and isinstance(item,str):
                                p=Path(item)
                                if data in p.parents and p.relative_to(data).as_posix() not in files: raise ValueError('Referenced file missing; retry backup during a quiet period')
                            else: verify(item)
                    elif isinstance(value,list):
                        for item in value:verify(item)
                verify(json.loads(body))
        with destination.open('xb') as output:
            os.chmod(destination,0o600)
            try:
                with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as archive:
                    hashes={}
                    for name,path in files.items():
                        content=path.read_bytes();hashes[name]=hashlib.sha256(content).hexdigest();archive.writestr(name,content)
                    archive.writestr('manifest.json',json.dumps({'version':1,'data_root':str(data),'files':hashes}))
            except Exception:
                destination.unlink(missing_ok=True);raise
    return len(files)


def restore(archive_path,destination):
    destination=Path(destination).resolve()
    if destination.exists(): raise ValueError('Restore requires a new directory; live data is never overwritten')
    destination.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent) as temporary,zipfile.ZipFile(archive_path) as archive:
        temp=Path(temporary);manifest=json.loads(archive.read('manifest.json'))
        if manifest.get('version')!=1 or 'pilot.sqlite3' not in manifest.get('files',{}): raise ValueError('Invalid backup manifest')
        old_root=Path(manifest['data_root'])
        for name,digest in manifest['files'].items():
            p=PurePosixPath(name)
            if p.is_absolute() or '..' in p.parts or '\\' in name: raise ValueError('Unsafe archive path')
            content=archive.read(name)
            if hashlib.sha256(content).hexdigest()!=digest: raise ValueError('Backup checksum mismatch')
            path=temp/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(content)
        with sqlite3.connect(temp/'pilot.sqlite3') as db:
            if db.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('Invalid database')
            def relocate(value):
                if isinstance(value,dict):
                    for key,item in value.items():
                        if key in ('path','original_path') and isinstance(item,str) and old_root in Path(item).parents:
                            value[key]=str(destination/Path(item).relative_to(old_root))
                        else:relocate(item)
                elif isinstance(value,list):
                    for item in value:relocate(item)
            for kind,owner,key,body in db.execute('SELECT kind,owner,id,body FROM pilot_records').fetchall():
                value=json.loads(body);relocate(value);db.execute('UPDATE pilot_records SET body=? WHERE kind=? AND owner=? AND id=?',(json.dumps(value,ensure_ascii=False),kind,owner,key))
            # Restored credentials remain, but invalidate browser sessions after recovery.
            db.execute("DELETE FROM pilot_records WHERE kind='login'")
        temp.rename(destination)
        os.chmod(destination,0o700)
    return destination

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='action',required=True)
    save=sub.add_parser('create');save.add_argument('--data',required=True);save.add_argument('--output',required=True)
    load=sub.add_parser('restore');load.add_argument('--archive',required=True);load.add_argument('--destination',required=True)
    args=parser.parse_args()
    if args.action=='create':print('Private backup created; files:',snapshot(args.data,args.output))
    else:restore(args.archive,args.destination);print('Restored to a new directory; sign in again after switching the service to it.')
