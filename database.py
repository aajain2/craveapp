import sqlite3

class Database:
    def __init__(self, db_name='crave.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                dietary_restrictions TEXT
            )
        ''')
        self.conn.commit()

    def add_user(self, name, dietary_restrictions):
        self.cursor.execute('INSERT INTO users (name, dietary_restrictions) VALUES (?, ?)',
                            (name, dietary_restrictions))
        self.conn.commit()

    def get_user_preferences(self, user_id):
        self.cursor.execute('SELECT dietary_restrictions FROM users WHERE id = ?', (user_id,))
        return self.cursor.fetchone()[0]

    def close(self):
        self.conn.close()