from typing import List, Optional

from member import LibraryMember

import sqlite3
from sqlite3 import Cursor


class MemberStorage:

    def __init__(self, filename):
        self.filename = filename

    def save_member(self, member: LibraryMember) -> None:

        member_name = member.get_name()
        member_email = member.get_email()
        member_attributes = tuple(vars(member).values())

        spl_query_base = "INSERT INTO MEMBERS" \
                         "(member_id, name, address, phone_number, email, age, occupation, status)" \
                         "VALUES"
        try:
            with sqlite3.connect(self.filename) as conn:
                cursor = conn.cursor()

                if self.member_already_exists(cursor, member_name, member_email):
                    print(f'Member with name: {member_name}, and email: {member_email} already exists')
                    return None

                sql_query = f"{spl_query_base} {member_attributes}"
                cursor.execute(sql_query)
                print(f"Member was successfully added to the database")

        except sqlite3.Error as e:
            print(f'Failed to save member to the database: {e}')
            return None

    def update_member_entry(self, member: LibraryMember) -> None:
        member_attributes_copy = vars(member).copy()
        member_id = member_attributes_copy.pop('_member_id')
        columns = ", ".join([f'{key.strip("_")} = ?'for key in member_attributes_copy.keys()])
        values = tuple(member_attributes_copy.values())

        try:
            with sqlite3.connect(self.filename) as conn:
                cursor = conn.cursor()

                cursor.execute(f"UPDATE members SET {columns} WHERE member_id = {member_id}", values)
                print(f"Member entry was updated in the database")

        except sqlite3.Error as e:
            print(f'Failed to update database entry: {e}')

    def load_member_by_id(self, member_id: str) -> Optional[LibraryMember]:
        sql_query = f"SELECT * FROM members WHERE member_id={member_id}"
        try:
            with sqlite3.connect(self.filename) as conn:
                cursor = conn.cursor()
                cursor.execute(sql_query)
                results = cursor.fetchall()
        except sqlite3.Error as e:
            print(f'Failed to retrieve member with member id: {member_id} from the database: {e}')
            return None

        assert len(results) == 1, f"{len(results)} entries with the same id were found in the database"
        member_profile = LibraryMember(*results[0])
        return member_profile

    def load_members(self) -> List[LibraryMember]:
        sql = "SELECT * FROM MEMBERS"
        try:
            with sqlite3.connect(self.filename) as conn:
                cursor = conn.cursor()
                cursor.execute(sql)
                rows = cursor.fetchall()
                member_profiles = [LibraryMember(*row) for row in rows]
                return member_profiles
        except sqlite3.Error as err:
            print("Error: ", err)
            return list()

    @staticmethod
    def member_already_exists(cursor: Cursor, member_name: str, member_email: str):
        sql_query = f"SELECT EXISTS(SELECT 1 FROM MEMBERS WHERE name = ? AND email = ?)"
        cursor.execute(sql_query, (member_name, member_email))
        result = cursor.fetchone()[0]
        return result



