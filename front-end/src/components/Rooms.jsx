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
    <div className="relative overflow-x-auto p-4">
  <h1 className="text-xl font-bold mb-4">Available Rooms</h1>
  <table className="table-auto w-full border-collapse border border-gray-300">
    <thead className="bg-gray-100">
      <tr>
        <th className="border border-gray-300 px-4 py-2 text-left font-semibold">Room Number</th>
        <th className="border border-gray-300 px-4 py-2 text-left font-semibold">Type</th>
        <th className="border border-gray-300 px-4 py-2 text-left font-semibold">Price</th>
        <th className="border border-gray-300 px-4 py-2 text-left font-semibold">Availability</th>
      </tr>
    </thead>
    <tbody>
      {rooms.map((room) => (
        <tr key={room.roomNumber} className="hover:bg-gray-50">
          <td className="border border-gray-300 px-4 py-2">{room.roomNumber}</td>
          <td className="border border-gray-300 px-4 py-2">{room.roomType}</td>
          <td className="border border-gray-300 px-4 py-2">{room.price}</td>
          <td
            className={`border border-gray-300 px-4 py-2 font-medium ${
              room.availability === "Available" ? "text-green-600" : "text-red-600"
            }`}
          >
            {room.availability}
          </td>
        </tr>
      ))}
    </tbody>
  </table>
</div>

  )
}

export default Rooms;