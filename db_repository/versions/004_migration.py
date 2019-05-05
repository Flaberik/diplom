from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
schedule = Table('schedule', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('group_id', Integer),
    Column('lesson_id', Integer),
    Column('teacher_id', Integer),
    Column('day_week', String(length=2)),
    Column('pair', String(length=1)),
    Column('num_room', String(length=4)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['schedule'].columns['day_week'].create()
    post_meta.tables['schedule'].columns['num_room'].create()
    post_meta.tables['schedule'].columns['pair'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['schedule'].columns['day_week'].drop()
    post_meta.tables['schedule'].columns['num_room'].drop()
    post_meta.tables['schedule'].columns['pair'].drop()
