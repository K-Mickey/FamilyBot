import sqlite3


class DataBase:
    def __init__(self, name: str = "test.db"):
        self._conn = sqlite3.connect(name)
        self._cur = self._conn.cursor()

    def __del__(self):
        self._conn.close()

    def _execute(self, query: str, values: tuple = tuple()):
        args = (query, values) if values else (query, )
        self._cur.execute(*args)
        print(self._cur)
        self._conn.commit()

    def create_tables(self):
        self._create_habit_tables()
        self._create_actual_habits_tables()

    def _create_habit_tables(self):
        query = "CREATE TABLE IF NOT EXISTS habits(id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)"
        self._execute(query)

    def _create_actual_habits_tables(self):
        query = "CREATE TABLE IF NOT EXISTS actual_habits(id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)"
        self._execute(query)

    def habits_insert(self, string: str):
        values = (string, )
        query = "INSERT INTO habits (text) VALUES (?)"
        self._execute(query, values)

    def habits_get(self):
        query = "SELECT text FROM habits"
        self._execute(query)
        return self._cur.fetchall()

    def habits_remove(self, text: str):
        values = (text, )
        query = "DELETE FROM habits WHERE text=(?)"
        self._execute(query, values)


    def actual_habits_insert(self, string: str):
        values = (string, )
        query = "INSERT INTO actual_habits (text) VALUES (?)"
        self._execute(query, values)

    def actual_habits_get(self):
        query = "SELECT text FROM actual_habits"
        self._execute(query)
        return self._cur.fetchall()
