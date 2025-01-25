import NavBar from "./components/NavBar";
import Rooms from "./components/Rooms";
import Customers from "./components/Customers";
import MakeReservation from "./components/MakeReservation";
import RoomList from "./sections/RoomList";

export default function App() {
  return (
    <>
    <NavBar />
    <RoomList />
    <Customers />
    <MakeReservation />
    
    </>
    
  )
}