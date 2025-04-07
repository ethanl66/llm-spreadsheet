import pandas as pd
import sqlite3
import os
import logging

table_to_open = 'step1'

# Configure logging to log errors to a file
logging.basicConfig(filename='error.log', level=logging.ERROR, 
	format='%(asctime)s:%(levelname)s:%(message)s')

def handle_schema_conflict(cur, table_name, columns):
	# Check existing table schema
	cur.execute(f"PRAGMA table_info({table_name})")
	existing_schema = cur.fetchall()

	if existing_schema:
		print(f"Table '{table_name}' already exists with the following schema:")
		for col in existing_schema:
			print(f" - {col[1]}: {col[2]}")

		#Prompt user for action
		action = input("Schema conflict detected. Choose an action: [O]verwrite, [R]ename, [C]hoose new name, [A]ppend, [S]kip: ").strip().lower()
		if action == 'o':
			print(f"Overwriting table '{table_name}'...")
			cur.execute(f"DROP TABLE IF EXISTS {table_name}")
			# cur.execute(f"CREATE TABLE {table_name} ({', '.join(columns)});")
		elif action == 'r':
			new_table_name = input(f"Renaming '{table_name}': Enter new table name: ").strip()
			print(f"Renaming table to '{new_table_name}'...")
			cur.execute(f"ALTER TABLE {table_name} RENAME TO {new_table_name}")
			return new_table_name
		elif action == 'c':
			new_table_name = input(f"Enter new name for the table: ").strip()
			print(f"Creating new table '{new_table_name}'...")
			# cur.execute(f"CREATE TABLE {new_table_name} ({', '.join(columns)});")
			return new_table_name
		elif action == 'a':
			print(f"Appending data to existing table '{table_name}'...")
			# Append data to existing table
			# df.to_sql(table_name, conn, if_exists='append', index=False)
		elif action == 's':
			print(f"Skipping table '{table_name}'...")
			return None
		else:
			print("Invalid action. Skipping table creation.")
			return None
	return table_name


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

	try:
		# Load CSV into pandas df
		df = pd.read_csv(csv_file)

		# Inspect column names and data types in the CSV file
		table_name = csv_file.split('.')[0]
		columns = []
		for col, dtype in df.dtypes.items():
			sqlite_type = map_dtype_to_sqlite(dtype)
			columns.append(f"{col} {sqlite_type}")
			# make id columns PRIMARY KEY?

		# Handle schema conflicts
		table_name = handle_schema_conflict(cur, table_name, columns)
		if table_name is None:
			conn.close()	
			return

		# Execute create table
		create_table_stmt = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
		cur.execute(create_table_stmt)
		conn.commit()

		# Append rows of df data to the table
		df.to_sql(table_name, conn, if_exists='append', index=False)
		conn.commit()
	except Exception as e:
		logging.error(f"Error processing file {csv_file}: {e}")
		print(f"Error processing file {csv_file}: {e}")

	finally:
		conn.close()
		return table_name



csv_file_to_load = input("Name of csv file to load into database: ")
if csv_file_to_load.endswith('.csv'):
	csv_file_to_load = csv_file_to_load[:-4]
db_to_load_into = 'step3.db'

table_name = create_table_from_csv(csv_file_to_load + '.csv', db_to_load_into)
if table_name is None:
	print("No table created. Exiting.")
	exit()

# Test if the table is created correctly
conn = sqlite3.connect(db_to_load_into)
cur = conn.cursor()

cur.execute(f'SELECT * FROM {table_name}')
rows = cur.fetchall()
# print(rows)
assert rows == [
	(1, 'John Doe', 28), 
	(2, 'Jane Smith', 34), 
	(3, 'Emily Johnson', 22),
	(4, 'Michael Brown', 45),
	(5, 'Sarah Davis', 30)
], "FAILED: Data loaded incorrectly"
print("PASS: Data loaded correctly")
