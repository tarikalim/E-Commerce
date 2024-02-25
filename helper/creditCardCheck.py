import re


def validate_credit_card(credit_card_number):
    credit_card_regex = r'^\d{16}$'

    if not re.match(credit_card_regex, credit_card_number):
        return False, 'Invalid credit card number, credit card number must be 16 digits and contain only numbers.'

    return True, 'Credit card number is valid'
