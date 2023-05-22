import sqlite3
from typing import List


def insert_data_into_table(db_file_path: str, data: List[tuple], table_name: str, columns: tuple):

    spl_query_base = f"INSERT INTO {table_name} {columns} VALUES"

    try:
        with sqlite3.connect(db_file_path) as conn:
            cursor = conn.cursor()
            for entry in data:
                sql_query = f"{spl_query_base} {entry}"
                cursor.execute(sql_query)
            print(f"Added {len(data)} entries to table: {table_name}")
    except sqlite3.Error as e:
        print(f'Failed to add entries to table {table_name}: {e}')
