"""Initial portable pilot schema. JSON payloads carry versioned domain objects."""
from alembic import op
import sqlalchemy as sa
revision='0001_pilot'
down_revision=None
branch_labels=None
depends_on=None

def upgrade():
    if not sa.inspect(op.get_bind()).has_table('pilot_records'):
        op.create_table('pilot_records',sa.Column('kind',sa.String(40),primary_key=True),sa.Column('owner',sa.String(64),primary_key=True),sa.Column('id',sa.String(160),primary_key=True),sa.Column('body',sa.JSON(),nullable=False))

def downgrade():
    raise RuntimeError('This migration retains learner evidence; use an explicit backup/restore operation instead of dropping it.')
