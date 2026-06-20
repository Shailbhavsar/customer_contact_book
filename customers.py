
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
        CREATE TABLE IF NOT EXISTS customers ( 
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        phone VARCHAR(10) NOT NULL UNIQUE,
        email VARCHAR(255) NOT NULL UNIQUE
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
    return True


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

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO customers (name, phone, email) VALUES (%s, %s, %s)",
            (name, phone, email)
        )
        conn.commit()
        print("Customer added!")
    except mysql.connector.IntegrityError:
        print("Phone or email already exists.")
    finally:
        cursor.close()
        conn.close()

def view_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, email FROM customers")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        print("\nCustomer list is empty.")
    else:
        for row in rows:
            print(f"ID   : {row[0]}")
            print(f"Name : {row[1]}")
            print(f"Phone: {row[2]}")
            print(f"Email: {row[3]}")
            print("-" * 30)
            
def search_customer():
    term = input("Enter name, phone or email to search: ").strip().lower()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, email FROM customers")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    found = False
    for row in rows:
        if (term in row[1].lower()
            or term in row[2]
            or term in row[3].lower()):
            print(f"ID   : {row[0]}")
            print(f"Name : {row[1]}")
            print(f"Phone: {row[2]}")
            print(f"Email: {row[3]}")
            print("-" * 30)
            found = True

    if not found:
        print("Customer not found.")
        
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
    cursor.execute("SELECT id, name, phone, email FROM customers WHERE id = %s", (customer_id,))
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
        if validate_phone(phone_input):
            new_phone = phone_input
            break

    new_email = customer[3]
    while True:
        email_input = input(f"Enter new email (current: {customer[3]}): ").strip()
        if email_input == "":
            break
        if validate_email(email_input):
            new_email = email_input
            break

    try:
        cursor.execute(
            "UPDATE customers SET name=%s, phone=%s, email=%s WHERE id=%s",
            (new_name, new_phone, new_email, customer_id)
        )
        conn.commit()
        print("Customer updated.")
    except mysql.connector.IntegrityError:
        print("Phone or email already exists.")
    finally:
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
            
        