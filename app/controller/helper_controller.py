import re


def is_valid_email(email):
    return '@' in email and '.' in email.split('@')[1]


def is_valid_name(name):
    return not any(char.isdigit() for char in name)


def is_valid_password(password):
    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[\W_]).{8,}$'
    return re.match(pattern, password)


def is_not_empty_or_null(data, keys):
    return all(key in data and data[key] for key in keys)


def is_integer(x):
    try:
        int(x)
        return True
    except ValueError:
        return False
