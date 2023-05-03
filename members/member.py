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

        self._member_id = member_id
        self._name = name
        self._address = address
        self._phone_number = phone_number
        self._email = email
        self._age = age
        self._occupation = occupation

        if status.lower() not in ['ενεργή', 'ανενεργή']:
            raise Exception(f"Μη έγκυρη τιμή status: {status}. Παρακαλώ επιλέξτε ενεργή ή ανενεργή")
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

