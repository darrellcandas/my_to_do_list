import sqlite3

def create_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            UNIQUE(name, email)
        )
    ''')
    conn.commit()
    conn.close()

def add_user(name, email):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        result = "User added successfully!"
    except sqlite3.IntegrityError:
        result = "User already exists!"
    conn.close()
    return result

def get_users():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()
    return users

# Ensure the table is created when the module is imported
create_table()

