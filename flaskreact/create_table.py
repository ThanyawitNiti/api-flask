import sqlite3
conn = sqlite3.connect('database.db')

print('Connect db 200')

conn.execute('CREATE TABLE user (first_name TEXT, last_name TEXT, username TEXT,password TEXT)')

conn.close