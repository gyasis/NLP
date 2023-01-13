# %%

import sqlite3
import os

class SQLiteDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        """
        Create a table with the given name and columns
        :param table_name: name of the table to create
        :param columns: columns and their data types in a string format
        """
        query = f"CREATE TABLE IF NOT EXISTS {table_name}({columns})"
        self.cursor.execute(query)

    def insert(self, table_name, values):
        """
        Insert values into a table
        :param table_name: name of the table to insert into
        :param values: values to insert in a tuple format
        """
        placeholders = ", ".join(["?" for _ in values])
        query = f"INSERT INTO {table_name} VALUES({placeholders})"
        self.cursor.execute(query, values)

    def close(self):
        """
        Commit any changes and close the connection
        """
        self.conn.commit()
        self.conn.close()
# %%
# Usage Example

# Create an instance of SQLiteDatabase
db = SQLiteDatabase('/media/gyasis/Blade 15 SSD/Users/gyasi/Google Drive (not syncing)/Collection/playground/NLP/Language_tools/Apps/Language_tracker/tree.db')

# %%
# Create a table named 'test_data' with id, name, and value columns
db.create_table('test_data', 'id INTEGER PRIMARY KEY, name TEXT, value REAL')

# Add a new entry to the test_data table
db.insert('test_data', (1, 'example', 3.14))

# Close the connection
db.close()

# %%
