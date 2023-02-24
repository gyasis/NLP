# %%

import calendar
from flask import Flask, render_template, request
import pandas as pd
from datetime import date, timedelta

# %%
app = Flask(__name__)

# %%

#Necessary processing
def n_processing(df):
    tree = [date(2023, 1, 2) + timedelta(days=i) for i in range(0, 365, 7)]
    headers = ['Associate'] + tree[0:52]
    df = df.rename(columns=dict(zip(df.columns, headers)))
    df= df.drop([0,1])
    df = df.reset_index(drop=True)
    return df

year = 2023
df = pd.read_excel('~/Downloads/Team_Calender.xlsx', header=None)
df = n_processing(df)

# %%

import calendar
from flask import Flask, render_template, request
import pandas as pd
# from dat

@app.route("/", methods=["GET", "POST"])
def index():
    print('index')
    employees = df["Associate"].tolist()
    if request.method == "POST":
        selected_employee = request.form["employee"]
        selected_employee_data = df.loc[df['Associate'] == selected_employee].iloc[0]
        events = []
        for i in range(len(selected_employee_data)):
            if not pd.isna(selected_employee_data[i]):
                events.append({
                    'title': selected_employee_data[i],
                    'start': f'2023-01-{i+1}',
                    'end': f'2023-01-{i+3}'
                })
        return render_template('calendar.html', events=events)
    else:
        return render_template('index.html', employees=employees)




@app.route("/calendar", methods=['POST'])
def show_calendar():
    print("Showing calendar")
    associate = request.form['events']
    
    
    # Create a dictionary to store the calendar for the selected associate
    calendar = {}
    
    # Get the row for the selected associate
    associate_row = df[df['Associate'] == associate]
    
    # Iterate through the 52 dates
    for i in range(52):
        date = associate_row.iloc[0][i]
        week = i + 1
        print(f"Week {week}: {date}")
        # If there is a location for that week, add it to the calendar
        if not pd.isna(date):
            calendar[week] = date
                
    return render_template("calendar.html", calendar=calendar, year=year, associate=associate)

if __name__ == "__main__":
    app.run()
