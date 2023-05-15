import os.path
import sqlite3
from sqlite3 import Error
from typing import List, Optional

DB_FILE_PATH = './library.db'
MEMBER_FILE_PATH = './library_db/members.txt'


def read_members_from_txt(txt_file_path: str, header=True) -> List[tuple]:
    if not os.path.exists(txt_file_path):
        raise Exception(f"Το αρχείο: {txt_file_path} δεν βρέθηκε")

    with open(txt_file_path) as f:
        lines = f.read().splitlines()
        # excluding first line as it acts as a header
        if header:
            lines = lines[1:]

        return [tuple(member_profile.split('\t')) for member_profile in lines]


def insert_data_into_table(member_data: List[tuple], db_file_path: Optional[str] = None):

    if db_file_path is None:
        db_file_path = DB_FILE_PATH
        print(f"Defaulting to database: {DB_FILE_PATH}")

    spl_query_base = "INSERT INTO MEMBERS" \
                     "(member_id, name, address, phone_number, email, age, occupation, status)" \
                     "VALUES"

    try:
        with sqlite3.connect(db_file_path) as conn:
            cursor = conn.cursor()
            for member in member_data:
                sql_query = f"{spl_query_base} {member}"
                cursor.execute(sql_query)
            print(f"Επιτυχής προσθήκη {len(member_data)} μελών στην βάση δεδομένων")
    except Error as e:
        print(f'Η προσθήκη μελών στην βάση δεδομένων απέτυχε: {e}')


if __name__ == '__main__':
    members = read_members_from_txt(MEMBER_FILE_PATH)
    insert_data_into_table(members)
