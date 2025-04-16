"""
LLM PROMPT:
MUST EDIT THE PROMPT WITH THE CORRECT DESCRIPTION OF THE DATABASE
"""

print("Starting...")
import pandas as pd
import sqlite3
import os
import logging
from openai import OpenAI

table_to_open = 'step1'

# Configure logging to log errors to a file
logging.basicConfig(filename='error.log', level=logging.ERROR, 
	format='%(asctime)s:%(levelname)s:%(message)s')

def handle_schema_conflict(cur, table_name, columns):

	append = False

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
			print(f"Creating new table '{table_name}'...")
		elif action == 'c':
			new_table_name = input(f"Enter new name for the table: ").strip()
			print(f"Creating new table '{new_table_name}'...")
			# cur.execute(f"CREATE TABLE {new_table_name} ({', '.join(columns)});")
			return new_table_name, append
		elif action == 'a':
			print(f"Appending data to existing table '{table_name}'...")
			append = True
			# Append data to existing table
			# df.to_sql(table_name, conn, if_exists='append', index=False)
		elif action == 's':
			print(f"Skipping table '{table_name}'...")
			return None, append
		else:
			print("Invalid action. Skipping table creation.")
			return None, append
	return table_name, append


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
		table_name, append = handle_schema_conflict(cur, table_name, columns)
		# append: Set to overwrite vs append (CREATE TABLE vs CREATE TABLE IF NOT EXISTS)
		if table_name is None:
			conn.close()	
			return

		# Execute create table
		if append:
			create_table_stmt = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
		elif not append:
			create_table_stmt = f"CREATE TABLE {table_name} ({', '.join(columns)});"
		cur.execute(create_table_stmt)
		conn.commit()

		# Append rows of df data to the table
		df.to_sql(table_name, conn, if_exists='append', index=False)
		conn.commit()
	except Exception as e:
		logging.error(f"Error processing file {csv_file}: {e}")
		print(f"Error processing file {csv_file}: {e}")
		table_name = None
	finally:
		conn.close()
		return table_name
	
def list_tables(conn):
	cur = conn.cursor()
	cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
	tables = cur.fetchall()
	if tables:
		print("Available tables:")
		for table in tables:
			print(f"{table[0]}:")
			# Print table
			cur.execute(f"SELECT * FROM {table[0]} LIMIT 10;")
			rows = cur.fetchall()
			#print(f"Sample data from {table[0]}:")
			for row in rows:
				print(row)
	else:
		print("No tables found in the database.")

def get_tables(conn):
	cur = conn.cursor()
	# Get schema of all tables in the database
	cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
	tables = cur.fetchall()

	if not tables:
		print("No tables found in the database.")
		return None
	
	#print("Available tables:")
	schema = ""
	for table in tables:
		table_name = table[0]
		schema += f"\nTable: {table_name}\n"
		schema += "Columns:\n"

		# Get table columns
		cur.execute(f"PRAGMA table_info({table_name});")
		columns = cur.fetchall()
		for col in columns:
			schema += f" - {col[1]}: {col[2]}\n"

		# Get table data
		schema += "Sample Data:\n"
		cur.execute(f"SELECT * FROM {table_name} LIMIT 25;")
		rows = cur.fetchall()
		for row in rows:
			schema += f" - {row}\n"
		schema += "\n"

	#print(schema)
	return schema

def run_sql_query(conn):
	try:
		# Get natural language query from user
		user_query = input("Enter your query: ").strip()

		# Define prompt for ChatGPT

		#- sales (sale_id, product_id, quantity, sale_date, revenue)
        #- products (product_id, product_name, category, price)
        #- employees (employee_id, name, department, hire_date)
        #- customers (customer_id, customer_name, location)

		client = OpenAI(
			# This is the default and can be omitted
			api_key=os.environ.get("OPENAI_API_KEY"),
		)

		schema = get_tables(conn)

		prompt = f"""
		You are an AI assistant tasked with converting user queries into SQL statements. 
        The database uses SQLite and contains the following schema:
		"{schema}"

		User Query: "{user_query}"

		Your task is to:
        1. Generate a 1-line SQL query that accurately answers the user's question.
        2. Ensure the SQL is compatible with SQLite syntax.
        3. Provide a short comment explaining what the query does.

        Output Format:
        - SQL Query
        - Explanation
		"""

		# Send prompt to ChatGPT
		response = client.responses.create(
			model="gpt-4o",
			input=prompt,
			temperature=0.6,
			#max_tokens=1500
		)

		# Extract the generated SQL query and explanation from the response
		#print(f"Response:\n{response}\n")
		response_text = response.output_text
		#print("\nChatGPT Response:")
		#print(response_text)

		# Parse SQL query and explanation from the response
		lines = response_text.split('\n')
		sql_query = lines[1].strip()

		# Execute the SQL query
		#print("\nExecuting SQL query...")
		#print(f"SQL Query: {sql_query}")
		#print("Explanation:")
		#for line in lines[1:]:
			#print(line.strip())
		# Execute the SQL query
				
		#query = input("Enter SQL query: ").strip()
		cur = conn.cursor()
		cur.execute(sql_query)
		if sql_query.lower().startswith("select"):
			rows = cur.fetchall()
			#print("SQL query results:")
			for row in rows:
				print(row)
		else:
			conn.commit()
			print("SQL query executed successfully.")
	except Exception as e:
		logging.error(f"Error executing SQL query: {e}")
		print(f"Error executing SQL query: {e}")

def interactive_assistant():
	db_file = 'step4.db'
	conn = sqlite3.connect(db_file)

	while True:
		print("\nOptions:")
		print("1. Load a CSV file into the database")
		print("2. List available tables in the database")
		print("3. Run a custom query")
		print("4. Exit")
		choice = input("Choose an option (1-4): ").strip()

		if choice == '1':
			try:
				csv_file = input("Enter the name of the CSV file: ").strip()
				if csv_file.endswith('.csv'):
					csv_file = csv_file[:-4]
				table_name = create_table_from_csv(csv_file + '.csv', db_file)
				if table_name is None:
					print("No table created. Exiting.")
					exit()

				# Test if the table is created correctly
				#conn = sqlite3.connect(db_to_load_into)
				cur = conn.cursor()

				cur.execute(f'SELECT * FROM {table_name}')
				rows = cur.fetchall()
				print(table_name + ":")
				print(rows)
				""" assert rows == [
					(1, 'John Doe', 28), 
					(2, 'Jane Smith', 34), 
					(3, 'Emily Johnson', 22),
					(4, 'Michael Brown', 45),
					(5, 'Sarah Davis', 30)
				], "FAILED: Data loaded incorrectly"
				print("PASS: Data loaded correctly") """
			except Exception as e:
				logging.error(f"Error: {e}")
				print(f"Error: {e}")
		elif choice == '2':
			list_tables(conn)
		elif choice == '3':
			run_sql_query(conn)
		elif choice == '4':
			print("Exiting...")
			break
		else:
			print("Invalid choice. Please try again.")
	
	conn.close()


if __name__ == "__main__":
	interactive_assistant()


""" Step 3 old
try:
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
	print(table_name + ":")
	print(rows)
	
except Exception as e:
	logging.error(f"Error: {e}")
	print(f"Error: {e}") """