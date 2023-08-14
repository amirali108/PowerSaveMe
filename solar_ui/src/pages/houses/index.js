//import { useState } from 'react';
import { Grid, Typography } from '@mui/material';
import AddHouse from 'components/cards/AddHouse';
import HouseCard from 'components/cards/House';
import useLocalStorage from 'use-local-storage';

const Houses = () => {
  const [houses] = useLocalStorage('houses', []);

  return (
    <Grid container rowSpacing={4.5} columnSpacing={2.75}>
      <Grid item xs={12} sx={{ mb: -2.25 }}>
        <Typography variant="h5">Your houses</Typography>
      </Grid>

      {houses.map((house, index) => (
        <Grid key={index} item xs={12} sm={6} md={4} lg={3} xl={2}>
          <HouseCard house={house} />
        </Grid>
      ))}
      <Grid item xs={12} sm={6} md={4} lg={3} xl={2}>
        <AddHouse />
      </Grid>
    </Grid>
  );
};

export default Houses;
