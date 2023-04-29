from typing import Optional, List, Union


class LibraryMember:
    """ Προφίλ μέλους δανειστικής βιβλιοθήκης"""

    def __init__(self,
                 member_id: str,
                 name: str,
                 address: str,
                 phone_number: str,
                 email: str,
                 age: str,
                 occupation: str,
                 status: str):

        # check member id
        self._member_id = member_id
        # check name
        self._name = name

        # check address
        self._address = address

        # check phone number
        self._phone_number = phone_number

        # check email
        self._email = email

        # check age
        self._age = age

        self._occupation = occupation

        # check if status is active or inactive
        self._status = status

    def __repr__(self):
        """Prints class attributes"""
        attributes = ""
        for attribute_name, attribute_val in self.__dict__.items():
            attributes += f"{attribute_val}\t"
        return attributes

    def get_member_id(self):
        return self._member_id

    def get_member_status(self):
        return self._status