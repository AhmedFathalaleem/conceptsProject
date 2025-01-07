from flask import Flask, request , jsonify
import imparativeHotel as IH
from flask_restful import Resource,Api,reqparse,fields,marshal_with,abort
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

class Rooms(Resource):
    @marshal_with(rooms_fields)
    def get(self):
            data = IH.get_rooms()
            print("API Response:", data)  # Debugging
            return data
    
    @marshal_with(rooms_fields)
    def post(self):
        args= rooms_args.parse_args()
        IH.add_room_to_db(args['roomNumber'],args['roomType'],args['price'],args['availability'])
        return 201

class extra(Resource):
    @marshal_with(rooms_fields)
    def delete(self,id):
        IH.delete_room_from_db(id)
        return IH.get_rooms()

class Customers(Resource):
    @marshal_with(customers_fields)  
    def get(self):
        data = IH.get_customers()
        print("API Response:", data)  # Debugging
        return data

class extra2(Resource):
    @marshal_with(customers_fields)
    def delete(self,id):
        IH.delete_customer_from_db(id)
        return IH.get_rooms()
        
    @marshal_with(customers_fields)  
    def post(self):
        args= customers_args.parse_args()
        IH.add_customer_to_db(args['name'],args['contact'],args['payment'])
        return 201
    

api.add_resource(Rooms,'/')
api.add_resource(extra,'/Room/<int:id>')
api.add_resource(Customers,'/Customers')
api.add_resource(extra2,'/Customers/<int:id>')

   






if __name__ =="__main__":
    app.run(debug=True)
    