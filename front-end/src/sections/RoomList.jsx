import React, { useEffect, useState } from 'react'
import RoomCard from '../components/RoomCard'

const RoomList = () => {
    const [rooms, setRooms] = useState([]);
    useEffect (() => {
        const fetchRooms = async () => {
            try {
                const response = await fetch ("http://127.0.0.1:5000/");
                const data = await response.json();
                setRooms(data);
            } catch(error) {
                console.error('Error fetching rooms', error);
            }
        };
        fetchRooms();
    })


    
    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 p-4">
          {rooms.map((room) => (
            <RoomCard
              key={room.roomNumber}
              roomType={room.roomType}
              price={room.price}
              availability={room.availability}
            />
          ))}
        </div>
      );
    };
    
    export default RoomList;