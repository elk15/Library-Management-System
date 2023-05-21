from typing import List, Optional

from members.member import LibraryMember

import sqlite3
from sqlite3 import Cursor

PATH_TO_LIBRARY_DB = './library.db'


class MemberStorage:
    """
    Class for storing and managing member profiles in a database.

    Attributes:
        path_to_db (str): The path of the database file.
    """

    def __init__(self, path_to_db: Optional[str] = None):
        path_to_db = path_to_db if path_to_db is not None else PATH_TO_LIBRARY_DB
        self.path_to_db = path_to_db

    def save_member(self, member: LibraryMember) -> None:
        """
        Saves a new member profile in the database after checking for duplicates.

        The method checks if another member with the same name and email already exists in the database.
        If a duplicate is found, the member profile is not saved.
        """

        member_name = member.get_name()
        member_email = member.get_email()
        member_attributes = tuple(vars(member).values())

        spl_query_base = "INSERT INTO MEMBERS" \
                         "(member_id, name, address, phone_number, email, age, occupation, status)" \
                         "VALUES"
        try:
            with sqlite3.connect(self.path_to_db) as conn:
                cursor = conn.cursor()

                if self.member_already_exists_in_db(cursor, member_name, member_email):
                    print(f'Member with name: {member_name}, and email: {member_email} already exists')
                    return None

                sql_query = f"{spl_query_base} {member_attributes}"
                cursor.execute(sql_query)
                print(f"Member was successfully added to the library database")

        except sqlite3.Error as e:
            print(f'Failed to save member to the database: {e}')
            return None

    def update_member_entry(self, member: LibraryMember) -> None:
        """
        Update the entry of a member in the library database

        The method updates the profile of a member in the library database
        based on the provided new profile information.
        """
        member_attributes_copy = vars(member).copy()
        member_id = member_attributes_copy.pop('_member_id')

        columns = ", ".join([f'{key.strip("_")} = ?'for key in member_attributes_copy.keys()])
        values = tuple(member_attributes_copy.values())

        try:
            with sqlite3.connect(self.path_to_db) as conn:
                cursor = conn.cursor()

                cursor.execute(f"UPDATE members SET {columns} WHERE member_id = {member_id}", values)
                print(f"Member entry was updated in the database")

        except sqlite3.Error as e:
            print(f'Failed to update database entry: {e}')

    def load_member_by_id(self, member_id: int) -> Optional[LibraryMember]:
        """
        Load a member's profile based on their ID from the library database.

        The method retrieves and returns the profile of a member with the specified ID from the library database.
        """

        try:
            with sqlite3.connect(self.path_to_db) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM members WHERE member_id={member_id}")
                results = cursor.fetchall()
        except sqlite3.Error as e:
            print(f'Failed to retrieve member with member id: {member_id} from the database: {e}')
            return None

        member_profile = self.validate_single_member_result(results, member_id)
        return member_profile

    def load_members(self) -> List[LibraryMember]:
        """
        Load all the member profiles from the library database.
        """
        try:
            with sqlite3.connect(self.path_to_db) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM MEMBERS")
                rows = cursor.fetchall()
                member_profiles = [LibraryMember(*row) for row in rows]
                return member_profiles
        except sqlite3.Error as err:
            print("Error: ", err)
            return list()

    @staticmethod
    def member_already_exists_in_db(cursor: Cursor, member_name: str, member_email: str):
        """
        Check if a member with the given name and email already exists in the database
        """
        sql_query = f"SELECT EXISTS(SELECT 1 FROM MEMBERS WHERE name = ? AND email = ?)"
        cursor.execute(sql_query, (member_name, member_email))
        result = cursor.fetchone()[0]
        return result

    @staticmethod
    def validate_single_member_result(results: list, member_id: int) -> Optional[LibraryMember]:
        """
        Validate a single member result extracted from the database.

        The method checks if the extracted results correspond to exactly one member profile in the database.
        """
        num_found_members = len(results)
        if num_found_members < 1:
            print(f"Member with ID {member_id} was not found in the library database.")
            return None
        elif num_found_members > 1:
            raise ValueError(f"{num_found_members} entries with the same id were found in the database.")
        else:
            return LibraryMember(*results[0])



