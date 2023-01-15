# db_helper.py
import sqlite3
import psycopg2
import os

from datetime import datetime

class SQLiteDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(os.path.join(app.root_path,db_name))
        self.cursor = self.conn.cursor()

    def create_table(self):
        """
        Create a table named 'data_entry' 
        """
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS data_entry
                            (uniqe_id INTEGER PRIMARY KEY, hours INTEGER, date DATE)''')

    def insert(self, values):
        """
        Insert values into data_entry table
        :param values: values to insert in a tuple format
        """
        placeholders = ", ".join(["?" for _ in values])
        query = f"INSERT INTO data_entry(uniqe_id,hours,date) VALUES({placeholders})"
        self.cursor.execute(query, values)

    def close(self):
        """
        Commit any changes and close the connection
        """
        self.conn.commit()
        self.conn.close()

    def retrieve_data(self):
        self.cursor.execute('''SELECT * FROM log_table''')
        rows = self.cursor.fetchall()
        return rows

    def close_connection(self):
        self.conn.close()

def sync_databases(local_db, remote_db):
    # ... function code ...
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



import plotly.graph_objects as go

def create_bar_chart(local_db):
    # Connect to the local SQLite database
    local_conn = sqlite3.connect(local_db)
    local_cursor = local_conn.cursor()

    # Retrieve the data from the database
    local_cursor.execute("SELECT date, SUM(hours) FROM logs GROUP BY date")
    logs = local_cursor.fetchall()
    dates = [log[0] for log in logs]
    hours = [log[1] for log in logs]

    # Create the bar chart
    fig = go.Figure(data=[go.Bar(x=dates, y=hours)])
    fig.update_layout(title='Total hours per day', xaxis_title='Date', yaxis_title='Total Hours')

    return fig.to_json()