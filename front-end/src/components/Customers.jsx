import React, { useState, useEffect } from 'react';
import axios from 'axios'
import Table from './Table';
const Customers = () => {

    const [customers, SetCustomers] = React.useState([]);

    useEffect(() =>{
        const fetchCustomers = async () => {
            try{
                const response = await axios.get('http://127.0.0.1:5000/Customers');

                SetCustomers(response.data);
            } catch (error) {
                console.error('Error fetching Customers', error);
            }
        };
        fetchCustomers();
    })


    const columns = [
        {
            header: 'Customer ID',
            accessor: 'id',
        },
        {
            header: 'Name',
            accessor: 'name',
        },
        {
            header: 'Contact number',
            accessor: 'contact',
        },
        {
            header: 'Payment method',
            accessor:  'payment',
        }
        
    ]



  return <Table data={customers} columns={columns} title="Customers" />;
}

export default Customers