import sqlite3
from functools import reduce
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
    #Find an item in a collection based on a condition.
    return next(filter(condition_fn, data), None)

def update_data(data, condition_fn, update_fn):
    #Update items in a collection based on a condition.
    return list(map(lambda item: update_fn(item) if condition_fn(item) else item, data))













# Database Functions

def execute_query(query, params=(), fetch=False, many=False):
    # Function to execute database queries safely.
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









# DB get functions 
def get_rooms():
    query = 'SELECT * FROM rooms'
    result = execute_query(query, fetch=True)
    if result is None:
        return []
    return list(map(lambda room: {"roomNumber": room[0], "roomType": room[1], "price": room[2], "availability": room[3]}, result or []))

def get_customers():
    query = 'SELECT * FROM customers'
    result = execute_query(query, fetch=True)
    if result is None:
        return []
    
    return list(map(lambda customer: {"id": customer[0], "name": customer[1], "contact": customer[2], "payment": customer[3]}, result))

def get_reservations_for_customer(customer_id):
    query = '''
        SELECT r.roomNumber, r.roomType, res.checkIn, res.checkOut
        FROM reservations res
        JOIN rooms r ON res.roomNumber = r.roomNumber
        WHERE res.customer_id = ?
    '''
    result = execute_query(query, (customer_id,), fetch=True)
    return result or []











def add_room_to_db(room_number, room_type, price, availability):
    query = 'INSERT INTO rooms (roomNumber, roomType, price, availability) VALUES (?, ?, ?, ?)'
    execute_query(query, (room_number, room_type, price, availability))
    print(f"Room {room_number} added successfully!")

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
        list(map(lambda room: checkout_room_from_db(room[0]), reserved_rooms))

    
    delete_customer_query = 'DELETE FROM customers WHERE id = ?'
    execute_query(delete_customer_query, (customer_id,))
    print(f"Customer with ID {customer_id} and their reservations deleted successfully!")
















# Main Application Functions

# Retrieve and display available rooms.
def available_rooms():
    rooms = get_rooms()
    return list(filter(lambda room: room["availability"], rooms))
























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
    room_info = map(lambda room: f"Room {room['roomNumber']} - {room['roomType']} - ${room['price']}", rooms)
    print("\n".join(room_info))

    try:
        reservation_details = input_reservation_details()
        # check check out date < check in date
        daysnum = (datetime.strptime(reservation_details["check_out"], "%Y-%m-%d") - datetime.strptime(reservation_details["check_in"], "%Y-%m-%d")).days
        if daysnum <=0:
            print("Wrong date")
            return
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

















def add_customer():
    try:
        name = input("Enter customer name: ")
        contact = input("Enter customer contact: ")
        payment = input("Enter payment method (e.g., cash, credit card): ")
        add_customer_to_db(name, contact, payment)
        print(f"Customer {name} added successfully!")
    except Exception as e:
        print(f"Error adding customer: {e}")


# Get and display customers inforamtion.
def show_customers():
    try:
        # Get customers and map them to their formatted details
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
















 #Function to calculate and show the customer's bill based on reservations.
def show_bill(customer_id):
   
    reservations = get_reservations_for_customer(customer_id)
    if not reservations:
        print("No reservations found for this customer.")
        return
    
    def calculate_total_bill(reservations, get_rooms):
        def compute_bill(reservation):
            room_number, room_type, check_in, check_out = reservation
            room = find(get_rooms(), lambda x: x["roomNumber"] == room_number)
            if room:
                room_price = room["price"]
                days_stayed = (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days
                return room_price * days_stayed
            return 0
        return reduce(lambda acc, reservation: acc + compute_bill(reservation), reservations, 0)
    total_bill = calculate_total_bill(reservations,get_rooms)    
    print(f"Total bill for customer {customer_id}: ${total_bill}")






















# Menu options.
def main_menu():
    return {
        "1": ("Add Customer", lambda: add_customer()),
        "2": ("Make Reservation", lambda: make_reservation()),
        "3": ("Check Out", lambda: checkout()),
        "4": ("View Available Rooms", view_available_rooms),
        "5": ("Add Room", lambda: add_room()),
        "6": ("Delete Room", lambda: delete_room()),
        "7": ("Show Customers", lambda: show_customers()),
        "8": ("Delete Customer", lambda: delete_customer()),
        "9": ("Show Bill", lambda: show_bill(int(input("Enter customer ID to view the bill: ")))),
        "10": ("Exit", lambda: "exit")
    }

def view_available_rooms():
    rooms = get_rooms()
    available_rooms = filter(lambda room: room["availability"], rooms)
    formatted_rooms = map(lambda room: f"Room {room['roomNumber']} - {room['roomType']} - ${room['price']}", available_rooms)
    print("\nAvailable Rooms:")
    print("\n".join(formatted_rooms))

def run_menu(menu):
    """Recursively display the menu and execute selected options."""
    print("\nMenu:")
    for key, (description, _) in menu.items():
        print(f"{key}. {description}")
    
    choice = input("Choose an option: ").strip()
    selected_option = menu.get(choice)

    if selected_option:
        _, action = selected_option
        result = action()  # Perform the action
        if result == "exit":
            print("Exiting...")
            return
    else:
        print("Invalid option, please try again.")
    
    # Recursively call the menu
    run_menu(menu)

# Run the program
if __name__ == "__main__":
    create_tables()  # Initialize tables
    run_menu(main_menu())
