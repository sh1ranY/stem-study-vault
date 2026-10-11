"""Portable transactional storage. SQLite is the local default; PostgreSQL uses the same schema."""
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, String, JSON, select, insert, update, delete

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / '.env')
DATA = Path(os.getenv('STUDIO_DATA_DIR', str(ROOT / 'data')))
DATA.mkdir(parents=True, exist_ok=True)
URL = os.getenv('STUDIO_DATABASE_URL', 'sqlite:///' + str(DATA / 'pilot.sqlite3'))
engine = create_engine(URL, connect_args={'check_same_thread': False, 'timeout': 20} if URL.startswith('sqlite') else {}, pool_pre_ping=True)
meta = MetaData()
records = Table('pilot_records', meta,
    Column('kind', String(40), primary_key=True), Column('owner', String(64), primary_key=True),
    Column('id', String(160), primary_key=True), Column('body', JSON, nullable=False))
meta.create_all(engine)

def now(): return datetime.now(timezone.utc).isoformat()
def uid(): return uuid.uuid4().hex

def fetch(kind, owner, key, conn=None):
    if conn is None:
        with engine.connect() as c: return fetch(kind, owner, key, c)
    return conn.execute(select(records.c.body).where(records.c.kind == kind, records.c.owner == owner, records.c.id == key)).scalar_one_or_none()

def listing(kind, owner, conn=None):
    if conn is None:
        with engine.connect() as c: return listing(kind, owner, c)
    return list(conn.execute(select(records.c.body).where(records.c.kind == kind, records.c.owner == owner)).scalars())

def save(kind, owner, value, conn=None):
    if conn is None:
        with engine.begin() as c: return save(kind, owner, value, c)
    condition = (records.c.kind == kind, records.c.owner == owner, records.c.id == value['id'])
    if fetch(kind, owner, value['id'], conn) is None:
        conn.execute(insert(records).values(kind=kind, owner=owner, id=value['id'], body=value))
    else:
        conn.execute(update(records).where(*condition).values(body=value))
    return value

def remove(kind, owner, key, conn=None):
    if conn is None:
        with engine.begin() as c: return remove(kind, owner, key, c)
    conn.execute(delete(records).where(records.c.kind == kind, records.c.owner == owner, records.c.id == key))
