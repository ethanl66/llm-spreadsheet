import pandas as pd
import sqlite3
import os

def map_dtype_to_sqlite(dtype):
	if pd.api.types.is_integer_dtype(dtype):
		return 'INTEGER'
	elif pd.api.types.is_float_dtype(dtype):
		return 'REAL'
	elif pd.api.types.is_string_dtype(dtype):
		return 'TEXT'
	elif pd.api.types.is_bool_dtype(dtype):
		return 'BOOLEAN'
	elif pd.api.types.is_datetime64_any_dtype(dtype):
		return 'DATETIME'
	elif pd.api.types.is_timedelta64_dtype(dtype):
		return 'TIME'
	elif pd.api.types.is_object_dtype(dtype):
		return 'BLOB'
	else:
		raise ValueError(f"Unsupported dtype: {dtype}")
	
def create_table_from_csv (csv_file, db_file):
	
	conn = sqlite3.connect(db_file)
	cur = conn.cursor()

	# Load CSV into pandas df
	df = pd.read_csv('step1.csv')

	# Inspect column names and data types in the CSV file
	table_name = csv_file.split('.')[0]
	columns = []
	for col, dtype in df.dtypes.items():
		sqlite_type = map_dtype_to_sqlite(dtype)
		columns.append(f"{col} {sqlite_type}")
		# make id columns PRIMARY KEY?

	# Execute create table
	create_table_stmt = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
	cur.execute(create_table_stmt)
	conn.commit()

	# Append rows of df data to the table
	df.to_sql(table_name, conn, if_exists='append', index=False)
	conn.commit()
		
	conn.close()


create_table_from_csv('step1.csv', 'step2.db')

# Test if the table is created correctly
conn = sqlite3.connect('step2.db')
cur = conn.cursor()

cur.execute('SELECT * FROM step1')
rows = cur.fetchall()
assert rows == [
	(1, 'John Doe', 28), 
	(2, 'Jane Smith', 34), 
	(3, 'Emily Johnson', 22),
	(4, 'Michael Brown', 45),
	(5, 'Sarah Davis', 30)
], "FAILED: Data loaded incorrectly"
print("PASS: Data loaded correctly")
