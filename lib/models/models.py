import datetime

class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

class Post:
    def __init__(self, id, title, content, created_at, author):
        self.id = id
        self.title = title
        self.content = content
        self.created_at = created_at
        self.author = author

    @staticmethod
    def from_row(row):
        return Post(
            id=row[0],
            title=row[1],
            content=row[2],
            created_at=row[3],
            author=User(row[4], row[5], row[6])
        )

class Database:
    def __init__(self, filename):
        self.filename = filename

    def connect(self):
        import sqlite3
        self.conn = sqlite3.connect(self.filename)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                author_id INTEGER NOT NULL,
                FOREIGN KEY (author_id) REFERENCES users (id)
            )
        ''')
        self.conn.commit()

    def insert_user(self, name, email):
        self.cursor.execute('''
            INSERT INTO users (name, email) VALUES (?, ?)
        ''', (name, email))
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_post(self, title, content, author_id):
        self.cursor.execute('''
            INSERT INTO posts (title, content, created_at, author_id) VALUES (?, ?, ?, ?)
        ''', (title, content, datetime.datetime.now(), author_id))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_posts(self):
        self.cursor.execute('''
            SELECT * FROM posts ORDER BY created_at DESC
        ''')
        rows = self.cursor.fetchall()
        return [Post.from_row(row) for row in rows]

    def close(self):
        self.conn.close()