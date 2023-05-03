
def combine_address_components(*components):
    address = ""
    for component in components:
        address += f"{component} "
    return address


def validate_address_components(steet_address: str, city: str, zip_code: str, country: str, state: Optional[str]):
    # required_fields: street address, city, ZIP code, country

    # check ZIP code
    zip_code = preprocess_zip_code(zip_code)
    if consists_of_five_digits(zip_code):
        print("Invalid zip code. Zip code must consist of 5 digits")


def preprocess_zip_code(zip_code):
    zip_code = zip_code.replace(" ", "")
    zip_code = zip_code.replace("-", "")
    return zip_code


def consists_of_five_digits(zip_code):
    return (len(zip_code) != 5) or (not zip_code.isdigit())
