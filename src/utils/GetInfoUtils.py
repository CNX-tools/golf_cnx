import random
import os

email_dir = os.path.join(os.getcwd(), 'assets', 'emails.txt')
used_email_dir = os.path.join(os.getcwd(), 'assets', 'used_info.csv')

# Get the used info
with open(used_email_dir, 'r') as f:
    used_info = list(map(lambda x: x.strip(), f.readlines()))

used_info = list(map(lambda x: x.split(','), used_info))
used_emails = list(map(lambda x: x[0], used_info))
used_phone_numbers = list(map(lambda x: x[1], used_info))


def __get_email() -> str:
    with open(email_dir, 'r', encoding='utf8') as f:
        emails = list(map(lambda x: x.strip(), f.readlines()))

    while True:
        use_email = random.choice(emails)
        if use_email not in used_emails:
            break

    return use_email


def __get_first_name() -> str:
    return "William"


def __get_last_name() -> str:
    return "Chan"


def __get_password() -> str:
    return "Testpassword@123"


def __get_phone() -> str:
    bc_area_code = ["236", "250", "604", "778"]
    local_number = random.randint(1000000, 9999999)

    use_phone_number = f"{random.choice(bc_area_code)}{local_number}"

    if use_phone_number in used_phone_numbers:
        return __get_phone()
    else:
        return use_phone_number


def get_random_info(use_phone=None) -> dict:
    # Get the random info
    email = __get_email()
    first_name = __get_first_name()
    last_name = __get_last_name()
    password = __get_password()

    if use_phone is None:
        phone = __get_phone()
    else:
        phone = use_phone

    # Store the used info
    with open(used_email_dir, 'a') as f:
        f.write(f"{email},{phone},{first_name + ' ' + last_name},{password}\n")

    data = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'password': password,
        'phone': phone
    }

    return data
