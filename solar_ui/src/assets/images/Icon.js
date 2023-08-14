import { Box } from '@mui/material';
import PropTypes from 'prop-types';
const Icon = ({ height, width, children }) => {
  return (
    <Box height={height} width={width}>
      <svg height={height} width={width} viewBox={`0 0 ${height * 6} ${width * 6}`} fill="none" xmlns="http://www.w3.org/2000/svg">
        {children}
      </svg>
    </Box>
  );
};

Icon.PropTypes = {
  height: PropTypes.number,
  width: PropTypes.number
};

export default Icon;
