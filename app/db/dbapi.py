__author__ = 'sajive'
import uuid
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import logging
from ..db import consts, models
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

#db_string = "postgres://admin:donotusethispassword@aws-us-east-1-portal.19.dblayer.com:15813/compose"


def get_engine():
    return create_engine(consts.db_string_pgsql, echo=True)


def get_session(engine):
    Session = sessionmaker(engine)
    session = Session()
    return session


gEngine = get_engine()


def model_query(*args, **kwargs):
    """Query helper that accounts for context's `read_deleted` field.
    :param context: context to query under
    :param session: if present, the session to use
    :param read_deleted: if present, overrides context's read_deleted field.
    :param project_only: if present and context is user-type, then restrict
            query to match the context's project_id.
    """
    session = kwargs.get('session') or get_session(gEngine)
    read_deleted = kwargs.get('read_deleted') or 'no'  # context.read_deleted
    project_only = kwargs.get('project_only')

    query = session.query(*args)
    print(query.__dict__)

    if read_deleted == 'no':
        query = query.filter_by(deleted=False)
    elif read_deleted == 'yes':
        pass  # omit the filter to include deleted and active
    elif read_deleted == 'only':
        query = query.filter_by(deleted=True)
    else:
        raise Exception(
            "Unrecognized read_deleted value '%s'" % read_deleted)
    return query


def get_agency(filters=None, session=None):
    print_metadata()
    if filters is None:
        return model_query(models.AgencyOrm,
                           session=session, read_deleted='no').all()
    else:
        return model_query(models.AgencyOrm,
                           session=session).filter_by(**filters).all()


def create_agency(session=None, values=None):
    session = get_session(get_engine())
    agency_ref = models.AgencyOrm()
    print(type(agency_ref))

    values['id'] = str(uuid.uuid4())
    agency_ref.update(values)
    print(agency_ref.__dict__)

    agency_ref.save(session=session)
    session.commit()


def print_metadata():
    pg_tables = pg_tables = sa.Table(
        'pg_tables', sa.MetaData(),
        sa.Column('schemaname'),
        sa.Column('tablename'),
        sa.Column('tableowner'),
        sa.Column('tablespace'),
        sa.Column('hasindexes')
    )
    query = pg_tables.select().where(pg_tables.c.schemaname == 'pg_catalog')

# sqlalchemy statement with parameters
    query = sa.select('*') \
        .select_from(sa.text('sqrt(:num) as a')) \
        .select_from(sa.text('sqrt(:a2) as b')) \
        .select_from(sa.text('sqrt(:z3) as c')) \
        .params(num=16, a2=36, z3=25)
