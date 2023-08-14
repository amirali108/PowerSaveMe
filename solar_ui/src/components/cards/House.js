import PropTypes from 'prop-types';

// material-ui
import { Stack, Typography, Box } from '@mui/material';

// project import
import MainCard from 'components/MainCard';

import { BatteryAlert, BatteryChargingFull, Height, Kitchen } from '@mui/icons-material';
import HouseIcon from 'assets/images/house/HouseIcon';



const to_the_power_of = {
  position: 'relative',
  bottom: '1ex',
  fontSize: '80%'
};

const icon_style = {
  height: '32px',
  width: '32px'
};

const icon_text_props = {
  component: 'span',
  sx: { display: 'flex', flexDirection: 'center', justifyContent: 'center', alignItems: 'center' },
  textAlign: 'center',
  variant: 'body2',
  color: 'textSecondary'
};

const House = ({house}) => (
  <MainCard link={`/dashboard/houses/${house.id}`} contentSX={{ p: 2.25 }}>
    <Stack spacing={0.5} direction="row" justifyContent="space-between">
      <Stack justifyContent="center" spacing={2}>
        <Stack spacing={0.5} direction="row" alignItems="center">
          <Typography component="span" textAlign="center" variant="body2" color="textSecondary">
            {house.adress}
          </Typography>
        </Stack>
        <HouseIcon height={100} width={100} />
      </Stack>

      <Stack spacing={2}>
        <Stack direction="row" spacing={1} justifyContent="space-between">
          {!house.has_battery && house.batteries.length === 0 ? (
            <>
              <Typography {...icon_text_props}>No batteries</Typography>
              <Box>
                <BatteryAlert color="error" sx={{ height: icon_style.height, width: icon_style.width }} />
              </Box>
            </>
          ) : (
            <>
              <Typography {...icon_text_props}>
                {house.batteries.length} {house.batteries.length === 1 ? 'battery' : 'batteries'}
              </Typography>
              <Box>
                <BatteryChargingFull color="success" sx={{ height: icon_style.height, width: icon_style.width }} />
              </Box>
            </>
          )}
        </Stack>
        <Stack direction="row" spacing={1}>
          <Typography {...icon_text_props}>
            {house.size} m<span style={to_the_power_of}>2</span>
          </Typography>
          <Box>
            <Height sx={{ height: icon_style.height, width: icon_style.width }} />
          </Box>
        </Stack>

        <Stack direction="row" spacing={1}>
          <Typography {...icon_text_props}>
            {house.devices.length} {house.devices.length === 1 ? 'device' : 'devices'}
          </Typography>
          <Box>
            <Kitchen color="info" sx={{ height: icon_style.height, width: icon_style.width }} />
          </Box>
        </Stack>
      </Stack>
    </Stack>
    <Box sx={{ pt: 2.25 }}>
      <Typography textAlign="center" textTransform="capitalize" variant="h5" color="textSecondary">
        {house.name}
      </Typography>
    </Box>
  </MainCard>
);

House.propTypes = {
  house: PropTypes.array.isRequired
};

House.defaultProps = {
  color: 'primary'
};

export default House;
