import * as Yup from 'yup';
import { Formik, FieldArray } from 'formik';
import {
  Button,
  Grid,
  InputLabel,
  OutlinedInput,
  Stack,
  FormHelperText,
  Slider,
  ButtonBase,
  Box,
  Typography,
  IconButton,
  Select,
  MenuItem
} from '@mui/material';
import AnimateButton from 'components/@extended/AnimateButton';
import { Delete } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import useLocalStorage from 'use-local-storage';

const HouseForm = () => {
  const [houses, setHouses] = useLocalStorage('houses', []);
  const navigate = useNavigate();

  const addHouse = async (house) => {
    let latest_id = 0;
    houses.forEach((house) => {
      if (house.id > latest_id) {
        latest_id = house.id;
      }
    });
    house.id = latest_id + 1;
    setHouses([...houses, house]);
  };

  return (
    <Formik
      initialValues={{
        name: '',
        size: 0,
        heating: '',
        heating_efficiency: 0,
        cooling_efficiency: 0,
        has_battery: false,
        adress: '',
        devices: [],
        batteries: []
      }}
      validationSchema={Yup.object().shape({
        name: Yup.string().max(255).required('A name is required'),
        adress: Yup.string().max(255).required('An adress is required'),
        size: Yup.number().required('A size is required')
      })}
      onSubmit={async (values, { setErrors, setStatus, setSubmitting }) => {
        try {
          setStatus({ success: false });
          setSubmitting(false);
        } catch (err) {
          setStatus({ success: false });
          setErrors({ submit: err.message });
          setSubmitting(false);
        }
        addHouse(values).then(() => {
          navigate(`/dashboard/houses/${houses[houses.length-1].id}`);
        });
      }}
    >
      {({ errors, handleBlur, handleChange, handleSubmit, isSubmitting, touched, values }) => (
        <form noValidate onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Stack spacing={1} direction="row" sx={{ width: '100%' }}>
                <Stack spacing={1} sx={{ width: '100%' }}>
                  <InputLabel htmlFor="form-name">House name</InputLabel>
                  <OutlinedInput
                    id="form-name"
                    type="text"
                    value={values.name}
                    name="name"
                    onBlur={handleBlur}
                    onChange={handleChange}
                    placeholder="Enter a house name"
                    fullWidth
                    error={Boolean(touched.name && errors.name)}
                  />
                  {touched.name && errors.name && (
                    <FormHelperText error id="standard-weight-helper-text-house-name">
                      {errors.name}
                    </FormHelperText>
                  )}
                </Stack>
                <Stack spacing={1} sx={{ width: '100%' }}>
                  <InputLabel htmlFor="form-size">House size (m^2)</InputLabel>
                  <OutlinedInput
                    id="form-size"
                    type="number"
                    value={values.size}
                    name="size"
                    onBlur={handleBlur}
                    onChange={handleChange}
                    placeholder="in m^2"
                    fullWidth
                    error={Boolean(touched.size && errors.size)}
                  />
                  {touched.size && errors.size && (
                    <FormHelperText error id="standard-weight-helper-text-house-size">
                      {errors.size}
                    </FormHelperText>
                  )}
                </Stack>
              </Stack>
            </Grid>
            <Grid item xs={12}>
              <Stack spacing={1} sx={{ width: '100%' }}>
                <InputLabel htmlFor="form-adress">House adress</InputLabel>
                <OutlinedInput
                  id="form-adress"
                  type="text"
                  value={values.adress}
                  name="adress"
                  onBlur={handleBlur}
                  onChange={handleChange}
                  placeholder="Adress, City"
                  fullWidth
                  error={Boolean(touched.adress && errors.adress)}
                />
                {touched.adress && errors.adress && (
                  <FormHelperText error id="standard-weight-helper-text-house-adress">
                    {errors.adress}
                  </FormHelperText>
                )}
              </Stack>
            </Grid>
            <Grid item xs={12}>
              <Stack spacing={4} direction="row" sx={{ width: '100%' }}>
                <Stack spacing={1} sx={{ width: '100%' }}>
                  <InputLabel htmlFor="form-heating">Heating efficiency</InputLabel>
                  <Slider
                    aria-label="Heating efficiency"
                    defaultValue={0.5}
                    valueLabelDisplay="auto"
                    name="heating_efficiency"
                    value={values.heating_efficiency}
                    onChange={handleChange}
                    step={0.1}
                    marks
                    min={0.0}
                    max={1.0}
                  />
                  {touched.heating_efficiency && errors.heating_efficiency && (
                    <FormHelperText error id="standard-weight-helper-text-house-heating_efficiency">
                      {errors.heating_efficiency}
                    </FormHelperText>
                  )}
                </Stack>
                <Stack spacing={1} sx={{ width: '100%' }}>
                  <InputLabel htmlFor="form-cooling">Cooling efficiency</InputLabel>
                  <Slider
                    aria-label="Cooling efficiency"
                    defaultValue={0.5}
                    valueLabelDisplay="auto"
                    name="cooling_efficiency"
                    value={values.cooling_efficiency}
                    onChange={handleChange}
                    step={0.1}
                    marks
                    min={0.0}
                    max={1.0}
                  />
                  {touched.cooling_efficiency && errors.cooling_efficiency && (
                    <FormHelperText error id="standard-weight-helper-text-house-cooling_efficiency">
                      {errors.cooling_efficiency}
                    </FormHelperText>
                  )}
                </Stack>
              </Stack>
            </Grid>
            <Grid item xs={12}>
              <Typography variant="h5" color="textSecondary">
                Batteries
              </Typography>
            </Grid>
            <FieldArray
              name="batteries"
              render={(arrayHelpers) => (
                <>
                  {values.batteries.map((battery, index) => (
                    <Grid item xs={12} key={index}>
                      <Stack spacing={1} direction="row" sx={{ width: '100%' }}>
                        <Stack spacing={1} sx={{ width: '100%' }}>
                          <InputLabel htmlFor="form-battery-name">Battery name</InputLabel>
                          <OutlinedInput
                            id="form-battery-name"
                            type="text"
                            value={battery.name}
                            name="name"
                            onBlur={handleBlur}
                            onChange={(e) => {
                              let new_battery = { ...values.batteries[index] };
                              new_battery.name = e.target.value;
                              arrayHelpers.replace(index, new_battery);
                            }}
                            placeholder="Enter a battery name"
                            fullWidth
                          />
                        </Stack>
                        <Stack spacing={1} sx={{ width: '100%' }}>
                          <InputLabel htmlFor="form-battery-capacity">Battery capacity</InputLabel>
                          <OutlinedInput
                            id="form-battery-capacity"
                            type="number"
                            value={battery.capacity}
                            name="capacity"
                            onBlur={handleBlur}
                            onChange={(e) => {
                              let new_battery = { ...values.batteries[index] };
                              new_battery.capacity = e.target.value;
                              arrayHelpers.replace(index, new_battery);
                            }}
                            placeholder="Enter a battery capacity"
                            fullWidth
                          />
                        </Stack>
                        <Stack spacing={1} sx={{ width: '100%', height: '100%', alignSelf: 'flex-end' }}>
                          <IconButton color="error" aria-label="delete" onClick={() => arrayHelpers.remove(index)}>
                            <Delete />
                          </IconButton>
                        </Stack>
                      </Stack>
                    </Grid>
                  ))}
                  <Grid item xs={12}>
                    <Stack spacing={1} sx={{ width: '100%' }}>
                      <ButtonBase
                        onClick={() => {
                          let new_battery = {
                            name: `Battery${values.batteries.length}`,
                            capacity: 0
                          };
                          arrayHelpers.push(new_battery);
                        }}
                        sx={{ border: '5px dashed gray' }}
                      >
                        <Box sx={{ width: '100%', p: 2.33 }}>
                          <Typography variant="h5" color="textSecondary">
                            Add new battery
                          </Typography>
                        </Box>
                      </ButtonBase>
                    </Stack>
                  </Grid>
                </>
              )}
            />

            <Grid item xs={12}>
              <Typography variant="h5" color="textSecondary">
                Devices
              </Typography>
            </Grid>
            <FieldArray
              name="devices"
              render={(arrayHelpers) => (
                <>
                  {values.devices.map((device, index) => (
                    <Grid item xs={12} key={index}>
                      <Stack spacing={1} direction="row" sx={{ width: '100%' }}>
                        <Stack spacing={1} sx={{ width: '100%' }}>
                          <InputLabel htmlFor="form-device-type">Device type</InputLabel>
                          <Select
                            value={values.devices[index].type}
                            name="type"
                            onChange={(e) => {
                              let new_device = { ...values.devices[index] };
                              new_device.type = e.target.value;
                              arrayHelpers.replace(index, new_device);
                            }}
                          >
                            <MenuItem value="other">Other</MenuItem>
                            <MenuItem value="solar">Solar</MenuItem>
                          </Select>
                        </Stack>
                        <Stack spacing={1} sx={{ width: '100%' }}>
                          <InputLabel htmlFor="form-device-name">Device name</InputLabel>
                          <OutlinedInput
                            id="form-device-name"
                            type="text"
                            value={device.name}
                            name="name"
                            onBlur={handleBlur}
                            onChange={(e) => {
                              let new_device = { ...values.devices[index] };
                              new_device.name = e.target.value;
                              arrayHelpers.replace(index, new_device);
                            }}
                            placeholder="Enter a device name"
                            fullWidth
                          />
                        </Stack>
                        <Stack spacing={1} sx={{ width: '100%' }}>
                          <InputLabel htmlFor="form-device-capacity">Device capacity</InputLabel>
                          <OutlinedInput
                            id="form-device-capacity"
                            type="number"
                            value={device.power}
                            name="capacity"
                            onBlur={handleBlur}
                            onChange={(e) => {
                              let new_device = { ...values.devices[index] };
                              new_device.power = e.target.value;
                              arrayHelpers.replace(index, new_device);
                            }}
                            placeholder="Enter a device capacity"
                            fullWidth
                          />
                        </Stack>
                        <Stack spacing={1} sx={{ width: '100%', height: '100%', alignSelf: 'flex-end' }}>
                          <IconButton color="error" aria-label="delete" onClick={() => arrayHelpers.remove(index)}>
                            <Delete />
                          </IconButton>
                        </Stack>
                      </Stack>
                    </Grid>
                  ))}
                  <Grid item xs={12}>
                    <Stack spacing={1} sx={{ width: '100%' }}>
                      <ButtonBase
                        onClick={() => {
                          let new_device = {
                            name: `Device${values.batteries.length}`,
                            power: 0,
                            type: 'other'
                          };
                          arrayHelpers.push(new_device);
                        }}
                        sx={{ border: '5px dashed gray' }}
                      >
                        <Box sx={{ width: '100%', p: 2.33 }}>
                          <Typography variant="h5" color="textSecondary">
                            Add new device
                          </Typography>
                        </Box>
                      </ButtonBase>
                    </Stack>
                  </Grid>
                </>
              )}
            />

            {errors.submit && (
              <Grid item xs={12}>
                <FormHelperText error>{errors.submit}</FormHelperText>
              </Grid>
            )}
            <Grid item xs={12}>
              <AnimateButton>
                <Button disableElevation disabled={isSubmitting} size="large" type="submit" variant="contained" color="primary">
                  Add house
                </Button>
              </AnimateButton>
            </Grid>
          </Grid>
        </form>
      )}
    </Formik>
  );
};

export default HouseForm;
