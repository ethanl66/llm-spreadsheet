import sqlite3
from src.utils.csv_loader import load_csv_to_db
from src.database.schema_handler import inspect_schema, handle_schema_conflict
from src.ai.query_generator import QueryGenerator
from src.utils.logger import log_error

def interactive_chat():
    print("Welcome to the Chat-Based Spreadsheet Application!")
    print("You can load CSV files, run SQL queries, or type 'exit' to quit.")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("Exiting the application. Goodbye!")
            break

        elif user_input.startswith("load csv "):
            csv_file = user_input.split("load csv ")[1]
            try:
                load_csv_to_db(csv_file)
                print(f"Successfully loaded {csv_file} into the database.")
            except Exception as e:
                log_error(f"Error loading CSV: {e}")
                print("An error occurred while loading the CSV file.")

        elif user_input.startswith("run query "):
            query = user_input.split("run query ")[1]
            try:
                # Assuming there's a function to execute the query and return results
                results = execute_query(query)  # This function needs to be defined
                print("Query Results:", results)
            except Exception as e:
                log_error(f"Error executing query: {e}")
                print("An error occurred while executing the query.")

        elif user_input == "list tables":
            try:
                tables = inspect_schema()
                print("Tables in the database:", tables)
            except Exception as e:
                log_error(f"Error listing tables: {e}")
                print("An error occurred while listing the tables.")

        else:
            print("Sorry, I didn't understand that. Please try again.")

if __name__ == "__main__":
    interactive_chat()