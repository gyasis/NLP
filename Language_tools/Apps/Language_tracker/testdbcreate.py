import sqlite3

# Connect to or create the database
conn = sqlite3.connect('tree.db')

# Create a cursor
c = conn.cursor()

# Create a table named 'test_data'
c.execute('''CREATE TABLE IF NOT EXISTS test_data
             (id INTEGER PRIMARY KEY, name TEXT, value REAL)''')

# Add a new entry to the table
c.execute("INSERT INTO test_data VALUES (1, 'example', 3.14)")

# Commit the changes and close the connection
conn.commit()
conn.close()
