import sqlite3

import sqlite3

def create_connection():
    try:
        conn = sqlite3.connect('hotel.db')  # Creates or opens the hotel.db file
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def create_tables():
    conn = create_connection()
    if conn is None:
        return
    try:
        with conn:
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
                contact TEXT
            )''')
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")
    finally:
        conn.close()

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

def checkout_room_from_db(room_number):
    delete_reservation_query = 'DELETE FROM reservations WHERE roomNumber = ?'
    update_room_query = 'UPDATE rooms SET availability = ? WHERE roomNumber = ?'
    
    execute_query(delete_reservation_query, (room_number,))
    execute_query(update_room_query, (True, room_number))
    print(f"Room {room_number} checked out successfully!")