import React, { useState, useEffect, useContext } from 'react';
import ListItem from '../components/ListItem';
import AddButton from '../components/AddButton';
import DownloadButton from '../components/DownloadButton';
import AuthContext from '../context/AuthContext';
import FilterParameters from '../components/FilterParameters';
import './ParametersListPage.css'; 

const ParametersListPage = () => {
  const [parameters, setParameters] = useState([]);
  const [filterData, setFilterData] = useState({});
  const { authTokens, logoutUser } = useContext(AuthContext);

  useEffect(() => {
    getParameters();
  }, [filterData]);

  const getParameters = async () => {
    try {
      // Формируем URL запроса с учетом фильтров
      const url = new URL('https://envtrack.ru/api/parameters/');
      
      if (filterData.responsible) {
        url.searchParams.append('responsible', filterData.responsible);
      }
      if (filterData.room) {
        url.searchParams.append('room', filterData.room);
      }
      // Добавляем фильтр по дате, если выбрана дата
      if (filterData.date) {
        url.searchParams.append('date', filterData.date);
      }
  
      const response = await fetch(url.toString(), {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + String(authTokens.access),
        },
      });
      const data = await response.json();
  
      if (response.status === 200) {
        setParameters(data);
      } else if (response.status === 401) {
        logoutUser();
      }
    } catch (error) {
      console.error('Error fetching parameters:', error);
    }
  };

  return (
    <div className='page-container'>
      <FilterParameters onFilterChange={setFilterData} onResetFilters={() => setFilterData({})} />
      <div className='parameters-list'>
        {parameters.map((parameter, index) => (
          <ListItem key={index} parameter={parameter} />
        ))}
      </div>
      <DownloadButton />
      <AddButton />

    </div>
  );
};

export default ParametersListPage;