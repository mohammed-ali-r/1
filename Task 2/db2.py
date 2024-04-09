import sqlite3

# Create connection to SQLite DB
conn= sqlite3.connect("zoo.db")
cursor= conn.cursor()

# Create users table
cursor.execute('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT, firstname TEXT, lastname TEXT, address TEXT, dob TEXT)'''
               )

# Creates a table called users in zoo db that has an ID that goes up by itself and is the primary key, has email and password which will be hashed, first name , last name, address and dob