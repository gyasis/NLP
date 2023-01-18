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
    
    
    # make dates readable
    
    return a1_date, a2_date, b1_date, b2_date


# %%
#create table in database if not there
def create_milestones():
    conn = sqlite3.connect('milestones.db')
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE milestones (
            a1 DATE,
            a2 DATE,
            b1 DATE,
            b2 DATE)''')
        conn.commit()
        conn.close()
        conn = sqlite3.connect('milestones.db')
        c = conn.cursor()
        c.execute("INSERT INTO milestones VALUES (?,?,?,?)", milestones)
        conn.commit()
        conn.close()
    
    except:
        print('Table already exists\nTrying to update table...')
        conn.close()
    
# add table values to database

  
#update table values in database
def update_milestones(milestones):
    conn = sqlite3.connect('milestones.db')
    c = conn.cursor()
    c.execute("UPDATE milestones SET a1=?, a2=?, b1=?, b2=?", milestones)
    conn.commit()
    conn.close()
# %%


while True:
    # Prompt the user for the target date of B2 completion
    b2_date_text = input('Enter the target date of B2 completion (mm/dd/yyyy): ')
    # Convert the user input to a datetime object
    b2_date = datetime.strptime(b2_date_text, '%m/%d/%Y')
    original_b2_date = b2_date
    
    # Prompt the user for the number of hours per day or week
    hours_per_day_text = input('Enter the number of hours per day or week (d/w): ')
    if hours_per_day_text == 'w':
        #divided by 7 to get hours per day
        hours_per_day = float(input('Enter the number of hours per week: ')) / 7
    elif hours_per_day_text == 'd':
        hours_per_day = float(input('Enter the number of hours per day: '))
        
        
        
    # Calculate the estimated date of each milestone
    a1_date, a2_date, b1_date, b2_date = calculate_milestone(datetime.now(), hours_per_day, proficiency_levels)
    milestones = [a1_date, a2_date, b1_date, b2_date]
    #if calculated b2 date is after the target date, then warn that date will be passed and give a weekly hour estimate to get to target
    # if b2_date > original_b2_date:
    #     print('Warning: The target date of B2 completion will be passed.')
    #     print('You will need to study', round((get_days_from_now(original_b2_date) * 6yt hours_per_day) / 7, 2), 'hours per week to reach the target date.')
    
    # Display the milestones in a table
    print(tabulate([
    ['A1', a1_date.strftime('%m/%d/%Y')],
    ['A2', a2_date.strftime('%m/%d/%Y')],
    ['B1', b1_date.strftime('%m/%d/%Y')],
    ['B2', b2_date.strftime('%m/%d/%Y')]
    ], headers=['Milestone', 'Estimated Date']))
   
    #prompt user to save data to database
    save = input('Would you like to save this data to the database? (y/n): ')
    if save == 'y':
        #check for database and table and create and save otherwise update
        create_milestones()
      
        update_milestones(milestones)
    
    #print out contents of database
    conn = sqlite3.connect('milestones.db')
    table = pd.read_sql_query("SELECT * FROM milestones", conn)
    print(table)
    # Prompt the user to rerun the script or quit
    repeat = input('Enter "r" to rerun the script, or "q" to quit: ')
    if repeat == 'q':
        break
# %%