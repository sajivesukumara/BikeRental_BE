from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
import models

DB_CONN_URL = 'postgresql://datum:hpinvent@127.0.0.1/datum'

engine = create_engine(DB_CONN_URL, echo=True)

Base = declarative_base()


Session = sessionmaker(bind=engine)
session = Session()


def model_query(context, *args, **kwargs):
    """Query helper that accounts for context's `read_deleted` field.
    :param context: context to query under
    :param session: if present, the session to use
    :param read_deleted: if present, overrides context's read_deleted field.
    :param project_only: if present and context is user-type, then restrict
            query to match the context's project_id.
    """
    session = kwargs.get('session') or get_session()
    read_deleted = kwargs.get('read_deleted') or context.read_deleted
    project_only = kwargs.get('project_only')

    query = session.query(*args)

    if read_deleted == 'no':
        query = query.filter_by(deleted=False)
    elif read_deleted == 'yes':
        pass  # omit the filter to include deleted and active
    elif read_deleted == 'only':
        query = query.filter_by(deleted=True)
    else:
        raise Exception(
            _("Unrecognized read_deleted value '%s'") % read_deleted)

    if project_only and utils.is_user_context(context):
        query = query.filter_by(project_id=context.project_id)

    return query


def create_agents()
c1 = models.CustomersOrm(first_name='Ravi',
                         last_name="Kumar",
                         dob="",
                         address='Station Road Nanded',
                         id_proof="PAN Card",
                         driving_license="DL/2021/02-24",
                         phone_mobile="+91 9090909090",
                         email='ravi@gmail.com')

session.add(c1)
session.commit()


