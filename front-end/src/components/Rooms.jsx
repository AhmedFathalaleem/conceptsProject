import React, { useEffect, useState } from 'react';
import axios from 'axios'
const Rooms = () => {
    const [rooms, setRooms] = React.useState([]);

    useEffect(() => {
        const fetchRooms = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/');

                setRooms(response.data);
            } catch (error) {
                console.error('Error fetching rooms', error);
            }
        };
        fetchRooms(); 
    }, []); 
    

  return (
    <div>
            <h1>Available Rooms</h1>
            {rooms.map(room => (
                <div key={room.roomNumber}>
                    <h2>Room Number: {room.roomNumber}</h2>
                    <p>Type: {room.roomType}</p>
                    <p>Price: {room.price}</p>
                    <p>Availability: {room.availability}</p>
                </div>
            ))}
        </div>
  )
}

export default Rooms;