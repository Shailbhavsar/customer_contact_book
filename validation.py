from datetime import datetime
from database import get_connection

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

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM customers WHERE phone = %s", (phone,))
    exists = cursor.fetchone()
    cursor.close()
    conn.close()

    if exists:
        print("This phone number is already registered.")
        return False

    return True

def validate_email(email):
    if not email:
        print("Email cannot be empty.")
        return False
    if "@" not in email or "." not in email:
        print("Invalid email format.")
        return False
    if " " in email:
        print("Email cannot contain spaces.")
        return False

    conn = get_connection()
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
        parsed_date = datetime.strptime(dob, "%d-%m-%Y")
    except ValueError:
        print("Invalid date. Please check the date , month, and year.")
        return False

    if parsed_date.date() > datetime.now().date():
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

    return datetime.strptime(formatted, "%d-%m-%Y").date()

def get_age(dob):
    if not dob:
        return None
    today = datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    
    return age
