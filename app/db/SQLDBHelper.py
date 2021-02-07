#!/usr/bin/python3
__author__ = 'sajive'

import logging
import os
from configparser import ConfigParser
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, Table, MetaData, \
    insert, update, select, false
from sqlalchemy import exc as sa_exceptions
from app.db.DBHelper import DBHelper
from app.db import constants
import json

log_dir = os.getcwd()
log_filename = os.path.join(log_dir, 'db_client.log')
log_level = logging.INFO
log_fmt = ('%(asctime)s.%(msecs)03d %(process)d %(levelname)s '
           '%(name)s [-] %(message)s')
datefmt = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(filename=log_filename, format=log_fmt, datefmt=datefmt,
                    level=log_level)

LOG = logging.getLogger(__name__)


class SQLDBHelper(DBHelper):
    """
    A DB helper library for connecting to and performing a CRUD
    on a SQL databases. Can be used across python applications
    as a library using SQL databases as DB engine for cataloging.
    """

    def __init__(self, dialect=constants.POSTGRES_DIALECT):
        """
        Constructor for initializing the engine
        :param dialect: Switch for SQL databases. Dialects supported are:
                        MYSQL, PostGreSQL, Oracle, SQLite, MSSQL Server etc..
        :return:
        """
        self.__engine = None
        self.__tables = None
        __db_config_dict = os.getenv(constants.DB_CONFIG)
        __db_config_dict = json.loads(__db_config_dict)
        __db_config = __db_config_dict[dialect]
        __db_connection_cfg = {k: v for k, v in __db_config.items()
                               if k in constants.CONNECTION_KEYS}

        connection_string = URL(**__db_connection_cfg)
        engine_args = dict()
        if __db_config.get('pool_size'):
            engine_args['pool_size'] = __db_config.get('pool_size')
        if __db_config.get('max_overflow'):
            engine_args['max_overflow'] = __db_config.get('max_overflow')
        if __db_config.get('timeout'):
            engine_args['timeout'] = __db_config.get('timeout')

        # first try creating engine using lazy connect
        try:
            engine = create_engine(connection_string, **engine_args)
        except sa_exceptions.ArgumentError as err:
            LOG.error('Failed to create engine to database: '
                      'Reason: %s. Please review : %s'
                      % (str(err), str(connection_string)))
            raise
        except Exception as err:
            LOG.error('Failed to create engine to database: '
                      'Reason: %s.' % str(err))
            raise

        # secondly try opening a connection
        try:
            conn = engine.connect()
            conn.close()
        except sa_exceptions.DatabaseError as err:
            LOG.error('Failed to create connection to database: '
                      'Reason: %s.' % str(err))
            raise

        self.__engine = engine

        # get all tables from the engine
        meta = MetaData()
        meta.reflect(bind=engine)
        self.__tables = meta.tables

    def dispose_engine(self):
        """
        Disposes the database engine.
        """
        try:
            self.__engine.dispose()
            LOG.info('Engine disposed')
        except Exception as ex:
            LOG.error('Failed to dispose engine.'
                      ' Reason: %s ', str(ex))
            raise

    def insert_records(self, table, values):
        """
        Inserts the record into table.
        :param table: Table name
        :param values: record values in form of json dict
        or list(json dict) matching table columns.
        :return:
        """
        try:
            table_obj = self.__tables[table]
            ins = insert(table_obj)
            with self.__engine.connect() as conn:
                values.update({'deleted': False})
                conn.execute(ins, values)
            LOG.info('Data loaded into table %s.' % table)
        except Exception as ex:
            LOG.error("Failed to insert rows into table %s. Reason: %s "
                      % (table, str(ex)))
            raise

    def delete_record(self, table, resource_id):
        """
        Soft deletes the record from the table
        :param table: Table name
        :param resource_id: Unique resource id to be deleted.
        :return:
        """
        try:
            table_obj = self.__tables[table]
            delete_query = update(table_obj).\
                where(table_obj.c.id == resource_id).\
                values(deleted=True)
            with self.__engine.connect() as conn:
                conn.execute(delete_query)
            LOG.info('Data deleted from table %s.' % table)
        except Exception as ex:
            LOG.error('Failed to delete record from table %s. Reason: %s ',
                      table, str(ex))
            raise

    def get_records(self, table):
        """
        Get all records from the table
        :param table:
        :return:
        """
        try:
            table_obj = self.__tables[table]
            select_query = select([table_obj]).\
                where(table_obj.c.deleted == false())
            with self.__engine.connect() as conn:
                result = conn.execute(select_query)
            LOG.info('Data record fetched from table %s.' % table)
            return [dict(row) for row in result]
        except Exception as ex:
            LOG.error('Failed to fetch rows from table %s. Reason: %s ',
                      table, str(ex))
            raise

    def get_record(self, table, resource_id):
        """
        Get record for a specific resource in the table
        :param table:
        :param resource_id:
        :return:
        """
        try:
            table_obj = self.__tables[table]
            select_query = select([table_obj]).\
                where((table_obj.c.id == resource_id) &
                      (table_obj.c.deleted == false()))
            with self.__engine.connect() as conn:
                result = conn.execute(select_query)
            LOG.info('Data record fetched from table %s.' % table)
            return [dict(row) for row in result][0] \
                if result.rowcount else dict()

        except Exception as ex:
            LOG.error('Failed to fetch rows from table %s. Reason: %s ',
                      table, str(ex))
            raise

    def update_record(self, table, resource_id, values):
        """
        Updates a specific record in the table
        :param table: table name
        :param resource_id: record to be updated
        :param values: update values
        :return:
        """
        try:
            table_obj = self.__tables[table]
            delete_query = update(table_obj).\
                where(table_obj.c.id == resource_id).\
                values(values)
            with self.__engine.connect() as conn:
                conn.execute(delete_query)
            LOG.info('Data updated for table %s.' % table)
        except Exception as ex:
            LOG.error('Failed to update record from table %s. Reason: %s ',
                      table, str(ex))
            raise

    def truncate_table(self, table):
        """
        Deletes all rows in a table
        :param table:
        :return:
        """
        try:
            table_obj = self.__tables[table]
            delete_query = table_obj.delete()
            with self.__engine.connect() as conn:
                conn.execute(delete_query)
            LOG.info('All records deleted for table %s.' % table)
        except Exception as ex:
            LOG.error('Failed to delete all records from table %s. '
                      'Reason: %s ', table, str(ex))
            raise