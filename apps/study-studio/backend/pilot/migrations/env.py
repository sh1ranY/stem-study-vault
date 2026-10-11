from alembic import context
from sqlalchemy import create_engine, pool
from sqlalchemy.engine import make_url
import os
from pathlib import Path
from dotenv import load_dotenv
root=Path(__file__).resolve().parents[3]
load_dotenv(root/'.env')
url=os.getenv('STUDIO_DATABASE_URL','sqlite:///'+str(Path(os.getenv('STUDIO_DATA_DIR',str(root/'data')))/'pilot.sqlite3'))
parsed=make_url(url)
if parsed.get_backend_name()=='sqlite' and parsed.database and parsed.database!=':memory:':
    Path(parsed.database).parent.mkdir(parents=True,exist_ok=True)
if context.is_offline_mode():
    context.configure(url=url,literal_binds=True)
    with context.begin_transaction(): context.run_migrations()
else:
    with create_engine(url,poolclass=pool.NullPool).connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction(): context.run_migrations()
