import { Box } from '@mui/material';
import MainCard from 'components/MainCard';
import { Add } from '@mui/icons-material';

const AddHouse = () => (
  <MainCard link={`/dashboard/houses/add`} contentSX={{ p: 2.0, height: "100%" }}>
    <Box sx={{ display: 'flex', flexDirection: "column", justifyContent: 'center', alignItems: 'center', height: "100%" }}>
      <Add color="primary" sx={{height: "100%", width: "100%", opacity: 0.5 }} />
    </Box>
  </MainCard>
);

export default AddHouse;
