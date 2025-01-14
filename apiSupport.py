from flask import Flask, request 
import Models as models
from flask_restful import Resource,Api,reqparse,fields,marshal_with

app= Flask(__name__)
api =Api(app)
rooms_args = reqparse.RequestParser()
rooms_args.add_argument('roomNumber',type=int, required=True ) 
rooms_args.add_argument('roomType',type=str, required=True ) 
rooms_args.add_argument('price',type=int, required=True ) 
rooms_args.add_argument('availability',type=bool, required=True ) 

customers_args = reqparse.RequestParser()
customers_args.add_argument('name',type=str, required=True )  
customers_args.add_argument('contact',type=int, required=True ) 
customers_args.add_argument('payment',type=str, required=True ) 

reservations_args = reqparse.RequestParser()
reservations_args.add_argument('customer',type=str, required=True )
reservations_args.add_argument('roomNumber',type=int, required=True )
reservations_args.add_argument('checkIn',type=str, required=True )
reservations_args.add_argument('checkOut',type=str, required=True )


rooms_fields={
    'roomNumber':fields.Integer,
    'roomType':fields.String,
    'price':fields.Integer,
    'availability':fields.Boolean,
}
customers_fields={
    'id':fields.Integer,
    'name':fields.String,
    'contact':fields.Integer,
    'payment':fields.String,
}

reservation_fields = {
    'roomNumber': fields.Integer,
    'roomType': fields.String,
    'customer_id': fields.Integer,
    'checkIn': fields.String,
    'checkOut': fields.String
}

class Rooms(Resource):
    @marshal_with(rooms_fields)
    def get(self):
            data = models.get_rooms()
            print("API Response:", data)  # Debugging
            return data
    
    @marshal_with(rooms_fields)
    def post(self):
        args= rooms_args.parse_args()
        models.add_room_to_db(args['roomNumber'],args['roomType'],args['price'],args['availability'])
        return 201

class Room(Resource):
    @marshal_with(rooms_fields)
    def delete(self,id):
        models.delete_room_from_db(id)
        return models.get_rooms()
    
    @marshal_with(rooms_fields)
    def put(self,id):
        models.checkout(id)
        return models.get_rooms()

class Customers(Resource):
    @marshal_with(customers_fields)  
    def get(self):
        data = models.get_customers()
        print("API Response:", data)  # Debugging
        return data
    
    @marshal_with(customers_fields)  
    def post(self):
        args= customers_args.parse_args()
        models.add_customer_to_db(args['name'],args['contact'],args['payment'])
        return 201

class Customer(Resource):
    @marshal_with(customers_fields)
    def delete(self,id):
        models.delete_customer_from_db(id)
        return models.get_rooms()
    
class Reservations(Resource):
    @marshal_with(reservation_fields)  
    def get(self):
        data = models.get_reservations()
        print("API Response:", data)  # Debugging
        return data      

    @marshal_with(reservation_fields)  
    def post(self):
        args= reservations_args.parse_args()
        models.add_reservation_to_db(args['customer'],args['roomNumber'],args['checkIn'],args['checkOut'])
        return 201     

    
class Reservation(Resource):
    @marshal_with(reservation_fields)  
    def get(self,id):
        data = models.get_reservations_for_customer(id)
        print("API Response:", data)  # Debugging
        return data
    
    @marshal_with(reservation_fields)
    def delete(self,id):
        models.delete_reservation_from_db(id)
        return models.get_rooms()


        

    

api.add_resource(Rooms,'/')
api.add_resource(Room,'/Room/<int:id>')
api.add_resource(Customers,'/Customers')
api.add_resource(Customer,'/Customers/<int:id>')
api.add_resource(Reservations,'/Reservations')
api.add_resource(Reservation,'/Reservations/<int:id>')


   






if __name__ =="__main__":
    app.run(debug=True)
    