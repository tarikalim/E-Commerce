import re
import dns.resolver


def check_mx_record(email):
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

    if not check_mx_record(email):
        return False, 'Email domain is not valid'

    return True, 'Email is valid'
