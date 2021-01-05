#!/usr/bin/env python
import datetime
from sqlalchemy import Column
from sqlalchemy import DateTime, Boolean, Integer, String, ForeignKey, Text, \
    BigInteger
from sqlalchemy.orm import backref, object_mapper, relationship


class ModelBase():
    """Base class for models."""

    __table_initialized__ = False
    __table_args__ = {'mysql_engine': 'InnoDB'}
    __default_time = datetime.datetime.utcnow()

    created_at = Column(DateTime, default=__default_time)
    updated_at = Column(DateTime, default=__default_time,
                        onupdate=__default_time)
    deleted_at = Column(DateTime)
    deleted = Column(Boolean, default=False)
    metadata = None

    def save(self, session=None):
        """Save this object."""
        if not session:
            session = get_session()
        with session.begin(subtransactions=True):
            session.add(self)
            session.flush()

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def __iter__(self):
        columns = list(dict(object_mapper(self).columns).keys())
        if hasattr(self, '_extra_keys'):
            columns.extend(self._extra_keys())

        self._i = iter(columns)
        return self

    def __next__(self):
        n = next(self._i)
        return n, getattr(self, n)

    def update(self, values):
        """Make the model object behave like a dict."""
        for k, v in values.items():
            setattr(self, k, v)

    def _as_dict(self):
        """Make the model object behave like a dict.
        Includes attributes from joins.
        """
        local = dict((key, value) for key, value in self)
        joined = dict([(k, v) for k, v in self.__dict__.items()
                       if k[0] != '_'])
        local.update(joined)
        return local

    def iteritems(self):
        """Make the model object behave like a dict."""
        return self._as_dict().items()

    def items(self):
        """Make the model object behave like a dict."""
        return self._as_dict().items()

    def keys(self):
        """Make the model object behave like a dict."""
        return [key for key, value in self.iteritems()]

    def delete(self, session=None):
        """Delete this object."""
        self.deleted = True
        self.deleted_at = datetime.datetime.utcnow()
        self.save(session=session)

