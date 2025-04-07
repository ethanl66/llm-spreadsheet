class DbManager:
    def __init__(self, db_name):
        import sqlite3
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        if params is None:
            params = []
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_all(self, query, params=None):
        if params is None:
            params = []
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        if params is None:
            params = []
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()