# Chat-Based Spreadsheet Application

This project is a chat-based spreadsheet application that allows users to interact with a SQLite database using natural language queries. The application dynamically loads CSV files into the database, resolves schema conflicts, and uses OpenAI's ChatGPT to generate SQL queries from user input.

## Features

1. **Load CSV Files into SQLite**:
   - Automatically creates SQLite tables from CSV files.
   - Handles schema conflicts (overwrite, rename, append, or skip).

2. **Interactive Assistant**:
   - Provides a command-line interface (CLI) for users to:
     - Load CSV files into the database.
     - List available tables in the database.
     - Run custom SQL queries using natural language.

3. **ChatGPT Integration**:
   - Converts natural language queries into SQL statements.
   - Executes the generated SQL queries and displays results.

4. **Error Logging**:
   - Logs errors to `error.log` for debugging.

## Prerequisites

- Python 3.7 or higher
- SQLite
- Required Python libraries:
  - `pandas`
  - `openai`

## Files and Folders
### Updated program files are in the `Step-2` folder:
- `main.py`: The main program file.
- `step1.csv`: Sample CSV file used for testing.
- `step4.db`: SQLite database file.
- `error.log`: Log file for errors encountered during execution.
