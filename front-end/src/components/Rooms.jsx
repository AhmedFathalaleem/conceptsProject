import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Table from './Table';

const Rooms = () => {
  const [rooms, setRooms] = useState([]);

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

  // Define the columns for the table
  const columns = [
    {
      header: 'Room Number',
      accessor: 'roomNumber',
    },
    {
      header: 'Type',
      accessor: 'roomType',
    },
    {
      header: 'Price',
      accessor: 'price',
    },
    {
      header: 'Availability',
      accessor: 'availability',
      cellStyle: (availability) =>
        availability === 'Available' ? 'text-green-600 font-medium' : 'text-red-600 font-medium',
    },
  ];

  return <Table data={rooms} columns={columns} title="Available Rooms" />;
};

export default Rooms;
