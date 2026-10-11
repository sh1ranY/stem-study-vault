"""Initialize the mounted volume, then drop privileges before starting the application."""
import os
import runpy
from pathlib import Path

if __name__=='__main__':
    root=Path(os.environ.get('STUDIO_DATA_DIR','/var/data/study-studio')).resolve()
    if Path('/var/data') not in root.parents: raise ValueError('Container data must be a directory under /var/data')
    root.mkdir(parents=True,exist_ok=True)
    if os.getuid()==0:
        os.chown(root,10001,10001);os.setgroups([]);os.setgid(10001);os.setuid(10001)
    runpy.run_module('backend.serve',run_name='__main__')
