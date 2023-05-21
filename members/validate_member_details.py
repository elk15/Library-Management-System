from typing import Optional
import re


def validate_name(name: str) -> Optional[str]:
    """
    Validates the correctness of the name of the library member.

    The method checks if the name is blank and ensures that it contains only valid characters.
    """

    # Check if the name is not empty.
    if (name is None) or (not name.strip()):
        print(f"Name is blank")
        return None

    # Ensure that the name contains only valid characters: alphabets, spaces, full stops (for cases such as
    # J.K. Rowling).
    if not re.match(r'^[a-z .]+$', name, flags=re.IGNORECASE):
        print(f"Invalid name: {name}. "
              f"Name must contain only valid characters: letters, spaces and dots in case of middle names")
        return None

    return name


def validate_phone_number(phone_number: str) -> Optional[str]:
    """
    Validates the correctness of the phone number of the library member.

    The method checks if the phone number is empty and ensures that it contains only digits,
    hyphens and country codes.
    """

    # Check if the phone number is not empty.
    if phone_number is None:
        print(f"Phone number is empty")
        return None

    # Ensure that the phone number consists of digits, spaces, hyphens and optionally a country code (such as +30)
    if not re.match(r'^\+?[0-9 \-]+$', phone_number):
        print(f"Invalid phone number: {phone_number}")
        return None

    return phone_number


def validate_age(age: str):
    """
    Validates the correctness of the age of the library member.

    The method ensures that the age is not blank, it is an integer, and it falls within the range
    of the permitted minimum and maximum ages in the library.
    """

    min_age = 3
    max_age = 105

    message = f"Invalid age: {age}. Age must be a integer number between {min_age} and {max_age}"

    if age is None:
        return None

    try:
        age = int(age)
        if min_age <= age <= max_age:
            return age
        else:
            print(message)
    except ValueError:
        print(message)

    return None


def validate_email(email: str):
    """
    Validates the correctness of the email of the library member.

    The method checks if the email follows acceptable forms such as "name@domain.tld", "name-surname@domain.tld",
    "name.surname@domain.tld" or "name123@domain.tld",.
    """
    if email is None:
        return None

    # matches a string that contains:
    # at least one digit, letter, hyphen or dot before and after the "@" symbol
    # followed by a dot and any word character
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(pattern, email):
        print(f"Invalid email address: {email}")
        return None

    return email


def validate_occupation(occupation: str) -> Optional[str]:
    """
    This method checks if the member occupation is not blank
    """

    if not occupation.strip():
        return None

    return occupation


def validate_status(status: str) -> Optional[str]:
    """
    Validates the correctness of the status of the library member.

    This method checks if the member status is active or inactive
    """

    if status is None:
        return None

    if status.lower() not in ['active', 'inactive']:
        raise Exception(f"Invalid status: {status}. Status can be either Active or Inactive")

    return status