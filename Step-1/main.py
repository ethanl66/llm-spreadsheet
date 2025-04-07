import sqlite3
import pandas as pd
import os

# Manually create table in sqlite
conn = sqlite3.connect('step1.db')
cur = conn.cursor()

# Manually create csv file
# Delete the file if it exists
try:
	os.remove('step1.csv')
except OSError:
	pass
with open('step1.csv', 'w') as f:
	f.write('id,name,age\n')
	f.write('1,John Doe,28\n')
	f.write('2,Jane Smith,34\n')
	f.write('3,Emily Johnson,22\n')
	f.write('4,Michael Brown,45\n')
	f.write('5,Sarah Davis,30\n')

# Prototype table
cur.execute('''
	CREATE TABLE IF NOT EXISTS step1 (
		id INTEGER PRIMARY KEY,
		name TEXT NOT NULL,
		age INTEGER NOT NULL
	);
''')
conn.commit()
# clear table if it exists
cur.execute('DROP TABLE IF EXISTS step1')
conn.commit()


# Use pandas to load data from csv to pandaas dataframe
df = pd.read_csv('step1.csv')

# append data from df to sqlite table
df.to_sql('step1', conn, if_exists = 'append', index = False)	
conn.commit()

# Run basic queries to check if data is loaded correctly
cur.execute('SELECT * FROM step1')
rows = cur.fetchall()
""" for row in rows:
	print(row) """
assert rows == [
	(1, 'John Doe', 28), 
	(2, 'Jane Smith', 34), 
	(3, 'Emily Johnson', 22),
	(4, 'Michael Brown', 45),
	(5, 'Sarah Davis', 30)
], "FAILED: Data loaded incorrectly"
print("PASS: Data loaded correctly")
