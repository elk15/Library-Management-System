import re
from typing import Optional


class LibraryMember:

    """
    Class representing a library member with personal details.

    Attributes:
        _member_id (int): The unique identifier for the library member.
        _name (str): The name of the library member.
        _address (str): The address of the library member.
        _phone_number (str): The phone number of the library member.
        _email (str): The email address of the library member.
        _age (str): The age of the library member.
        _occupation (str): The occupation of the library member.
        _status (str): The subscription status (active or inactive) of the library member.
    """

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

    def set_member_id(self, member_id: int) -> None:
        self._member_id = member_id

    def set_status(self, status: str) -> None:
        self._status = status

    def get_member_id(self) -> int:
        return self._member_id

    def get_name(self) -> str:
        return self._name

    def get_address(self) -> str:
        return self._address

    def get_phone_number(self) -> str:
        return self._phone_number

    def get_email(self) -> str:
        return self._email

    def get_age(self) -> str:
        return self._age

    def get_occupation(self) -> str:
        return self._occupation

    def get_status(self) -> str:
        return self._status
