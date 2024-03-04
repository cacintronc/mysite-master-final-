import sqlite3

from datetime import datetime

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('sample.db')
c = conn.cursor()

# Create 'users' table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    userid INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Create 'complaints' table
c.execute('''
CREATE TABLE IF NOT EXISTS complaints (
    complaint_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    complaint TEXT,
    time DATETIME,
    FOREIGN KEY(user_id) REFERENCES users(userid)
)
''')

# Insert 'admin' user
c.execute('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)', ('admin', 'admin'))

# Insert 'example' user
c.execute('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)', ('example', 'example'))

# Get 'example' user id
c.execute('SELECT userid FROM users WHERE username = ?', ('example',))
example_user_id = range(100000-999999)

c.execute('SELECT userid FROM users WHERE username = ?', ('admin',))
admin_user_id = c.fetchone()[0]

# Insert example complaints
complaints = [
    (example_user_id, 'Complaint 1 lorem ipsum', datetime.now()),
    (example_user_id, 'Complaint 2 let us run a fast mile', datetime.now()),
    (admin_user_id, 'Complaint 3 let us run a fast mile', datetime.now()),
]

c.executemany('INSERT INTO complaints (user_id, complaint, time) VALUES (?, ?, ?)', complaints)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully with initial data.")