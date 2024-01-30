import React, { useState, useEffect, useContext } from 'react';
import AuthContext from '../context/AuthContext';
import './FilterParameters.css';

const FilterParameters = ({ onFilterChange, onResetFilters }) => {
  const [selectedResponsible, setSelectedResponsible] = useState('');
  const [selectedRoom, setSelectedRoom] = useState('');
  const [selectedDate, setSelectedDate] = useState('');

  const [responsibles, setResponsibles] = useState([]);
  const [rooms, setRooms] = useState([]);
  const { authTokens } = useContext(AuthContext);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const responsiblesResponse = await fetch('https://envtrack.ru/api/responsibles/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + String(authTokens.access),
          },
        });

        if (responsiblesResponse.ok) {
          const responsiblesData = await responsiblesResponse.json();
          setResponsibles(responsiblesData);
        }

        const roomsResponse = await fetch('https://envtrack.ru/api/rooms/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + String(authTokens.access),
          },
        });

        if (roomsResponse.ok) {
          const roomsData = await roomsResponse.json();
          setRooms(roomsData);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [authTokens.access]);

  const handleFilterChange = () => {
    const filters = {
      responsible: selectedResponsible,
      room: selectedRoom,
      date: selectedDate,
    };
    onFilterChange(filters);
  };

  const handleResetFilters = () => {
    setSelectedResponsible('');
    setSelectedRoom('');
    setSelectedDate('');
    onResetFilters();
  };

  return (
    <div className="filter-parameters">
      <select
        value={selectedResponsible}
        onChange={(e) => setSelectedResponsible(e.target.value)}
      >
        <option value="">Выберите ответственного</option>
        {responsibles.map((responsible) => (
          <option key={responsible.id} value={responsible.id}>
            {responsible.last_name} 
          </option>
        ))}
      </select>

      <select
        value={selectedRoom}
        onChange={(e) => setSelectedRoom(e.target.value)}
      >
        <option value="">Выберите помещение</option>
        {rooms.map((room) => (
          <option key={room.id} value={room.id}>
            {room.room_number} 
          </option>
        ))}
      </select>

      <input
        type="date"
        value={selectedDate}
        onChange={(e) => setSelectedDate(e.target.value)}
      />

      <button className="apply-button" onClick={handleFilterChange}>
        Применить фильтры
      </button>

      <button className="reset-button" onClick={handleResetFilters}>
        Сбросить фильтры
      </button>
    </div>
  );
};

export default FilterParameters;