import os.path
from typing import Optional, List, Union
import logging

import uuid

from member import LibraryMember

logger = logging.getLogger()


class LibraryMemberStorage:

    def __init__(self, filename):
        self.filename = filename

    def save_members(self, members: List[LibraryMember]):
        with open(self.filename, 'w') as f:
            for member in members:
                f.write(repr(member))

    def save_member_profile(self, member: LibraryMember):
        with open(self.filename, 'a') as f:
            f.write(repr(member))
            print("Member successfully added to the database")

    def load_members(self) -> List[LibraryMember]:
        if os.path.exists(self.filename):
            with open(self.filename) as f:
                # excluding first line as it acts as a header
                lines = f.read().splitlines()[1:]
                return [LibraryMember(*member_profile.split('\t')) for member_profile in lines]
        else:
            return list()


class MemberProfileManager:

    def __init__(self, database_path: str):
        self._storage = LibraryMemberStorage(database_path)
        self._members = self._storage.load_members()
        self._existing_member_ids = set(member.get_member_id() for member in self._members)

    def add_new_member(self,
                       name: str,
                       address: str,
                       phone_number: str,
                       email: str,
                       age: str,
                       occupation: str):
        ''' Προσθηκη νέου μέλους '''
        member_id = self.generate_member_id()
        status = self.set_member_status(active=True)
        member = LibraryMember(member_id, name, address, phone_number, email, age, occupation, status)

        self._existing_member_ids.add(member_id)
        self._members.append(member)
        self._storage.save_members(self._members)

        return member

    def update_member_profile(self, member_id: str):
        """Επικαιροποίηση στοιχείων μελών"""
        # load member profile
        member_profile = self.get_member_profile_by_id(member_id)
        # set the new member details
        ## προσομοίωση με front end


    def renew_membership(self, member_id: LibraryMember):
        """Ανανέωση εγγραφής μέλους"""
        # renew the members subsription
        status = MemberProfileManager.set_member_status(active=True)
        pass

    def pause_membership(self, member: LibraryMember):
        """Διακοπή εγγραφής μέλους"""
        status = MemberProfileManager.set_member_status(active=False)
        pass

    def get_member_profile_by_id(self, member_id: str):
        if member_id is None:
            return None

        for member_profile in self._members:
            if member_profile.get_member_id() == member_id:
                return member_profile

    def generate_member_id(self):
        # generates random member id
        member_id = str(uuid.uuid4())
        while self.member_id_exists(member_id):
            member_id = str(uuid.uuid4())

        return member_id

    @staticmethod
    def set_member_status(active: bool):
        return "active" if active else "inactive"

    def member_id_exists(self, member_id):
        return member_id in self._existing_member_ids




if __name__ == "__main__":
    #### Εισαγωγή δεδομένων στις αρχικές δομές
    filename = "members.txt"
    member_profile_manager = MemberProfileManager(filename)

    while True:

        print("Επιλογές")
        print("========")
        print("1. Προσθήκη νέου μέλους, ", end="")
        print("2. Επικαιροποίηση στοιχείων μέλους, ", end="")
        print("3. Ανανέωση εγγραφής μέλους, ", end="")
        print("4. Διακοπή εγγραφής μέλους", end="")
        choice = input("Εισάγετε την επιλογή σας:")
        if choice == "1":
            member_profile_manager.add_new_member()
        elif choice == "2":
            member_profile_manager.update_member_profile()
        elif choice == "3":
            member_profile_manager.renew_membership()
        elif choice == "4":
            member_profile_manager.pause_membership()
            break
        else:
            print("Παρακαλώ εισάγετε έγκυρη επιλογή")














