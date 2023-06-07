import logging
import os
import sqlite3
from typing import Iterable

from config import LOG_FMT

logger = logging.getLogger(__name__)
logfile = logging.FileHandler("database/log_db.log")
logfile.setLevel(logging.DEBUG)
logfile.setFormatter(logging.Formatter(LOG_FMT))
logger.addHandler(logfile)


class DataBase:

    def __init__(self, name: str = "test.db"):
        self._name = name
        self._conn = sqlite3.connect(self._name)
        self._cur = self._conn.cursor()

        self.create_tables()

    def __del__(self):
        self._conn.close()

    def _execute(self, query: str, values: tuple = tuple()):
        args = (query, values) if values else (query, )
        logger.debug(str(args))
        self._cur.execute(*args)
        self._conn.commit()

    def create_tables(self):
        if not os.path.exists(self._name):
            logger.info("DB WAS CREATE")
        self._create_habit_tables()
        self._create_actual_habits_tables()

    def _create_habit_tables(self):
        query = "CREATE TABLE IF NOT EXISTS habits(id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)"
        self._execute(query)

    def _create_actual_habits_tables(self):
        query = """
        CREATE TABLE IF NOT EXISTS actual_habits(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        text TEXT, 
        btn_id INT
        )"""
        self._execute(query)

    def insert(self, name_table: str = None, **kwargs) -> None:
        values = tuple(kwargs.values())

        query_args = self._join_values(kwargs)
        n_query_values = self._join_n_questions(values)
        query = f"INSERT INTO {name_table} ({query_args}) VALUES ({n_query_values})"

        self._execute(query, values)

    def remove(self, name_table: str = None, **kwargs) -> None:
        query = f"DELETE FROM {name_table}"
        values = None
        if kwargs:
            where_val = self._join_by_and(kwargs)
            query += f" WHERE {where_val}"
            values = tuple(kwargs.values())

        self._execute(query, values)

    def get(self, name_table: str = None, select: Iterable = (), **kwargs) -> Iterable:
        name_columns = self._join_values(select) if select else "*"
        query = f"SELECT {name_columns} FROM {name_table}"
        values = None
        if kwargs:
            where_val = self._join_by_and(kwargs)
            query += f" WHERE {where_val}"
            values = tuple(kwargs.values())

        self._execute(query, values)
        return self._cur.fetchall()

    @staticmethod
    def _join_by_and(values: Iterable):
        return " AND ".join([f"{i}=(?)" for i in values])

    @staticmethod
    def _join_values(values: Iterable):
        return ", ".join([str(arg) for arg in values])

    @staticmethod
    def _join_n_questions(values: tuple) -> str:
        return ", ".join("?" * len(values))
