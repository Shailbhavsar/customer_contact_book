from datetime import datetime
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Admin1234",
        database="customer_book"
    )
    
def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS states (
            id INT AUTO_INCREMENT PRIMARY KEY,
            state_name VARCHAR(100) NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            id INT AUTO_INCREMENT PRIMARY KEY,
            city_name VARCHAR(100) NOT NULL,
            state_id INT NOT NULL,
            FOREIGN KEY (state_id) REFERENCES states(id),
            UNIQUE (city_name, state_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            phone VARCHAR(10) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            DOB DATE,
            Address VARCHAR(255) NOT NULL,
            city_id INT,
            FOREIGN KEY (city_id) REFERENCES cities(id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()  
        
def validate_name(name):
    if not name.strip():
        print("Name cannot be empty.")
        return False
    if any(char.isdigit() for char in name):
        print("Name cannot contain numbers.")
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
        return True 

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
        return ""

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

def get_or_create_state(state_name):
    state_name = state_name.strip().upper()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM states WHERE state_name = %s", (state_name,))
    result = cursor.fetchone()

    if result:
        state_id = result[0]
    else:
        cursor.execute("INSERT INTO states (state_name) VALUES (%s)", (state_name,))
        conn.commit()
        state_id = cursor.lastrowid

    cursor.close()
    conn.close()
    return state_id


def get_or_create_city(city_name, state_id):
    city_name = city_name.strip().upper()
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM cities WHERE city_name = %s AND state_id = %s",
        (city_name, state_id)
    )
    result = cursor.fetchone()

    if result:
        city_id = result[0]
    else:
        cursor.execute(
            "INSERT INTO cities (city_name, state_id) VALUES (%s, %s)",
            (city_name, state_id)
        )
        conn.commit()
        city_id = cursor.lastrowid

    cursor.close()
    conn.close()
    return city_id

def add_customer():
    while True:
        name = input("Enter name: ").strip()
        if validate_name(name):
            break

    while True:
        phone = input("Enter phone: ").strip()
        if validate_phone(phone):
            break

    while True:
        email = input("Enter email: ").strip()
        if validate_email(email):
            break

    while True:
        dob_input = input("Enter date of birth (DDMMYYYY): ").strip()
        if dob_input == "":
                dob = ""
                break
        dob = format_dob(dob_input)
        if dob is not None:
                break
      
    while True:
        address = input("Enter address: ").strip()
        if validate_address(address):
            break
    while True:
        city_name = input("Enter city: ").strip()
        if validate_city_state(city_name, "City"):
            break

    while True:
        state_name = input("Enter state: ").strip()
        if validate_city_state(state_name, "State"):
            break

    state_id = get_or_create_state(state_name)
    city_id = get_or_create_city(city_name, state_id)

    age = get_age(dob) 
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
            "INSERT INTO customers (name, phone, email, DOB, Address, city_id) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (name, phone, email, dob or None, address or None, city_id)
        )
    conn.commit()
    print("Customer added!")
    cursor.close()
    conn.close()

def view_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT customers.id, customers.name, customers.phone, customers.email,
               customers.DOB, customers.Address,
               cities.city_name, states.state_name
        FROM customers
        LEFT JOIN cities ON customers.city_id = cities.id
        LEFT JOIN states ON cities.state_id = states.id
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        print("\nCustomer list is empty.")
    else:
        for row in rows:
            print(f"ID      : {row[0]}")
            print(f"Name    : {row[1]}")
            print(f"Phone   : {row[2]}")
            print(f"Email   : {row[3]}")
            print(f"DOB     : {row[4].strftime('%d-%m-%Y') if row[4] else '—'}")
            print(f"Age     : {get_age(row[4]) if row[4] else '—'}")
            print(f"Address : {row[5] or '—'}")
            print(f"City    : {row[6] or '—'}")
            print(f"State   : {row[7] or '—'}")
            print("-" * 30)
            
def search_customer():
    term = input("Enter name, phone, email, city or state to search: ").strip().lower()
    pattern = f"%{term}%"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT customers.id, customers.name, customers.phone, customers.email,
               customers.DOB, customers.Address,
               cities.city_name, states.state_name
        FROM customers
        LEFT JOIN cities ON customers.city_id = cities.id
        LEFT JOIN states ON cities.state_id = states.id
        WHERE customers.name LIKE %s
           OR customers.phone LIKE %s
           OR customers.email LIKE %s
           OR cities.city_name LIKE %s
           OR states.state_name LIKE %s
    """, (pattern, pattern, pattern, pattern, pattern))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        print("Customer not found.")
        return

    for row in rows:
        print(f"ID      : {row[0]}")
        print(f"Name    : {row[1]}")
        print(f"Phone   : {row[2]}")
        print(f"Email   : {row[3]}")
        print(f"DOB     : {row[4].strftime('%d-%m-%Y') if row[4] else '—'}")
        print(f"Age     : {get_age(row[4]) if row[4] else '—'}")
        print(f"Address : {row[5] or '—'}")
        print(f"City    : {row[6] or '—'}")
        print(f"State   : {row[7] or '—'}")
        print("-" * 30)  
              
def delete_customer():
    term = input("Enter customer ID to delete: ").strip()

    if not term.isdigit():
        print("Invalid ID. Please enter a valid ID.")
        return

    customer_id = int(term)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM customers WHERE id = %s", (customer_id,))
    result = cursor.fetchone()

    if not result:
        print("Customer not found.")
        cursor.close()
        conn.close()
        return

    confirm = input(f"Are you sure you want to delete {result[0]}? (y/n): ").strip().lower()
    if confirm == 'y':
        cursor.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
        conn.commit()
        print("Customer deleted.")
    else:
        print("Deletion cancelled.")

    cursor.close()
    conn.close()
                
def update_customer():
    view_customers()

    term = input("Enter customer ID to update (or press Enter to cancel): ").strip()
    if term == "":
        print("Update cancelled.")
        return
    
    if not term.isdigit():
        print("Invalid ID. Please enter a valid ID.")
        return

    customer_id = int(term)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, phone, email, DOB, Address, city_id FROM customers WHERE id = %s",
        (customer_id,)
    )
    customer = cursor.fetchone()

    if not customer:
        print("Customer not found.")
        cursor.close()
        conn.close()
        return

    print("Press Enter to keep current value")

    new_name = customer[1]
    while True:
        name_input = input(f"Enter new name (current: {customer[1]}): ").strip()
        if name_input == "":
            break
        if validate_name(name_input):
            new_name = name_input
            break

    new_phone = customer[2]
    while True:
        phone_input = input(f"Enter new phone (current: {customer[2]}): ").strip()
        if phone_input == "":
            break
        if phone_input == customer[2]:
            new_phone = phone_input
            break
        if validate_phone(phone_input):
            new_phone = phone_input
            break

    new_email = customer[3]
    while True:
        email_input = input(f"Enter new email (current: {customer[3]}): ").strip()
        if email_input == "":
            break
        if email_input == customer[3]:
            new_email = email_input
            break
        if validate_email(email_input):
            new_email = email_input
            break

    new_dob = customer[4]
    while True:
        dob_input = input(f"Enter new DOB as DDMMYYYY (current: {customer[4].strftime('%d-%m-%Y') if customer[4] else '—'}): ").strip()
        if dob_input == "":
            break
        formatted = format_dob(dob_input)
        if formatted is not None:
            new_dob = formatted
            break  

    new_address = customer[5]
    while True:
        address_input = input(f"Enter new address (current: {customer[5] or '—'}): ").strip()
        if address_input == "":
            break
        if validate_address(address_input):
            new_address = address_input
            break

    new_city_id = customer[6]

    cursor.execute("""
        SELECT cities.city_name, states.state_name
        FROM cities
        LEFT JOIN states ON cities.state_id = states.id
        WHERE cities.id = %s""", (customer[6],))
    
    city_state_row = cursor.fetchone()

    current_city = city_state_row[0] if city_state_row else "—"
    current_state = city_state_row[1] if city_state_row else "—"

    city_input = input(f"Enter new city (current: {current_city}): ").strip()
    state_input = input(f"Enter new state (current: {current_state}): ").strip()

    if city_input or state_input:
        if not city_input:
            print("City is required if you're changing state. Keeping current city/state.")
        elif not state_input:
            print("State is required if you're changing city. Keeping current city/state.")
        else:
            state_id = get_or_create_state(state_input)
            new_city_id = get_or_create_city(city_input, state_id)

    cursor.execute(
        "UPDATE customers SET name=%s, phone=%s, email=%s, DOB=%s, Address=%s, city_id=%s WHERE id=%s",
        (new_name, new_phone, new_email, new_dob, new_address, new_city_id, customer_id)
        )
    conn.commit()
    print("Customer updated.")
    cursor.close()
    conn.close()
                
create_table()
                            
while True:
        print("\nCustomer Contact Book")
        print("\n1. Add Customer")
        print("2. View Customers")
        print("3. Search Customer")
        print("4. Delete Customer")
        print("5. Update Customer")
        print("6. Exit")
        choice = input("\nEnter your choice: ").strip()
        if choice == '1':
            add_customer()
        elif choice == '2':
            view_customers()
        elif choice == '3':
            search_customer()
        elif choice == '4':
            delete_customer()
        elif choice == '5':
            update_customer()  
        elif choice == '6':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")    