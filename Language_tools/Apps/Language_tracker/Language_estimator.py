# %%

from tabulate import tabulate
from datetime import datetime, timedelta
import sqlite3
import pandas as pd

# Define the proficiency levels and the number of hours required to reach each level
    



proficiency_levels = {'A1': 200, 'A2': 300, 'B1': 400, 'B2': 750}

#get now datetime and get amount of days from entered data

def get_days_from_now(b2_date):
    now = datetime.now()
    return (b2_date - now).days

def calculate_milestone(now, hours_per_day, proficiency_levels):
    # Calculate the estimated date of each milestone

    
    a1_date = now + timedelta(days=(proficiency_levels['A1'] / hours_per_day))
    a2_date = now + timedelta(days=(proficiency_levels['A2'] / hours_per_day))
    b1_date = now + timedelta(days=(proficiency_levels['B1'] / hours_per_day))
    b2_date = now + timedelta(days=(proficiency_levels['B2'] / hours_per_day))
    

    return a1_date, a2_date, b1_date, b2_date


# create database
def create_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE test (date text, hours real, tags text DEFAULT 'Uncategorized', notes text, unique_id INTEGER PRIMARY KEY AUTOINCREMENT)''')
        c.execute('''CREATE TABLE milestones (
                a1 DATE,
                a2 DATE,
                b1 DATE,
                b2 DATE)''')
    except sqlite3.OperationalError as e:
        if 'table test already exists' in str(e):
            pass
        else:
            raise e
    conn.commit()
    conn.close()
        
def check_database():
    try:
        conn = sqlite3.connect('test.db')
        print('Database exists')
        conn.close()
    except:
        create_db()
# %%

# add table values to database
def create_milestones(a1, a2, b1, b2):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    import pandas as pd
    
    df = pd.read_sql_query("SELECT * FROM milestones", conn)
    
    
    try:
        type(df['a1'][0])
        
    except:
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("INSERT INTO milestones (a1, a2, b1, b2) VALUES  (?, ?, ?, ?)", (a1, a2, b1, b2))
        conn.commit()
        conn.close()
    



  
#update table values in database
def update_milestones(a1, a2, b1, b2):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    
    print("updating milestones")
    c.execute("UPDATE milestones SET a1=?, a2=?, b1=?, b2=?", (a1, a2, b1, b2))
    conn.commit()
    
    #print out contents of database
    table = pd.read_sql_query("SELECT * FROM milestones", conn)
    print(table)
    
    conn.close()
# %%


# %%