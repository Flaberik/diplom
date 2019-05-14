from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
load = Table('load', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('group_id', Integer),
    Column('lesson_id', Integer),
    Column('teacher_id', Integer),
    Column('weeks', Integer),
    Column('academic_hours_week', Float),
    Column('academic_hours_term', Float),
    Column('courseworks', Integer),
    Column('lab_works', Integer),
    Column('ind_works', Integer),
    Column('exams', Integer),
    Column('advice', Integer),
    Column('total_hours', Float),
    Column('term', String(length=20)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['load'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['load'].drop()
