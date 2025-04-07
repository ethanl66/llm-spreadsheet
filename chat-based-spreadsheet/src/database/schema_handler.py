def inspect_table_schema(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    schema_info = cursor.fetchall()
    return schema_info

def create_table_from_csv(connection, csv_file_path, table_name):
    import pandas as pd

    df = pd.read_csv(csv_file_path)
    columns = df.columns
    dtypes = df.dtypes

    sql_types = {
        'object': 'TEXT',
        'int64': 'INTEGER',
        'float64': 'REAL',
        'bool': 'BOOLEAN',
        'datetime64[ns]': 'DATETIME'
    }

    columns_with_types = []
    for col, dtype in zip(columns, dtypes):
        sql_type = sql_types.get(str(dtype), 'TEXT')
        columns_with_types.append(f"{col} {sql_type}")

    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns_with_types)});"
    cursor = connection.cursor()
    cursor.execute(create_table_sql)
    connection.commit()

def handle_schema_conflict(connection, table_name, new_schema):
    existing_schema = inspect_table_schema(connection, table_name)

    if existing_schema:
        print(f"Schema conflict detected for table '{table_name}'.")
        print("Existing schema:", existing_schema)
        print("New schema:", new_schema)

        choice = input("Choose an action: (O)verwrite, (R)ename, (S)kip: ").strip().upper()
        if choice == 'O':
            cursor = connection.cursor()
            cursor.execute(f"DROP TABLE {table_name};")
            connection.commit()
            return True  # Indicate that the table should be recreated
        elif choice == 'R':
            new_table_name = input("Enter new table name: ").strip()
            return new_table_name
        elif choice == 'S':
            return None  # Indicate to skip the creation
    return True  # No conflict, proceed with creation