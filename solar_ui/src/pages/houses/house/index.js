import { Stack } from '@mui/material';
import useLocalStorage from 'use-local-storage';
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';

const House = () => {
  const [houses] = useLocalStorage('houses', []);
  const { id } = useParams();
  const getHouse = () => {
    const house = houses.find((house) => house.id == id);
    return house;
  };
  const [house, setHouse] = useState(null);

  useEffect(() => {
    setHouse(getHouse());
  }, [])
  
  useEffect(() => {
    setHouse(getHouse());
  }, [houses, id]);

  if (!house) return <div>House not found</div>;

  return (
    <Stack spacing={0.5} direction="row" justifyContent="space-between">
      <Stack justifyContent="center" spacing={2}></Stack>
      <Stack justifyContent="center" spacing={2}></Stack>
      <Stack justifyContent="center" spacing={2}></Stack>
    </Stack>
  );
};

export default House;
