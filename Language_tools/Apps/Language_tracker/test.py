# %%
import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute("PRAGMA table_info(milestones)")
data = c.fetchall()[0]

# %%
len(data)
# %%
print(data)
# 

# %%
c.execute('SELECT a1 FROM milestones WHERE rowid = 0')
result = c.fetchone()
# %%
import pandas as pd
table = pd.read_sql_query("SELECT * FROM milestones", conn)


# %%
table.head()
# %%
