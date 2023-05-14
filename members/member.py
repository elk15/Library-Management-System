import re
from typing import Optional


class LibraryMember:
    """ Προφίλ μέλους δανειστικής βιβλιοθήκης"""
    LOWER_AGE_LIMIT = 3
    UPPER_AGE_LIMIT = 105

    def __init__(self,
                 member_id: Optional[int] = None,
                 name: Optional[str] = None,
                 address: Optional[str] = None,
                 phone_number: Optional[str] = None,
                 email: Optional[str] = None,
                 age: Optional[str] = None,
                 occupation: Optional[str] = None,
                 status: Optional[str] = None):

        self._member_id = member_id
        self._name = name
        self._address = address
        self._phone_number = phone_number
        self._email = email
        self._age = age
        self._occupation = occupation
        self._status = status

    def __repr__(self):
        """Prints class attributes"""
        attributes = ""
        for attribute_name, attribute_val in self.__dict__.items():
            attributes += f"{attribute_val}\t"
        return attributes

    def set_member_id(self, member_id: int):
        self._member_id = member_id

    def set_name(self, name: str):
        if self.validate_name(name):
            self._name = name

    def set_address(self, address: str):
        # TODO: Add address validation
        self._address = address

    def set_phone_number(self, phone_number: str):
        if self.validate_phone_number(phone_number):
            self._phone_number = phone_number

    def set_email(self, email: str):
        if self.validate_email(email):
            self._email = email

    def set_age(self, age: str):
        if self.validate_age(age):
            self._age = age

    def set_occupation(self, occupation: str):
        self._occupation = occupation

    def set_status(self, status: str):
        if self.validate_status(status):
            self._status = status

    def get_member_id(self):
        return self._member_id

    def get_name(self):
        return self._name

    def get_address(self):
        return self._address

    def get_phone_number(self):
        return self._phone_number

    def get_email(self):
        return self._email

    def get_age(self):
        return self._age

    def get_occupation(self):
        return self._occupation

    def get_status(self):
        return self._status

    @staticmethod
    def validate_name(name: str) -> Optional[str]:
        # Check if the name is not empty.
        if (name is None) or (not name.strip()):
            print(f"Name is blank")
            return None

        # Ensure that the name contains only valid characters (alphabets, spaces, full stops e.g. J.K. Rowling etc.).
        pattern = r'^[a-z .]+$'
        if not re.match(pattern, name, flags=re.IGNORECASE):
            print(f"Invalid name: {name}. Name must contain only valid characters: alphabets, spaces and dots in case "
                  f"of middle names")
            return None

        return name

    @staticmethod
    def validate_phone_number(phone_number: str) -> Optional[str]:
        # Check if the phone number is not empty.
        if phone_number is None:
            print(f"Phone number is empty")
            return None

        pattern = r'^\+?[0-9 \-]+$'
        if not re.match(pattern, phone_number):
            print(f"Invalid phone number: {phone_number}")
            return None

        return phone_number

    @staticmethod
    def validate_age(age: str):
        lower_limit = LibraryMember.LOWER_AGE_LIMIT
        upper_limit = LibraryMember.UPPER_AGE_LIMIT
        message = f"Invalid age: {age}. Age must be a integer number between " \
                  f"{lower_limit} and {upper_limit}"

        if age is None:
            return None

        try:
            age = int(age)
            if lower_limit <= age <= upper_limit:
                return age
            else:
                print(message)
        except ValueError:
            print(message)

        return None

    @staticmethod
    def validate_email(email: str):
        if email is None:
            return None

        # matches a string that contains:
        # at least one digit, letter, hyphen or dot before  and after the "@" symbol
        # followed by a dot and any word character
        pattern = r'^[a-z0-9\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            print(f"Invalid email address: {email}")
            return None

        return email

    @staticmethod
    def validate_occupation(occupation: str):
        if not occupation.strip():
            return None

        return occupation

    @staticmethod
    def validate_status(status: str):
        if status is None:
            return None

        valid_status_vals = ['active', 'inactive']
        if status.lower() not in valid_status_vals:
            raise Exception(f"Μη έγκυρη τιμή status: {status} με επιτρεπτές τιμές: {valid_status_vals}")

        return status
