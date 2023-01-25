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
# %%
now = datetime.now()
# %%
c.execute("SELECT a1, a2, b1, b2 FROM milestones ORDER BY ABS(strftime('%s', a1) - strftime('%s', ?)) LIMIT 1", (now,))
closest_milestone = c.fetchone()
# %%
from dateutil import parser

# %% 

closest_milestone = min(closest_milestone, key=lambda x: abs(parser.parse(x)-now) )
# %%


days_until_milestone = (closest_milestone - now).days
# %%
