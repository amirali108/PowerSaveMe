import { Box, Stack } from '@mui/material';
import Typography from 'themes/overrides/Typography';

const NotFound = ({ Icon, title }) => (
  <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
    <Stack spacing={1} justifyContent="center" alignItems="center">
      <Icon color="secondary" sx={{ height: '64px', width: '64px' }} />
      <Typography variant="h3" align="center" component="div" color="textSecondary">
        {title}
      </Typography>
    </Stack>
  </Box>
);


export default NotFound;