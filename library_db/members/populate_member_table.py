import os.path
from typing import List, Optional

from library_db.common import insert_data_into_table

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


if __name__ == '__main__':
    library_db_file_path = 'library.db'
    table_name = 'members'
    columns = ('member_id', 'name', 'address', 'phone_number', 'email', 'age', 'occupation', 'status')

    members = read_members_from_txt(MEMBER_FILE_PATH)
    insert_data_into_table(library_db_file_path, members, table_name, columns)
