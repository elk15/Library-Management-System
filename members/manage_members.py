from typing import Optional

from members.member_storage import MemberStorage
from members.member import LibraryMember


class MemberManager:

    def __init__(self, database_path: str):
        self._storage = MemberStorage(database_path)

        self._members = self._storage.load_members()
        if not self._members:
            raise Exception("Failed to load members from the database")

        self._existing_member_ids = set(member.get_member_id() for member in self._members)

    def add_new_member(self):
        member_required_fields = ['name', 'address', 'phone_number', 'email', 'age', 'occupation']
        member = LibraryMember()

        for field in member_required_fields:
            self.add_member_details(field, member)

        member_id = self.generate_member_id()
        status = self.get_member_status(active=True)

        member.set_member_id(member_id)
        member.set_status(status)
        print(f"New member successfully created with id: {member_id}")

        self._members.append(member)
        self._existing_member_ids.add(member_id)
        self._storage.save_member(member)

        return member

    def update_member_profile(self):

        member_id = self.get_member_id()
        if member_id is None:
            return None

        member_profile = self.get_member_profile_by_id(member_id)
        if not member_profile:
            return None

        while True:
            # TODO: προσθήκη κατάστασης συνδρομής στις επιλογές?
            choice = input(f"Which field would you like to update?\n"
                           f"1. Member profile, 2. Address, 3. Phone number, 4. Email, "
                           f"5. Age, 6. Occupation (press enter for exit):")
            if not choice:
                print("Exit")
                break
            elif choice == "1":
                self.update_member_details('member name', member_profile)
            elif choice == "2":
                self.update_member_details('address', member_profile)
            elif choice == "3":
                self.update_member_details('phone_number', member_profile)
            elif choice == "4":
                self.update_member_details('email', member_profile)
            elif choice == "5":
                self.update_member_details('age', member_profile)
            elif choice == "6":
                self.update_member_details('occupation', member_profile)
            else:
                print("Invalid choice. Please choose a number from 1-6")

        self._storage.update_member_entry(member_profile)

    def manage_membership(self, renew: bool) -> None:

        member_id = self.get_member_id()
        if member_id is None:
            return None

        member_profile = self.get_member_profile_by_id(member_id)

        if member_profile:
            status = self.get_member_status(renew)
            if member_profile.get_status() != status:

                member_profile.set_status(status)
                self._storage.update_member_entry(member_profile)

                if renew:
                    print('Subscription successfully renewed')
                else:
                    print('Subscription paused')

            elif renew:
                print("Member is already active")
            else:
                print("Member is already inactive")

    @staticmethod
    def update_member_details(member_field: str, member: LibraryMember):
        setter_func = getattr(member, f'set_{member_field}')
        getter_func = getattr(member, f'get_{member_field}')

        member_field_formatted = member_field.title().replace('_', " ")

        while True:
            updated_field = input(f"Please provide new {member_field_formatted} (press enter to exit): ")
            if not updated_field:
                print('Exit')
                return None

            setter_func(updated_field)
            field_set = getter_func()
            if field_set == updated_field:
                print(f"{member_field_formatted} successfully updated!")
                return field_set

    @staticmethod
    def add_member_details(member_field: str, member: LibraryMember):
        setter_func = getattr(member, f'set_{member_field}')
        getter_func = getattr(member, f'get_{member_field}')

        while True:
            updated_field = input(f"Please provide member's {member_field} (press enter to exit): ")
            if not updated_field:
                print('Exit')
                return None

            setter_func(updated_field)
            field = getter_func()
            if field:
                return field

    def get_member_profile_by_id(self, member_id: int):
        if member_id is None:
            return None

        for member_profile in self._members:
            if member_profile.get_member_id() == member_id:
                return member_profile

        print(f"Member with id: {member_id} was not found in the database")
        return None

    def generate_member_id(self) -> int:
        max_member_id = self.get_max_member_id()
        return max_member_id + 1

    def get_max_member_id(self) -> int:
        member_prof = max(self._members, key=lambda x: x.get_member_id())
        return member_prof.get_member_id()

    @staticmethod
    def get_member_status(active: bool):
        return "Active" if active else "Inactive"

    def member_id_exists(self, member_id):
        return member_id in self._existing_member_ids

    @staticmethod
    def get_member_id() -> Optional[int]:
        while True:
            member_id = input('Please enter Member ID (press ENTER for exit): ')

            if not member_id:
                break
            elif member_id.isdigit():
                member_id = int(member_id)
                break
            else:
                print(f"Invalid Member ID: {member_id}")

        return member_id


if __name__ == "__main__":
    db_filename = './library.db'

    member_profile_manager = MemberManager(db_filename)

    while True:

        print("Please select one of the options below:")
        print("========")
        print("1. Add new member, ", end="")
        print("2. Update member profile, ", end="")
        print("3. Renew membership, ", end="")
        print("4. Pause membership", end="")
        choice = input(" (or press enter to exit): ")

        if not choice:
            print("Exit")
            break
        elif choice == "1":
            member_profile_manager.add_new_member()
        elif choice == "2":
            member_profile_manager.update_member_profile()
        elif choice == "3":
            member_profile_manager.manage_membership(renew=True)
        elif choice == "4":
            member_profile_manager.manage_membership(renew=False)
        else:
            print("Please enter a number between 1 and 4")
