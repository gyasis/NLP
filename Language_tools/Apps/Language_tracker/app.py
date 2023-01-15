# app.py
from flask import Flask, render_template, request, jsonify
from db_helper import *
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    # chart_data = create_bar_chart('logs.db')
    return render_template('index.html', 
                        #    chart_data=chart_data
                        )

def connect_(x):
    # create a connection to the database
    conn = sqlite3.connect(x)
    
    return conn



@app.route('/submit', methods=['POST'])
def submit():
    hours = request.form.get('hours')
    date = request.form.get('date')
    print(hours, date) 
    conn = connect_('/media/gyasis/Blade 15 SSD/Users/gyasi/Google Drive (not syncing)/Collection/playground/NLP/Language_tools/Apps/Language_tracker/thisbetterwork.db')
    # # insert data to SQLite/PostgreSQL Database
    # db = SQLiteDatabase('/media/gyasis/Blade 15 SSD/Users/gyasi/Google Drive (not syncing)/Collection/playground/NLP/Language_tools/Apps/Language_tracker/thisbetterwork.db')
    # db.create_table()
    # db.insert_data(hours, date)
    # db.close_connection()
    # return jsonify({"status": "success"})

    
    #check if the database exists(path)
    conn.execute('''CREATE TABLE IF NOT EXISTS logs(id INTEGER PRIMARY KEY, hours REAL, date DATE)''')
    
    # insert form data into database 
    conn.execute("INSERT INTO logs (hours, date) VALUES (?, ?)", (hours, date))
    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    app.run(debug=True)
