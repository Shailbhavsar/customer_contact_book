import database
import customers
import auth

def auth_menu():
    while True:
        print("\nCUSTOMER CONTACT BOOK")
        print("\n1. Login")
        print("2. Sign Up")
        print("3. Exit")
        choice = input("\nEnter your choice: ").strip()
        if choice == '1':
            token = auth.login()
            if token:
                return token
        elif choice == '2':
            auth.signup()
        elif choice == '3':
            print("Exiting...")
            return None
        else:
            print("Invalid choice. Please try again.")


def main():
    database.create_table()
    token = auth_menu()
    if not token:
        return
                            
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
            customers.add_customer()
        elif choice == '2':
            customers.view_customers()
        elif choice == '3':
            customers.search_customer()
        elif choice == '4':
            customers.delete_customer()
        elif choice == '5':
            customers.update_customer()  
        elif choice == '6':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()  
        