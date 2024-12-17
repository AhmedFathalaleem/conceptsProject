import sqlite3
from datetime import datetime
# Database Setup Functions

def create_connection():
    try:
        conn = sqlite3.connect('hotel.db')  # Creates or opens the hotel.db file
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def create_tables():
    try:
        conn = create_connection()
        if conn is None:
            return
        cursor = conn.cursor()
        
        # Create rooms table
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS rooms (
            roomNumber INTEGER PRIMARY KEY,
            roomType TEXT,
            price INTEGER,
            availability BOOLEAN
        )''')
        
        # Create customers table
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT,
            payment TEXT
        )''')
        
        # Create reservations table
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            roomNumber INTEGER,
            checkIn TEXT,
            checkOut TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (roomNumber) REFERENCES rooms(roomNumber)
        )''')

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

# Utility Functions

def find(data, condition_fn):
    """Find an item in a collection based on a condition."""
    return next((item for item in data if condition_fn(item)), None)

def update_data(data, condition_fn, update_fn):
    """Update items in a collection based on a condition."""
    return [update_fn(item) if condition_fn(item) else item for item in data]

# Database Functions

def execute_query(query, params=(), fetch=False, many=False):
    """Helper function to execute database queries safely."""
    try:
        conn = create_connection()
        if conn is None:
            return None
        cursor = conn.cursor()
        if many:
            cursor.executemany(query, params)
        else:
            cursor.execute(query, params)
        if fetch:
            result = cursor.fetchall()
        else:
            result = None
        conn.commit()
        conn.close()
        return result
    except sqlite3.Error as e:
        print(f"Database query error: {e}")
        return None

def get_rooms():
    query = 'SELECT * FROM rooms'
    result = execute_query(query, fetch=True)
    if result is None:
        return []
    return [{"roomNumber": room[0], "roomType": room[1], "price": room[2], "availability": room[3]} for room in result]

def get_customers():
    query = 'SELECT * FROM customers'
    result = execute_query(query, fetch=True)
    if result is None:
        return []
    return [{"id": customer[0], "name": customer[1], "contact": customer[2], "payment": customer[3]} for customer in result]

def get_reservations_for_customer(customer_id):
    query = '''
        SELECT r.roomNumber, r.roomType, res.checkIn, res.checkOut
        FROM reservations res
        JOIN rooms r ON res.roomNumber = r.roomNumber
        WHERE res.customer_id = ?
    '''
    result = execute_query(query, (customer_id,), fetch=True)
    return result or []

def add_customer_to_db(name, contact, payment):
    query = 'INSERT INTO customers (name, contact, payment) VALUES (?, ?, ?)'
    execute_query(query, (name, contact, payment))

def add_reservation_to_db(customer_name, room_number, check_in, check_out):
    customer_query = 'SELECT id FROM customers WHERE name = ?'
    customer_id_result = execute_query(customer_query, (customer_name,), fetch=True)
    if not customer_id_result:
        return "Customer not found."
    
    customer_id = customer_id_result[0][0]
    reservation_query = 'INSERT INTO reservations (customer_id, roomNumber, checkIn, checkOut) VALUES (?, ?, ?, ?)'
    update_query = 'UPDATE rooms SET availability = ? WHERE roomNumber = ?'
    
    execute_query(reservation_query, (customer_id, room_number, check_in, check_out))
    execute_query(update_query, (False, room_number))
    return "Reservation added successfully!"

def checkout_room_from_db(room_number):
    delete_query = 'DELETE FROM reservations WHERE roomNumber = ?'
    update_query = 'UPDATE rooms SET availability = ? WHERE roomNumber = ?'
    
    execute_query(delete_query, (room_number,))
    execute_query(update_query, (True, room_number))
    return "Checked out successfully!"

def delete_room_from_db(room_number):
    delete_room_query = 'DELETE FROM rooms WHERE roomNumber = ?'
    delete_reservations_query = 'DELETE FROM reservations WHERE roomNumber = ?'
    
    execute_query(delete_reservations_query, (room_number,))
    execute_query(delete_room_query, (room_number,))
    print(f"Room {room_number} deleted successfully!")

def delete_customer_from_db(customer_id):
    reservation_query = 'SELECT roomNumber FROM reservations WHERE customer_id = ?'
    reserved_rooms = execute_query(reservation_query, (customer_id,), fetch=True)
    if reserved_rooms:
        for room in reserved_rooms:
            room_number = room[0]
            checkout_room_from_db(room_number)
    
    delete_customer_query = 'DELETE FROM customers WHERE id = ?'
    execute_query(delete_customer_query, (customer_id,))
    print(f"Customer with ID {customer_id} and their reservations deleted successfully!")

# Main Application Functions

def add_customer():
    try:
        name = input("Enter customer name: ")
        contact = input("Enter customer contact: ")
        payment = input("Enter payment method (e.g., cash, credit card): ")
        add_customer_to_db(name, contact, payment)
        print(f"Customer {name} added successfully!")
    except Exception as e:
        print(f"Error adding customer: {e}")

def available_rooms():
    """Retrieve and display available rooms."""
    rooms = get_rooms()
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
        message = add_reservation_to_db(
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
        message = checkout_room_from_db(room_number)
        print(message)
    except ValueError:
        print("Invalid input. Please enter a valid room number.")
    except Exception as e:
        print(f"Error during checkout: {e}")

def add_room_to_db(room_number, room_type, price, availability):
    query = 'INSERT INTO rooms (roomNumber, roomType, price, availability) VALUES (?, ?, ?, ?)'
    execute_query(query, (room_number, room_type, price, availability))
    print(f"Room {room_number} added successfully!")

def add_room():
    try:
        room_number = int(input("Enter room number: "))
        room_type = input("Enter room type (single, double, suite, etc.): ")
        price = int(input("Enter price per night: "))
        availability = input("Is the room available? (yes/no): ").strip().lower() == "yes"
        add_room_to_db(room_number, room_type, price, availability)
    except ValueError:
        print("Invalid input. Please enter valid data.")
    except Exception as e:
        print(f"Error adding room: {e}")

def delete_room():
    try:
        room_number = int(input("Enter room number to delete: "))
        delete_room_from_db(room_number)
    except ValueError:
        print("Invalid input. Please enter a valid room number.")
    except Exception as e:
        print(f"Error deleting room: {e}")

def show_customers():
    """Functionally retrieve and display customer details with their reservations."""
    try:
        # Retrieve customers and map them to their formatted details
        def format_customer(customer):
            # Get reservations for the customer
            reservations = get_reservations_for_customer(customer["id"])
            # Format the rented rooms
            rooms_rented = [
                f"Room {reservation[0]} - {reservation[1]}" for reservation in reservations
            ]
            return {
                "id": customer["id"],
                "name": customer["name"],
                "contact": customer["contact"],
                "payment": customer["payment"],
                "rooms_rented": rooms_rented
            }

        customers = get_customers()
        formatted_customers = list(map(format_customer, customers))

        # Create output for each customer
        def format_output(customer):
            customer_info = f"ID: {customer['id']}, Name: {customer['name']}, Contact: {customer['contact']}, Payment: {customer['payment']}"
            if customer["rooms_rented"]:
                rooms_info = "\n  Rooms rented:\n    " + "\n    ".join(customer["rooms_rented"])
            else:
                rooms_info = "\n  No rooms rented."
            return customer_info + rooms_info

        # Generate the final output
        output = "\nList of Customers:\n" + "\n\n".join(map(format_output, formatted_customers))

        # Display the output
        print(output)

    except Exception as e:
        print(f"Error displaying customers: {e}")


def delete_customer():
    try:
        customer_id = int(input("Enter customer ID to delete: "))
        delete_customer_from_db(customer_id)
    except ValueError:
        print("Invalid input. Please enter a valid customer ID.")
    except Exception as e:
        print(f"Error deleting customer: {e}")

def show_bill(customer_id):
    """Function to calculate and show the customer's bill based on reservations."""
    # Get reservations for the customer
    reservations = get_reservations_for_customer(customer_id)
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
        rooms = get_rooms()
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
create_tables()  # Run this once to create the tables

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
            rooms = get_rooms()
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
