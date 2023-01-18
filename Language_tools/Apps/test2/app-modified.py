import pandas as pd
from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add', methods=['POST'])
def add():
    hours = request.form['hours']
    date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO test (hours, date) VALUES (?, ?)", (hours, date))
    except sqlite3.IntegrityError as e:
        if 'UNIQUE constraint failed' in str(e):
            pass
        else:
            raise
    conn.commit()
    conn.close()
    return redirect('/')

# @app.route('/data')
# def data():
#     conn = sqlite3.connect('test.db')
#     df = pd.read_sql_query("SELECT * from test", conn)
#     conn.close()
#     return '''
#     <script>
#         window.open("data:text/csv;charset=utf-8,%EF%BB%BF{}", "_blank");
#     </script>
#     '''.format(df.to_csv(index=False))

@app.route('/chart')
def chart():
    conn = sqlite3.connect('test.db')
    df = pd.read_sql_query("SELECT date, SUM(hours) as hours from test GROUP BY date", conn)
    conn.close()
    fig = px.bar(df, x='date', y='hours', labels={'date':'Date', 'hours':'Hours'})
    fig.update_layout(title='Total Hours by Date')
    fig.update_layout(bargap=0.1)
    return fig.show()

if __name__ == '__main__':
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''CREATE TABLE test (id INTEGER PRIMARY KEY AUTOINCREMENT, hours REAL, date DATE)''')
    except sqlite3.OperationalError as e:
        if 'table test already exists' in str(e):
            pass
        else:
            raise
    conn.commit()
    conn.close()
    app.run(debug=True)