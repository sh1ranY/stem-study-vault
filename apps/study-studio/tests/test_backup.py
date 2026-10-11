import json
import sqlite3
import tempfile
import unittest
import zipfile
from pathlib import Path
from backend.backup import snapshot,restore

class BackupTests(unittest.TestCase):
    def test_roundtrip_files_paths_and_login_revocation(self):
        with tempfile.TemporaryDirectory() as root:
            root=Path(root);data=root/'live';photo=data/'photos'/'owner'/'a.jpg';photo.parent.mkdir(parents=True);photo.write_bytes(b'synthetic-photo')
            with sqlite3.connect(data/'pilot.sqlite3') as db:
                db.execute('CREATE TABLE pilot_records (kind TEXT,owner TEXT,id TEXT,body TEXT)')
                db.execute('INSERT INTO pilot_records VALUES (?,?,?,?)',('photo','owner','a',json.dumps({'id':'a','path':str(photo)})))
                db.execute('INSERT INTO pilot_records VALUES (?,?,?,?)',('login','auth','token',json.dumps({'id':'token'})))
            archive=root/'backup.zip';self.assertEqual(snapshot(data,archive),2)
            destination=restore(archive,root/'restored')
            with sqlite3.connect(destination/'pilot.sqlite3') as db:
                self.assertEqual(db.execute("SELECT count(*) FROM pilot_records WHERE kind='login'").fetchone()[0],0)
                stored=json.loads(db.execute("SELECT body FROM pilot_records WHERE kind='photo'").fetchone()[0]);self.assertEqual(Path(stored['path']).read_bytes(),b'synthetic-photo')
            self.assertEqual(photo.read_bytes(),b'synthetic-photo')
            with self.assertRaises(ValueError):restore(archive,data)
            with self.assertRaises(ValueError):snapshot(data,data/'backup.zip')

    def test_checksum_and_traversal_rejected_without_partial_destination(self):
        with tempfile.TemporaryDirectory() as root:
            root=Path(root)
            for name,files in [('checksum',{'pilot.sqlite3':'invalid'}),('traversal',{'pilot.sqlite3':'invalid','../escape':'invalid'})]:
                archive=root/(name+'.zip');out=root/name
                with zipfile.ZipFile(archive,'w') as z:
                    z.writestr('manifest.json',json.dumps({'version':1,'data_root':'/old','files':files}));z.writestr('pilot.sqlite3',b'corrupt')
                with self.assertRaises(ValueError):restore(archive,out)
                self.assertFalse(out.exists())
