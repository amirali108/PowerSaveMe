
import { Grid, Typography, Stack } from '@mui/material';
import HouseForm from './HouseForm';


const AddHouse = () => {

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Stack direction="row" justifyContent="space-between" alignItems="baseline" sx={{ mb: { xs: -0.5, sm: 0.5 } }}>
          <Typography variant="h3">Add a house</Typography>
        </Stack>
      </Grid>
      <Grid item xs={12}>
        <HouseForm />
      </Grid>
    </Grid>
  );
};

export default AddHouse;
