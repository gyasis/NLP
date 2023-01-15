
# %%
import sqlite3

def create_db():
    conn = sqlite3.connect('hours_and_date.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE hours (date text, hours real, unique_id INTEGER PRIMARY KEY AUTOINCREMENT)''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()




# %%

def insert_data(date, hours):
    conn = sqlite3.connect('hours_and_date.db')
    c = conn.cursor()
    c.execute("INSERT INTO hours (date, hours) VALUES (?, ?)", (date, hours))
    conn.commit()
    conn.close()


# %%
import psycopg2
import sqlite3

def sync_databases(local_db_path, remote_db_config):
    # Connect to local SQLite database
    local_conn = sqlite3.connect(local_db_path)
    local_cursor = local_conn.cursor()
    
    # Connect to remote PostgreSQL database
    remote_conn = psycopg2.connect(
        host=remote_db_path['host'],
        port=remote_db_path['port'],
        user=remote_db_path['user'],
        password=remote_db_path['password'],
        database=remote_db_path['database']
    )
    remote_cursor = remote_conn.cursor()
    
    try:
        # Fetch all records from the local SQLite database
        local_cursor.execute("SELECT * FROM hours")
        local_records = local_cursor.fetchall()

        # Fetch all records from the remote PostgreSQL database
        remote_cursor.execute("SELECT * FROM hours")
        remote_records = remote_cursor.fetchall()
        
        # Compare the local and remote records
        for local_record in local_records:
            found = False
            for remote_record in remote_records:
                if local_record[0] == remote_record[0] and local_record[1] == remote_record[1] and local_record[2] == remote_record[2]:
                    found = True
                    break
            if not found:
                # Insert the local record into the remote database
                remote_cursor.execute("INSERT INTO hours (date, hours, unique_id) VALUES (?, ?, ?)", (local_record[0], local_record[1], local_record[2]))
                remote_conn.commit()
    finally:
        local_conn.close()
        remote_conn.close()
