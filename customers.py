from database import get_connection
import validation



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
        if validation.validate_name(name):
            break

    while True:
        phone = input("Enter phone: ").strip()
        if validation.validate_phone(phone):
            break

    while True:
        email = input("Enter email: ").strip()
        if validation.validate_email(email):
            break

    while True:
        dob_input = input("Enter date of birth (DDMMYYYY): ").strip()
        dob = validation.format_dob(dob_input)
        if dob is not None:
                break
      
    while True:
        address = input("Enter address: ").strip()
        if validation.validate_address(address):
            break
    while True:
        city_name = input("Enter city: ").strip()
        if validation.validate_city_state(city_name, "City"):
            break

    while True:
        state_name = input("Enter state: ").strip()
        if validation.validate_city_state(state_name, "State"):
            break

    state_id = get_or_create_state(state_name)
    city_id = get_or_create_city(city_name, state_id)

    age = validation.get_age(dob) 
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
            print(f"Age     : {validation.get_age(row[4]) if row[4] else '—'}")
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
        print(f"Age     : {validation.get_age(row[4]) if row[4] else '—'}")
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
        if validation.validate_name(name_input):
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
        if validation.validate_phone(phone_input):
            new_phone = phone_input
            break

    new_email = customer[3]
    while True:
        email_input = input(f"Enter new email (current: {customer[3]}): ").strip()
        if email_input == "":
            break
        if email_input.lower() == customer[3].lower():
            new_email = email_input
            break
        if validation.validate_email(email_input):
            new_email = email_input
            break

    new_dob = customer[4]
    while True:
        dob_input = input(f"Enter new DOB as DDMMYYYY (current: {customer[4].strftime('%d-%m-%Y') if customer[4] else '—'}): ").strip()
        if dob_input == "":
            break
        formatted = validation.format_dob(dob_input)
        if formatted is not None:
            new_dob = formatted
            break  

    new_address = customer[5]
    while True:
        address_input = input(f"Enter new address (current: {customer[5] or '—'}): ").strip()
        if address_input == "":
            break
        if validation.validate_address(address_input):
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
                
