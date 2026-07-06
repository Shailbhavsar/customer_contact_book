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
            token= auth.signup()
            if token:
                return token
        elif choice == '3':
            print("Exiting...")
            return None
        else:
            print("Invalid choice. Please try again.")
            
def get_valid_payload(token):
    return auth.decode_jwt_token(token)


def main():
    database.create_table()
    token = auth_menu()
    if not token:
        return

                          
    while True:
        payload = get_valid_payload(token)
        if payload is None:
            print("Session expired or invalid token. Please log in again.")
            token = auth_menu()
            if not token:
                return
            continue
        is_admin = payload.get("role") == "admin"
        
        print("\nCustomer Contact Book")
        print("\n1. Add Customer")
        print("2. View Customers")
        print("3. Search Customer")
        print("4. Delete Customer" +(""if is_admin else "(admin only)"))
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
            payload = get_valid_payload(token)
            if payload is None:
                print("Session expired or invalid token. Please log in again.")
                token = auth_menu()
                if not token:
                    return
                continue
            if payload.get("role") != "admin":
                print("You do not have permission to delete customers. Admin access required.")
            else:
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
        