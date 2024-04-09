import sqlite3

# Create connection to SQLite DB
conn= sqlite3.connect("zoo.db")
cursor= conn.cursor()

# Create contact table
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, phone TEXT, message TEXT)'''
               )

# Creates a table called contact in zoo db that has an ID that goes up by itself and is the primary key, has a name email and phone as well as the msg.