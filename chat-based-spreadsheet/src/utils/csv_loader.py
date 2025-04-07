import pandas as pd
import sqlite3
import os

def load_csv_to_dataframe(csv_file):
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"The file {csv_file} does not exist.")
    return pd.read_csv(csv_file)

def insert_dataframe_to_sqlite(df, table_name, conn):
    df.to_sql(table_name, conn, if_exists='append', index=False)

def load_csv_to_sqlite(csv_file, db_file, table_name):
    conn = sqlite3.connect(db_file)
    try:
        df = load_csv_to_dataframe(csv_file)
        insert_dataframe_to_sqlite(df, table_name, conn)
    finally:
        conn.close()