from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
groups = Table('groups', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('group_name', String(length=128)),
)

lessons = Table('lessons', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('lesson_name', String(length=128)),
)

teachers = Table('teachers', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('teacher_name', String(length=128)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['groups'].create()
    post_meta.tables['lessons'].create()
    post_meta.tables['teachers'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['groups'].drop()
    post_meta.tables['lessons'].drop()
    post_meta.tables['teachers'].drop()
