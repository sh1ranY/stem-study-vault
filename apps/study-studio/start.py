#!/usr/bin/env python3
"""Cross-platform local launcher; demo storage and model configuration are isolated."""
import argparse
import hashlib
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
import webbrowser

ROOT = Path(__file__).resolve().parent


def environment(demo):
    env = os.environ.copy()
    if demo:
        data = ROOT / 'data-demo'
        env.update(STUDIO_DATA_DIR=str(data), STUDIO_DATABASE_URL='sqlite:///' + str(data / 'pilot.sqlite3'),
                   STUDIO_DEPLOYMENT='local', STUDIO_COOKIE_SECURE='0', STUDIO_DEMO='1',
                   OPENAI_API_KEY='', DEEPSEEK_API_KEY='', STUDIO_MODEL='', STUDIO_VISION_MODEL='', STUDIO_PROVIDER='')
    return env


def main():
    parser = argparse.ArgumentParser(description='Start Study Studio locally. --demo uses separate data and disables AI calls.')
    parser.add_argument('--demo', action='store_true', help='Original three-course demo on port 5177; no private files or model calls')
    parser.add_argument('--prepare-only', action='store_true', help='Install, migrate, seed missing demos and build; do not start a server')
    parser.add_argument('--no-browser', action='store_true', help='Do not open a browser automatically')
    args = parser.parse_args()
    if sys.version_info < (3, 9):
        raise SystemExit('Python 3.9+ is required; Python 3.12 is recommended. / 请先安装 Python。')
    npm = shutil.which('npm')
    node = shutil.which('node')
    if not npm or not node:
        raise SystemExit('Install Node.js 22.12+ (includes npm), then run again. / 请先安装 Node.js。')
    version = tuple(int(x) for x in subprocess.check_output([node, '--version'], text=True).strip().lstrip('v').split('.'))
    if version < (20, 19, 0) or (version[0] == 22 and version < (22, 12, 0)) or version[0] == 21:
        raise SystemExit('Node.js 20.19+ or 22.12+ is required.')
    port = 5177 if args.demo else 8765
    if not args.prepare_only:
        with socket.socket() as probe:
            if probe.connect_ex(('127.0.0.1', port)) == 0:
                raise SystemExit(f'Port {port} is already in use. Stop its server before starting this version. / 请先关闭该端口正在运行的服务。')
    env = environment(args.demo)
    python = ROOT / '.venv' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    def run(*command):
        subprocess.run([str(x) for x in command], cwd=ROOT, env=env, check=True)
    if not python.exists(): run(sys.executable, '-m', 'venv', ROOT / '.venv')
    for inputs, stamp, command in [
        (['requirements.txt'], ROOT / '.venv/.studio-deps', [python, '-m', 'pip', 'install', '-r', 'requirements.txt']),
        (['package.json', 'package-lock.json'], ROOT / 'node_modules/.studio-deps', [npm, 'ci']),
    ]:
        digest = hashlib.sha256(b''.join((ROOT / f).read_bytes() for f in inputs)).hexdigest()
        if not stamp.exists() or stamp.read_text() != digest:
            run(*command)
            stamp.parent.mkdir(parents=True, exist_ok=True)
            stamp.write_text(digest)
    run(python, '-m', 'alembic', 'upgrade', 'head')
    run(python, '-m', 'backend.pilot.demo_course')
    run(npm, 'run', 'build')
    if args.prepare_only:
        print('Ready. / 安装与构建完成。')
        return
    url = f'http://127.0.0.1:{port}'
    process = subprocess.Popen([str(python), '-m', 'uvicorn', 'backend.app:app', '--host', '127.0.0.1', '--port', str(port)], cwd=ROOT, env=env)
    try:
        for _ in range(100):
            if process.poll() is not None: raise RuntimeError('The server could not start. See the message above.')
            try:
                with urllib.request.urlopen(url + '/api/health', timeout=1) as response:
                    if response.status == 200: break
            except OSError: time.sleep(0.2)
        else: raise RuntimeError('The server did not become ready.')
        print(('Original demo (AI disabled)' if args.demo else 'Local learning space') + ': ' + url, flush=True)
        print('Keep this window open. Press Ctrl+C to stop. / 保持此窗口打开，Ctrl+C停止。', flush=True)
        if not args.no_browser: webbrowser.open(url)
        process.wait()
    except KeyboardInterrupt:
        pass
    finally:
        if process.poll() is None:
            process.terminate()
            try: process.wait(timeout=10)
            except subprocess.TimeoutExpired: process.kill(); process.wait()


if __name__ == '__main__':
    try: main()
    except (subprocess.CalledProcessError, RuntimeError) as exc:
        raise SystemExit(str(exc))
