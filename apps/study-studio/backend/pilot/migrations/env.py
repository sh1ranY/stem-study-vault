from alembic import context
from sqlalchemy import create_engine, pool
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[3]/'.env')
url=os.getenv('STUDIO_DATABASE_URL','sqlite:///'+str(Path(os.getenv('STUDIO_DATA_DIR','data'))/'pilot.sqlite3'))
if context.is_offline_mode():
    context.configure(url=url,literal_binds=True)
    with context.begin_transaction(): context.run_migrations()
else:
    with create_engine(url,poolclass=pool.NullPool).connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction(): context.run_migrations()
