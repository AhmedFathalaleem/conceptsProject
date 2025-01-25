import React from 'react'

const RoomCard = ({roomType, price, availability}) => {
  return (
    <div className='relative border rounded-lg p-4 shadow-lg bg-white max-w-sm'>
        <h3 className='text-xl font-bold mb-2'>{roomType}</h3>
        <p className='text-lg text-grey-700 mb-1 font-semibold'>${price} per night</p>
        <p className={`text-md ${availability ? "text-green-500" : "text-red-500"}`}>
        {availability ? "Available" : "Unavailable"}
        </p>
      <button className={`mt-4 px-4 py-2 rounded-lg text-white font-semibold
       ${availability ? "bg-blue-500 hover:bg-blue-600" : "bg-gray-400 cursor-not-allowed"}`}
        disabled={!availability}>
        Book Now
      </button>
    </div>
  )
}

export default RoomCard