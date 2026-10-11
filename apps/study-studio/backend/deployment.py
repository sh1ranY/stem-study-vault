"""Explicit local/hosted boundary. A hosted process must fail closed on missing settings."""
import os
from dataclasses import dataclass
from urllib.parse import urlsplit

@dataclass(frozen=True)
class Deployment:
    hosted: bool
    origin: str
    hosts: tuple
    origins: tuple


def settings(env=None):
    env=os.environ if env is None else env
    mode=env.get('STUDIO_DEPLOYMENT','local')
    if mode not in ('local','hosted'): raise ValueError('STUDIO_DEPLOYMENT must be local or hosted')
    if mode=='local':
        return Deployment(False,'http://127.0.0.1:8765',('localhost','127.0.0.1','testserver'),('http://127.0.0.1:8765','http://localhost:8765','http://127.0.0.1:5177','http://localhost:5177','http://testserver'))
    origin=env.get('STUDIO_PUBLIC_ORIGIN') or env.get('RENDER_EXTERNAL_URL','')
    parsed=urlsplit(origin)
    if parsed.scheme!='https' or not parsed.hostname or parsed.username or parsed.password or parsed.path not in ('','/') or parsed.query or parsed.fragment or parsed.port not in (None,443):
        raise ValueError('Hosted mode requires one exact HTTPS origin in STUDIO_PUBLIC_ORIGIN or RENDER_EXTERNAL_URL')
    if len(env.get('STUDIO_BOOTSTRAP_TOKEN',''))<32:
        raise ValueError('Hosted mode requires STUDIO_BOOTSTRAP_TOKEN of at least 32 characters')
    if not env.get('STUDIO_DATA_DIR','').startswith('/'):
        raise ValueError('Hosted mode requires an absolute persistent STUDIO_DATA_DIR')
    # No wildcard hosts/origins. Health probes may address the loopback host.
    return Deployment(True,'https://'+parsed.netloc,(parsed.hostname,'localhost','127.0.0.1'),('https://'+parsed.netloc,))
