import Models as models
from datetime import datetime
# Main Application Functions

def add_customer():
    try:
        name = input("Enter customer name: ")
        contact = input("Enter customer contact: ")
        payment = input("Enter payment method (e.g., cash, credit card): ")
        models.add_customer_to_db(name, contact, payment)
        print(f"Customer {name} added successfully!")
    except Exception as e:
        print(f"Error adding customer: {e}")

def available_rooms():
    """Retrieve and display available rooms."""
    rooms = models.get_rooms()
    return [room for room in rooms if room["availability"]]

def input_reservation_details():
    """Get reservation details from the user."""
    return {
        "room_number": int(input("Enter room number to book: ")),
        "customer_name": input("Enter customer name for the reservation: "),
        "check_in": input("Enter check-in date (YYYY-MM-DD): "),
        "check_out": input("Enter check-out date (YYYY-MM-DD): "),
    }

def make_reservation():
    """Declarative function for making a reservation."""
    rooms = available_rooms()

    if not rooms:
        print("No available rooms.")
        return

    print("\nAvailable rooms:")
    output = []
    for room in rooms:
        room_info = f"Room {room['roomNumber']} - {room['roomType']} - ${room['price']}"
        output.append(room_info)

    #Join the list into a single string separated by newlines and print
    print("\n".join(output))

    try:
        reservation_details = input_reservation_details()
        message = models.add_reservation_to_db(
            reservation_details["customer_name"],
            reservation_details["room_number"],
            reservation_details["check_in"],
            reservation_details["check_out"]
        )
        print(message)
    except ValueError:
        print("Invalid input. Please try again.")
    except Exception as e:
        print(f"Error making reservation: {e}")

def checkout():
    try:
        room_number = int(input("Enter room number to check out: "))
        message = models.checkout_room_from_db(room_number)
        print(message)
    except ValueError:
        print("Invalid input. Please enter a valid room number.")
    except Exception as e:
        print(f"Error during checkout: {e}")

def add_room():
    try:
        room_number = int(input("Enter room number: "))
        room_type = input("Enter room type (single, double, suite, etc.): ")
        price = int(input("Enter price per night: "))
        availability = input("Is the room available? (yes/no): ").strip().lower() == "yes"
        models.add_room_to_db(room_number, room_type, price, availability)
    except ValueError:
        print("Invalid input. Please enter valid data.")
    except Exception as e:
        print(f"Error adding room: {e}")

def delete_room():
    try:
        room_number = int(input("Enter room number to delete: "))
        models.delete_room_from_db(room_number)
    except ValueError:
        print("Invalid input. Please enter a valid room number.")
    except Exception as e:
        print(f"Error deleting room: {e}")

def show_customers():
    try:
        customers = models.get_customers()
        print("\nList of Customers:")
        for customer in customers:
            print(f"ID: {customer['id']}, Name: {customer['name']}, Contact: {customer['contact']}, Payment: {customer['payment']}")
            reservations = models.get_reservations_for_customer(customer['id'])
            if reservations:
                print("  Rooms rented:")
                for reservation in reservations:
                    print(f"    Room {reservation[0]} - {reservation[1]}")
            else:
                print("  No rooms rented.")
    except Exception as e:
        print(f"Error displaying customers: {e}")

def delete_customer():
    try:
        customer_id = int(input("Enter customer ID to delete: "))
        models.delete_customer_from_db(customer_id)
    except ValueError:
        print("Invalid input. Please enter a valid customer ID.")
    except Exception as e:
        print(f"Error deleting customer: {e}")

def show_bill(customer_id):
    """Function to calculate and show the customer's bill based on reservations."""
    # Get reservations for the customer
    reservations = models.get_reservations_for_customer(customer_id)
    if not reservations:
        print("No reservations found for this customer.")
        return

    total_bill = 0

    # Iterate through reservations
    for reservation in reservations:
        room_number = reservation[0]
        check_in = reservation[2]
        check_out = reservation[3]

        # Look up the room directly
        rooms = models.get_rooms()
        room = None
        for r in rooms:
            if r["roomNumber"] == room_number:
                room = r
                break
        if room:
            room_price = room["price"]  
            days_stayed = (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days
            total_bill += room_price * days_stayed
    
    print(f"Total bill for customer {customer_id}: ${total_bill}")

# Run the setup
models.create_tables()  # Run this once to create the tables

# Main loop for manual testing
while __name__ =="__main__":
    print("\nMenu:")
    print("1. Add Customer")
    print("2. Make Reservation")
    print("3. Check Out")
    print("4. View Available Rooms")
    print("5. Add Room")
    print("6. Delete Room")
    print("7. Show Customers")
    print("8. Delete Customer")
    print("9. Show Bill")
    print("10. Exit")
    
    try:
        choice = input("Choose an option: ")
        if choice == "1":
            add_customer()
        elif choice == "2":
            make_reservation()
        elif choice == "3":
            checkout()
        elif choice == "4":
            rooms = models.get_rooms()
            print("\nAvailable Rooms:")
            for room in rooms:
                if room["availability"]:
                    print(f"Room {room['roomNumber']} - {room['roomType']} - ${room['price']}")
        elif choice == "5":
            add_room()
        elif choice == "6":
            delete_room()
        elif choice == "7":
            show_customers()
        elif choice == "8":
            delete_customer()
        elif choice == "9":
            customer_id = int(input("Enter customer ID to view the bill: "))
            show_bill(customer_id)
        elif choice == "10":
            print("Exiting...")
            break
        else:
            print("Invalid option, please try again.")
    except Exception as e:
        print(f"Unexpected error: {e}")
