import re
import dns.resolver


def validate_credit_card(credit_card_number):
    credit_card_regex = r'^\d{16}$'

    if not re.match(credit_card_regex, credit_card_number):
        return False, 'Invalid credit card number, credit card number must be 16 digits and contain only numbers.'

    return True, 'Credit card number is valid'


def validate_password(password):
    if len(password) >= 8 and re.search(r"[A-Z]", password) and re.search(r"[0-9]", password):
        return True
    return False


def validate_mx_record(email):
    domain = email.split('@')[-1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return False


def validate_email(email):
    email_regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    if not re.match(email_regex, email):
        return False, 'Invalid email format'

    if not validate_mx_record(email):
        return False, 'Email domain is not valid'

    return True, 'Email is valid'
