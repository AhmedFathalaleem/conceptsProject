import Models as models
from datetime import datetime

# built version of filter , map

def map_bltin(func, data):
    if not data:  
        return []
    return [func(data[0])] + map_bltin(func, data[1:])

def filter_bltin(things, condition_fn):
    if not things:  # Base case: empty list
        return []
    # Check if the first room satisfies the condition
    if condition_fn(things[0]):
        return [things[0]] + filter_bltin(things[1:], condition_fn)
    # Skip the current room if the condition is not met
    return filter_bltin(things[1:], condition_fn)

def reduce_bltin(func, data, initial):
    if not data:  # Base case: empty list
        return initial
    # Apply the function to the accumulator and the first element
    return reduce_bltin(func, data[1:], func(initial, data[0]))


# Main Application Functions

# Retrieve and display available rooms.
def available_rooms():
    rooms = models.get_rooms()
    return tuple(filter_bltin(rooms, lambda room: room["availability"]))

# Get reservation details from the user.
def input_reservation_details():  
    return {
        "room_number": int(input("Enter room number to book: ")),
        "customer_name": input("Enter customer name for the reservation: "),
        "check_in": input("Enter check-in date (YYYY-MM-DD): "),
        "check_out": input("Enter check-out date (YYYY-MM-DD): "),
    }


# Function for making a reservation.
def make_reservation():
    rooms = available_rooms()

    if not rooms:
        print("No available rooms.")
        return

    print("\nAvailable rooms:")
    transform_fn = lambda room: f"Room {room['roomNumber']} - {room['roomType']} - ${room['price']}"
    room_info = tuple(map_bltin(transform_fn,rooms))    
    print("\n".join(room_info))

    try:
        reservation_details = input_reservation_details()
        # check check out date < check in date
        daysnum = (datetime.strptime(reservation_details["check_out"], "%Y-%m-%d") - datetime.strptime(reservation_details["check_in"], "%Y-%m-%d")).days
        if daysnum <=0:
            print("Wrong date")
            return
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
        message = models.delete_reservation_from_db(room_number)
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

def add_customer():
    try:
        name = input("Enter customer name: ")
        contact = input("Enter customer contact: ")
        payment = input("Enter payment method (e.g., cash, credit card): ")
        models.add_customer_to_db(name, contact, payment)
        print(f"Customer {name} added successfully!")
    except Exception as e:
        print(f"Error adding customer: {e}")


# Get and display customers inforamtion.
def show_customers():
    try:
        customers = models.get_customers()
        print("\nList of Customers:")

        # Map over customers to print their details
        transform_fn = lambda customer: print_customer_details(customer)
        map_bltin(transform_fn, customers)        
    except Exception as e:
        print(f"Error displaying customers: {e}")

def print_customer_details(customer):
    """Print details of a single customer and their reservations."""
    print(f"ID: {customer['id']}, Name: {customer['name']}, Contact: {customer['contact']}, Payment: {customer['payment']}")
    reservations = models.get_reservations_for_customer(customer['id'])
    
    if reservations:
        print("  Rooms rented:")
        transform_fn = lambda reservation: print(f"    Room {reservation[0]} - {reservation[1]}")
        map_bltin(transform_fn, reservations)
    else:
        print("  No rooms rented.")


def delete_customer():
    try:
        customer_id = int(input("Enter customer ID to delete: "))
        models.delete_customer_from_db(customer_id)
    except ValueError:
        print("Invalid input. Please enter a valid customer ID.")
    except Exception as e:
        print(f"Error deleting customer: {e}")


 #Function to calculate and show the customer's bill based on reservations.
def show_bill(customer_id):
   
    reservations = models.get_reservations_for_customer(customer_id)
    if not reservations:
        print("No reservations found for this customer.")
        return
    
    def calculate_total_bill(reservations, get_rooms):
        def compute_bill(reservation):
            room_number, room_type, check_in, check_out = reservation
            room = models.find(get_rooms(), lambda x: x["roomNumber"] == room_number)
            if room:
                room_price = room["price"]
                days_stayed = (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days
                return room_price * days_stayed
            return 0
        transform_fn = lambda acc, reservation: acc + compute_bill(reservation)
        return reduce_bltin(transform_fn, reservations, 0)
    total_bill = calculate_total_bill(reservations,models.get_rooms)    
    print(f"Total bill for customer {customer_id}: ${total_bill}")


# Menu options.
models.create_tables()  # Run this once to create the tables

# Main loop for manual testing
while True:
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
