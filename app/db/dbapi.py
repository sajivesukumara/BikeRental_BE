import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import db.models as models
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

#db_string = "postgres://admin:donotusethispassword@aws-us-east-1-portal.19.dblayer.com:15813/compose"
db_string = "postgresql://postgres:hpinvent@127.0.0.1/bike_rental"


def get_engine():
    return create_engine(db_string, echo=True)


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
    read_deleted = kwargs.get('read_deleted') or 'no' #context.read_deleted
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
