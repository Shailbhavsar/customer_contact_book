import json
customers = []

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
        if not validate_phone(phone):
            continue
        if any(customer["phone"] == phone for customer in customers):
            print("Phone number already exists.")
            continue
        break

    while True:
        email = input("Enter email: ").strip()
        if not validate_email(email):
            continue
        if any(customer["email"] == email for customer in customers):
            print("Email already exists.")
            continue
        break

    next_id = max([customer["id"] for customer in customers], default=0) + 1
    customers.append({
        "id": next_id,
        "name": name,
        "phone": phone,
        "email": email
    })
    print("Customer added!")


def view_customers():
    if len(customers) == 0:
        print("\nCustomer list is empty.")
    else:
        for customer in customers:
            print(f"ID   : {customer['id']}")
            print(f"Name : {customer['name']}")
            print(f"Phone: {customer['phone']}")
            print(f"Email: {customer['email']}")
            print("-" * 30)
            
def search_customer():
    term = input("Enter name , phone or email to search: ").strip().lower()
    found = False
    
    for customer in customers:
        if (term in customer["name"].lower()
            or term in customer["phone"].lower()
            or term in customer["email"].lower()
            ):
            print(f"ID   : {customer['id']}")
            print(f"Name : {customer['name']}")
            print(f"Phone: {customer['phone']}")
            print(f"Email: {customer['email']}")
            print("-" * 30)
            found = True
    if not found:
        print("Customer not found.")

def delete_customer():
    term=input("Enter customer ID to delete: ").strip()
    
    if not term.isdigit():
        print("Invalid ID. Please enter a valid ID.")
        return
    
    term = int(term)
    found = False
        
     
    for customer in customers:
        if customer["id"] == term:
            confirm = input(f"Are you sure you want to delete {customer['name']}? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Deletion cancelled.")
                return
            customers.remove(customer)
            print("Customer deleted.")
            found=True
            break
        
    if not found:
        print("Customer not found.")
            
def update_customer():
    if not customers:
        print("No customers available to update.")
        return

    print("\nCurrent customers:")
    view_customers()

    while True:
        term = input("Enter customer ID to update (or press Enter to cancel): ").strip()
        if term == "":
            print("Update cancelled.")
            return
        if not term.isdigit():
            print("Invalid ID. Please enter a valid ID.")
            continue

        term = int(term)
        customer = next((c for c in customers if c["id"] == term), None)
        if customer is None:
            print("Customer not found. Please enter a valid ID.")
            continue
        break

    print("Leave blank to keep current value")

    while True:
        new_name = input(f"Enter new name (current: {customer['name']}): ").strip()
        if not new_name:
            break
        if validate_name(new_name):
            customer["name"] = new_name
            break

    while True:
        new_phone = input(f"Enter new phone (current: {customer['phone']}): ").strip()
        if not new_phone:
            break
        if not validate_phone(new_phone):
            continue
        if any(c["phone"] == new_phone and c != customer for c in customers):
            print("Phone number already exists.")
            continue
        customer["phone"] = new_phone
        break

    while True:
        new_email = input(f"Enter new email (current: {customer['email']}): ").strip()
        if not new_email:
            break
        if not validate_email(new_email):
            continue
        if any(c["email"] == new_email and c != customer for c in customers):
            print("Email already exists.")
            continue
        customer["email"] = new_email
        break

    print("Customer updated.")


def save_to_file():
    with open("customers.json", "w") as file:
        json.dump(customers, file, indent=4)
    print("Data saved")


def load_from_file():
    try:
        with open("customers.json", "r") as file:
            global customers
            data = json.load(file)
            customers = data if isinstance(data, list) else []
        print("Data loaded")
    except FileNotFoundError:
        print("No data file found. Starting with empty customer list.")
    except json.JSONDecodeError:
        print("Data file is corrupted. Starting with empty customer list.")
load_from_file()
                            
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
            save_to_file()
        elif choice == '2':
            view_customers()
        elif choice == '3':
            search_customer()
        elif choice == '4':
            delete_customer()
            save_to_file()
        elif choice == '5':
            update_customer() 
            save_to_file()   
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")    
            
        