import pandas as pd
from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import plotly.express as px
from Language_estimator import *
from dateutil import parser
from datetime import timedelta
from plotly.graph_objs import Bar
from plotly import offline as plotly, graph_objs as go


app = Flask(__name__)
proficiency_levels = {'A1': 200, 'A2': 300, 'B1': 400, 'B2': 750}


def check_milestones_table():

    try:
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("SELECT * FROM milestones")
        conn.close()
    except:
        try:
            conn.close()
        except:
            pass
        return render_template('setup.html')


@app.route('/')
def home():
    check_database()
    check_milestones_table()
    return render_template('home.html')

@app.route('/add', methods=['POST'])
def add():
    hours = request.form['hours']
    date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    tags = request.form['tags']
    notes = request.form['notes']
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO test (hours, date, tags, notes) VALUES (?, ?, ?, ?)", (hours, date, tags, notes))
    except sqlite3.IntegrityError as e:
        if 'UNIQUE constraint failed' in str(e):
            pass
        else:
            raise
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/chart')
def chart():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT date, SUM(hours) FROM test GROUP BY date")
    data = c.fetchall()
    conn.close()
    x = [d[0] for d in data]
    y = [d[1] for d in data]
    trace = Bar(x=x, y=y)
    layout = go.Layout(title='Total hours studied per day', xaxis=dict(title='Date'), yaxis=dict(title='Hours'))
    chart = plotly.plot([trace], output_type='div')
    return render_template('chart.html', chart=chart)



@app.route('/setup', methods=['GET', 'POST'])

def setup():
    create_db()
    if request.method == 'POST':
        b2_date_text = request.form['b2_date']
        b2_date = datetime.strptime(b2_date_text, '%m/%d/%Y')
        original_b2_date = b2_date
        hours_per_day_text = request.form['hours_per_day_week']
        if hours_per_day_text == 'w':
            print(type(request.form['hours_per_week']))
            hours_per_day = float(request.form['hours_per_week']) / 7
        elif hours_per_day_text == 'd':
            hours_per_day = float(request.form['hours_per_day'])
        a1_date, a2_date, b1_date, b2_date = calculate_milestone(datetime.now(), hours_per_day, proficiency_levels)
        milestones = [a1_date, a2_date, b1_date, b2_date]
        print(f"milestones: {milestones}")
        
        # create_milestones()
        update_milestones(a1_date, a2_date, b1_date, b2_date)
        return render_template('setup.html', a1_date=a1_date, a2_date=a2_date, b1_date=b1_date, b2_date=b2_date)
    else:
        return render_template('setup.html')

@app.route('/pace')
def pace():
    # Calculate the suggested hours per week to catch up
    # Get the current date and calculate the number of days until the closest milestone date
    conn = sqlite3.connect('test.db')
    now = datetime.now()
    c = conn.cursor()
    c.execute("SELECT a1, a2, b1, b2 FROM milestones ORDER BY ABS(strftime('%s', a1) - strftime('%s', ?)) LIMIT 1", (now,))
    
    closest_milestone = c.fetchone()
    c.execute("SELECT SUM(hours) FROM test")
    total_hours = c.fetchone()[0]
    
    c.execute("SELECT COUNT(hours) FROM test")
    total_days = c.fetchone()[0]
    
    # read from database first date entered and count number of days since then
    c.execute("SELECT date FROM test ORDER BY date ASC LIMIT 1")
    get_first_date = c.fetchone()[0]
    weeks_from_first_date = (now - parser.parse(get_first_date)).days /7
    days_from_first_date = (now - parser.parse(get_first_date)).days

    weekly_avg = total_hours / weeks_from_first_date
    weekly_avg_readable = timedelta(hours=weekly_avg)
    hourly_avg = total_hours / days_from_first_date
    hourly_avg_readable = timedelta(hours=hourly_avg) 
    
    

    #calculate current week and last week hours
    current_week_start = now - timedelta(days=now.weekday())
    last_week_start = current_week_start - timedelta(weeks=1)
    c.execute("SELECT SUM(hours) FROM test WHERE datetime(date, 'localtime') >= datetime(?, 'start of day') AND datetime(date, 'localtime') <= datetime(?, 'weekday 6')",(current_week_start, current_week_start))
    current_week_hours = c.fetchone()[0]
    c.execute("SELECT SUM(hours) FROM test WHERE datetime(date, 'localtime') >= datetime(?, 'start of day') AND datetime(date, 'localtime') <= datetime(?, 'weekday 6')",(last_week_start, last_week_start))
    last_week_hours = c.fetchone()[0]

    final_milestone = max(filter(lambda x: (parser.parse(x) - now) >= timedelta(0), closest_milestone), key=lambda x: (parser.parse(x) - now))
    closest_milestone = min(filter(lambda x: (parser.parse(x) - now) >= timedelta(0), closest_milestone), key=lambda x: (parser.parse(x) - now))
    conn.close()
    
    #Calculate days until milestones
    days_until_next_milestone = (parser.parse(closest_milestone) - now).days
    days_until_final_milestone = (parser.parse(final_milestone) - now).days

    #dataframe to show milestones and dates
    # df = pd.DataFrame({'Milestone': ['A1', 'A2', 'B1', 'B2'], 'Date': [a1_date, a2_date, b1_date, b2_date]})

    remaining_hours = proficiency_levels['B2'] - total_hours
    hours_per_day = total_hours/total_days
    #round to nearest 0.5
    suggested_hours_per_week = round(remaining_hours / (days_until_final_milestone / 7), 1)
    estimated_date_of_completion = (now + timedelta(days = (remaining_hours / hourly_avg))).strftime("%B %d, %Y")
    return render_template('pace.html', suggested_hours_per_week=suggested_hours_per_week, days_until_next_milestone = days_until_next_milestone,
    days_until_final_milestone=days_until_final_milestone, total_hours = total_hours,
    estimated_date_of_completion = estimated_date_of_completion, last_week_hours = last_week_hours, current_week_hours = current_week_hours,weekly_avg_readable = weekly_avg_readable, hourly_avg_readable = hourly_avg_readable)




if __name__ == '__main__':
    app.run(debug=True)