import sqlite3
import pandas as pd
from src.database.db_manager import DbManager
from src.cli.interactive_chat import start_chat

def main():
    # Initialize database connection
    db_manager = DbManager('chat_based_spreadsheet.db')
    
    # Start the interactive chat
    start_chat(db_manager)

if __name__ == "__main__":
    main()