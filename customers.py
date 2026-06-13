import json
customers = []


def add_customer():
    name = input("Enter name: ")
    phone = input("Enter phone: ")  
    email = input("Enter email: ")
    customers.append({
        "name": name,
        "phone": phone,
        "email": email
    }
    )
    print("Customer added!")


def view_customers():
    if len(customers) == 0:
        print("No customers found.")
    else:
        for customer in customers:
            print(customer)
            
def search_customer():
    term = input("Enter name to search: ").lower()
    found = False
    
    for customer in customers:
        if term in customer["name"].lower():
            print(customer)
            found = True
    if not found:
        print("Customer not found.")
           
def delete_customer():
    term=input("Enter name of customer to delete: ").lower()
    found=False
     
    for customer in customers:
        if term in customer["name"].lower():
            customers.remove(customer)
            print("Customer deleted.")
            found=True
            break
        
    if not found:
         print("Customer not found.")
            
def update_customer():
    term = input("Enter name of customer to update: ").lower()
    found = False

    for customer in customers:
        if term == customer["name"].lower():
            print("Leave blank to keep current value")
            new_name = input(f"Enter new name (current: {customer['name']}): ")
            new_phone = input(f"Enter new phone (current: {customer['phone']}): ")
            new_email = input(f"Enter new email (current: {customer['email']}): ")

            if new_name:
                customer["name"] = new_name
            if new_phone:
                customer["phone"] = new_phone
            if new_email:
                customer["email"] = new_email
            print("Customer updated.")
            found = True
            break
    if not found:
        print("Customer not found.")


def save_to_file():
    with open("customers.json", "w") as file:
        json.dump(customers, file)
    print("Data saved")


def load_from_file():
    try:
        with open("customers.json", "r") as file:
            global customers
            customers = json.load(file)
        print("Data loaded")
    except FileNotFoundError:
        print("No data file found. Starting with empty customer list.")
    except json.JSONDecodeError:
        print("Data file is corrupted. Starting with empty customer list.")
load_from_file()
                            
while True:
        print("\n1. Add Customer")
        print("2. View Customers")
        print("3. Search Customer")
        print("4. delete Customer")
        print("5. update Customer")
        print("6. Exit")
        choice = input("Enter your choice: ")
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
        
        save_to_file()
        