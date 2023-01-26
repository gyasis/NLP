# %%
import sqlite3
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# %%
# Add the new columns
cursor.execute("ALTER TABLE test ADD COLUMN tags TEXT DEFAULT 'Uncategorized'")
conn.commit()
# %%
cursor.execute("ALTER TABLE test ADD COLUMN notes TEXT")
conn.commit()
# %%
cursor.execute("ALTER TABLE test ADD CHECK (tags in ('structured learning', 'exposure', 'memorization', 'Uncategorized'))")

# %%
cursor.execute("PRAGMA table_info(test)")

# %%
tables = cursor.fetchall()

# %%
num_tables = len(tables)
print(f'There are {num_tables} tables in the test.db database.')
# %%
# Save the changes
conn.commit()

# Close the connection
conn.close()
