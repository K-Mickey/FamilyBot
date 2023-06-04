import logging
import os
import sqlite3

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
        query = "CREATE TABLE IF NOT EXISTS actual_habits(id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, habit_id INT)"
        self._execute(query)

    def habits_insert(self, string: str):
        values = (string, )
        query = "INSERT INTO habits (text) VALUES (?)"
        self._execute(query, values)

    def habits_find_note(self, but_id: int):
        values = (but_id, )
        query = "SELECT text FROM habits WHERE id=(?)"
        self._execute(query, values)
        return self._cur.fetchone()

    def habits_get(self, text: bool = True):
        query = "SELECT text FROM habits" if text else "SELECT * FROM habits"
        self._execute(query)
        return self._cur.fetchall()

    def habits_remove(self, text: str = None):
        if not text:
            query = "DELETE FROM habits"
            self._execute(query)
            return

        values = (text, )
        query = "DELETE FROM habits WHERE text=(?)"
        self._execute(query, values)

    def actual_habits_insert(self, text: str, habit_id: int):
        values = (text, habit_id)
        query = "INSERT INTO actual_habits (text, habit_id) VALUES (?, ?)"
        self._execute(query, values)

    def actual_habits_get(self):
        query = "SELECT text FROM actual_habits"
        self._execute(query)
        return self._cur.fetchall()

    def actual_habits_find_note(self, but_id: int):
        values = (but_id, )
        query = "SELECT text FROM actual_habits WHERE habit_id=(?)"
        self._execute(query, values)
        return self._cur.fetchone()
