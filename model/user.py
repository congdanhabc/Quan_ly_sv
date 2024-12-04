import sqlite3

class UserModel:
    def __init__(self, db_name="university.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()
        self.user = None

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    
    def check_login(self, username, password):
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor = self.conn.execute(query, (username, password))
        result = cursor.fetchone()
        if result:
            self.user = {
                "id": result[0],
                "name": result[1],
                "username": result[2],
                "password": result[3]
            }
            return self.user
        return False
    
    def register_user(self, name, username, password):
        try:
            query = "INSERT INTO users (name, username, password) VALUES (?, ?, ?)"
            self.conn.execute(query, (name, username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

