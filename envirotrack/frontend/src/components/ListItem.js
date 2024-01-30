// ListItem.js
import React from 'react';
import { Link } from 'react-router-dom';
import './ListItem.css';

const renderParameterSets = (parameterSets) => {
  if (!parameterSets || parameterSets.length === 0) return '-';

  return parameterSets.map((paramSet, index) => (
    <div key={index} className="parameter-set">
      <div className="parameter-item">
        <span>Набор {index + 1}:</span>
        <span> Температура: </span> {paramSet.temperature_celsius},
        <span> Влажность: </span> {paramSet.humidity_percentage},
        <span> Давление (кПа): </span> {paramSet.pressure_kpa},
        <span> Давление (мм рт. ст.): </span> {paramSet.pressure_mmhg},
        <span> Время создания: </span> {paramSet.time}
      </div>
    </div>
  ));
};

const ListItem = ({ parameter }) => {
  const getTime = (dateString) => {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate() - 1).padStart(2, '0');
  
    return `${day}.${month}.${year}`;
  };

  return (
    <Link to={`/parameter/${parameter.id}`}>
      <div className="parameters-list-item">
        <h3>Помещение: {parameter.room.room_number} | Ответственный: {parameter.responsible.first_name} {parameter.responsible.last_name}</h3>
        <div className="parameters-and-info">
          <div className="parameters">
            {renderParameterSets(parameter.parameter_sets)}
          </div>
          <div className="info">
            <div className="parameter-item">
              <span>Дата и время:</span> {getTime(parameter.created_at)}
            </div>
            <div className="parameter-item">
              <span>Средство измерения:</span> {parameter.measurement_instrument ? 
                `${parameter.measurement_instrument.name} ${parameter.measurement_instrument.type} ${parameter.measurement_instrument.serial_number}` : 
                'Нет информации'
              }
          </div>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default ListItem;