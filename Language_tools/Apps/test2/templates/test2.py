# %%

import sqlite3

class SQLiteDatabase:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS log_table(unique_id INTEGER PRIMARY KEY, hours REAL, date DATE)'''
        )
        self.conn.commit()

    def insert_data(self, unique_id, hours, date):
        self.cursor.execute(
            '''INSERT INTO log_table(unique_id, hours, date) VALUES(?,?,?)''', (unique_id, hours, date)
        )
        self.conn.commit()

    def retrieve_data(self):
        self.cursor.execute('''SELECT * FROM log_table''')
        rows = self.cursor.fetchall()
        return rows

    def close_connection(self):
        self.conn.close()
        
# %%
import psycopg2
from datetime import datetime

def sync_databases(local_db, remote_db):
    # Connect to the local database
    local_conn = psycopg2.connect(
        host=local_db["host"],
        port=local_db["port"],
        user=local_db["user"],
        password=local_db["password"],
        database=local_db["database"],
    )
    local_cursor = local_conn.cursor()

    # Connect to the remote database
    remote_conn = psycopg2.connect(
        host=remote_db["host"],
        port=remote_db["port"],
        user=remote_db["user"],
        password=remote_db["password"],
        database=remote_db["database"],
    )
    remote_cursor = remote_conn.cursor()

    try:
        # Find the most recent update time in the local and remote databases
        local_cursor.execute("SELECT MAX(update_time) FROM log_table")
        local_time = local_cursor.fetchone()[0]
        remote_cursor.execute("SELECT MAX(update_time) FROM log_table")
        remote_time = remote_cursor.fetchone()[0]
        
        if local_time == None:
            local_time = datetime(1970,1,1)
        if remote_time == None:
            remote_time = datetime(1970,1,1)
        
        # Check which database has the most recent data
        if local_time > remote_time:
            # Sync the remote database with the local database
            remote_cursor.execute("DELETE FROM log_table")
            local_cursor.execute("SELECT * FROM log_table")
            rows = local_cursor.fetchall()
            for row in rows:
                remote_cursor.execute("INSERT INTO log_table VALUES (%s, %s, %s, %s)", row)
            remote_conn.commit()
            print("Remote database synced with local database.")
        elif local_time < remote_time:
            # Sync the local database with the remote database
            local_cursor.execute("DELETE FROM log_table")
            remote_cursor.execute("SELECT * FROM log_table")
            rows = remote_cursor.fetchall()
            for row in rows:
                local_cursor.execute("INSERT INTO log_table VALUES (%s, %s, %s, %s)", row)
            local_conn.commit()
            print("Local database synced with remote database.")
        else:
            print("Local and remote databases are already synced.")
    finally:
        local_conn.close()
        remote_conn.close()

# Example usage
local_db = {
    "host": "localhost",
    "port": "5432",
    "user": "user",
    "password": "password",
    "database": "local_db",
}
remote_db = {
    "host": "remote_host",
    "port": "5432",
    "user": "user",
    "password": "password",
    "database": "remote_db",
}

sync_databases(local_db, remote_db)


# %%

from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/sync", methods=["GET"])
def sync():
    local_db = {
        "host": "localhost",
        "port": "5432",
        "user": "user",
        "password": "password",
        "database": "local_db",
    }
    remote_db = {
        "host": "remote_host",
        "port": "5432",
        "user": "user",
        "password": "password",
        "database": "remote_db",
    }

    sync_databases(local_db, remote_db)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
