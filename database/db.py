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

    def _create_habit_tables(self):
        query = "CREATE TABLE IF NOT EXISTS habits(id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)"
        self._execute(query)

    def insert(self, string: str):
        values = (string, )
        query = "INSERT INTO habits (text) VALUES (?)"
        self._execute(query, values)

    def get_all(self):
        query = "SELECT text FROM habits"
        self._execute(query)
        return self._cur.fetchall()
