# (C) Copyright 2020 Hewlett Packard Enterprise Development Company, L.P.

from abc import ABCMeta, abstractmethod
import threading


class ThreadSafeSingleton(ABCMeta):
    _instances = {}
    _singleton_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._singleton_lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(
                        ThreadSafeSingleton, cls
                    ).__call__(*args, **kwargs)
        return cls._instances[cls]


class DBHelper(metaclass=ThreadSafeSingleton):
    """
    A command line client for connecting to and performing a CRUD
    on any database. Can be used across python applications
    as a library for SQL and NOSQL DB helpers respectively.
    """

    def __init__(self):
        """
        Constructor.
        """
        pass

    @abstractmethod
    def insert_records(self, table, values):
        """
        Insert records into the table
        :param table:
        :param values:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def delete_record(self, table, resource_id):
        """
        Delete records from the table
        :param table:
        :param resource_id:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def get_records(self, table, **kwargs):
        """
        Get all records from the table
        :param table:
        :param kwargs:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def get_record(self, table, resource_id):
        """
        Get individual record from the table
        :param table:
        :param resource_id:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def update_record(self, table, resource_id, values):
        """
        update record in the table
        :param table:
        :param resource_id:
        :param values:
        :return:
        """
        raise NotImplementedError