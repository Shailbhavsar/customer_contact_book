from database import create_table
from customers import (
    add_customer,
    view_customers,
    search_customer, 
    delete_customer,
    update_customer )

def main():
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

if __name__ == "__main__":
    main()  
            