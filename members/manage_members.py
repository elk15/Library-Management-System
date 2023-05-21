from typing import Optional, Union, Callable

from members.member_storage import MemberStorage
from members.member import LibraryMember


def get_member_id(member_id_exists: Callable) -> Optional[int]:
    """
    Prompt the user to enter a member ID and validate it.

    This function prompts the user to provide a member ID and performs validation to ensure its correctness.
    The entered member ID is used to identify a specific member in the system.
    """

    while True:
        member_id = input("Enter Member id (contains only digits) or press ENTER to exit: ")

        if not member_id:
            return None
        elif not member_id.isdigit():
            print("Invalid member id. Member ids are non negative integers")
        elif member_id_exists(int(member_id)):
            return int(member_id)


class MemberManager:
    """
    Class for managing members in the library.

    This class provides functionality for managing members, including adding new members to the library.

    """
    def __init__(self):
        self._storage = MemberStorage()

        self._members = self._storage.load_members()
        if not self._members:
            raise Exception("Failed to load members from the database")

        self._existing_member_ids = set(member.get_member_id() for member in self._members)

    def add_new_member(self, name: str, address: str, phone_number: str, email: str, age: str,
                       occupation: str) -> Optional[LibraryMember]:
        """
        Create a new member profile and save it in the library database.
        """
        member = LibraryMember(name=name, address=address, phone_number=phone_number, email=email, age=age,
                               occupation=occupation)

        member_id = self._generate_member_id()
        status = self.get_member_status(active=True)

        member.set_member_id(member_id)
        member.set_status(status)
        print(f"New member successfully created with id: {member_id}")

        self._members.append(member)
        self._existing_member_ids.add(member_id)
        self._storage.save_member(member)

        return member

    def _generate_member_id(self) -> int:
        """
        Generate a new member ID by incrementing the largest ID in the database by 1.

        This function generates a unique member ID for a new member by retrieving the largest ID in the database,
        incrementing it by 1, and returning the new ID.
        """
        max_member_id = self._get_max_member_id()
        return max_member_id + 1

    def _get_max_member_id(self) -> int:
        member_prof = max(self._members, key=lambda x: x.get_member_id())
        return member_prof.get_member_id()

    @staticmethod
    def get_member_status(active: bool) -> str:
        return "Active" if active else "Inactive"
