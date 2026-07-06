import datetime
import re
import database

def validate_username(username):
    if not username.strip():
        print("Username cannot be empty.")
        return False
    if len(username) < 3:
        print("Username must be at least 3 characters long.")
        return False
    if not re.match("^[a-zA-Z0-9_]+$", username):
        print("Username can only contain letters, numbers, and underscores.")
        return False
    return True

def validate_password(password):
    if not password:
        print("Password cannot be empty.")
        return False
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        return False
    if not re.search(r"[A-Z]", password):
        print("Password must contain at least one uppercase letter.")
        return False
    if not re.search(r"[a-z]", password):
        print("Password must contain at least one lowercase letter.")
        return False
    if not re.search(r"[0-9]", password):
        print("Password must contain at least one digit.")
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        print("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>).")
        return False
    return True

def validate_name(name):
    if not name.strip():
        print("Name cannot be empty.")
        return False
    if any(char.isdigit() for char in name):
        print("Name cannot contain numbers.")
        return False
    if not all(char.isalpha() or char.isspace() for char in name):  
        print("Name can only contain letters and spaces.")
        return False
    parts = name.split()
    if len(parts) < 2:
        print("Please  enter both first name and last name.")
        return False
    
    return True

def validate_phone(phone):
    if not phone:
        print("Phone cannot be empty.")
        return False
    if not phone.isdigit():
        print("Phone must contain only digits.")
        return False
    if len(phone) != 10:
        print("Phone number must be 10 digits.")
        return False

    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM customers WHERE phone = %s", (phone,))
    exists = cursor.fetchone()
    cursor.close()
    conn.close()

    if exists:
        print("This phone number is already registered.")
        return False

    return True

def is_valid_email_format(email):
    if not email:
        print("Email cannot be empty.")
        return False
    if "@" not in email or "." not in email:
        print("Invalid email format.")
        return False
    if " " in email:
        print("Email cannot contain spaces.")
        return False
    return True

def validate_email(email):
    if not is_valid_email_format(email):
        return False

    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM customers WHERE email = %s", (email,))
    exists = cursor.fetchone()
    cursor.close()
    conn.close()

    if exists:
        print("This email is already registered.")
        return False

    return True

def validate_address(address):
    if not address.strip():
        print("Address cannot be empty.")
        return False
    return True

def validate_dob(dob):
    if not dob:
        print("Date of birth cannot be empty.")
        return False

    try:
        parsed_date = datetime.datetime.strptime(dob, "%d-%m-%Y")
    except ValueError:
        print("Invalid date. Please check the date , month, and year.")
        return False

    if parsed_date.date() > datetime.datetime.now().date():
        print("Date of birth cannot be in the future.")
        return False

    return True

def validate_city_state(value, field_name):
    if not value.strip():
        print(f"{field_name} cannot be empty.")
        return False
    return True


def format_dob(dob_input):
    digits = dob_input.replace("-", "").strip()

    if not digits:
        print("DOB cannot be empty.")
        return None

    if not digits.isdigit() or len(digits) != 8:
        print("DOB must be in DDMMYYYY format.")
        return None

    formatted = f"{digits[0:2]}-{digits[2:4]}-{digits[4:8]}"

    if not validate_dob(formatted):
        return None

    return datetime.datetime.strptime(formatted, "%d-%m-%Y").date()

def get_age(dob):
    if not dob:
        return None
    today = datetime.datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    
    return age
