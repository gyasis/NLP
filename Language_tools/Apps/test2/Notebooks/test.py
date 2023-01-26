# %%
import pandas as pd
from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import plotly.express as px



# %%
conn = sqlite3.connect('../test.db')
c = conn.cursor()
c.execute("SELECT SUM(hours) FROM test")
total_hours = c.fetchone()[0]
now = datetime.now()
# %%
c.execute("SELECT a1, a2, b1, b2 FROM milestones ORDER BY ABS(strftime('%s', a1) - strftime('%s', ?)) LIMIT 1", (now,))
milestone_dates = c.fetchone()
closest_milestone = milestone_dates
# %%
from dateutil import parser
from datetime import timedelta
# %% 
#This won't take into account already passed milestones
# closest_milestone = min(closest_milestone, key=lambda x: abs(parser.parse(x)-now) )
# %%
#This ignores passed milestones
closest_milestone = min(filter(lambda x: (parser.parse(x) - now) >= timedelta(0), closest_milestone), key=lambda x: (parser.parse(x) - now))

# %%
days_until_milestone = (parser.parse(closest_milestone) - now).days

# %% 
milestone_names = ['A1', 'A2', 'B1', 'B2']
# create a dataframe with the milestone names and the milestone dates
df = pd.DataFrame({'milestone':milestone_names, 'date':milestone_dates})