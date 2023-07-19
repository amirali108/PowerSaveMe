
# Constants
HEAT_CAPACITY_AIR = 1.005  # kJ/kg.K
DENSITY_AIR = 1.164  # kg/m3
EFFICIENCY_HEATING_SYSTEM = 0.9  # 90% efficiency
INSULATION_FACTOR = 0.5  # Arbitrary insulation factor
WIND_CHILL_FACTOR = 0.1  # Arbitrary wind chill factor
CLOUDINESS_FACTOR = 0.1  # Arbitrary cloudiness factor
U_VALUE_WALL = 0.35  # Heat transfer coefficient of the wall, W/(m2.K)
U_VALUE_WINDOW = 1.5  # Heat transfer coefficient of the window, W/(m2.K)
WINDOW_TO_WALL_RATIO = 0.2  # Ratio of window area to wall area

def calculate_hourly_energy_consumption(target_temperature, outside_temperature, wind_speed, cloudiness, house_size, insulation):
    # Calculate the temperature difference
    temperature_difference = target_temperature - outside_temperature

    # Calculate the wind chill
    wind_chill = wind_speed * WIND_CHILL_FACTOR

    # Calculate the cloudiness effect
    cloudiness_effect = cloudiness * CLOUDINESS_FACTOR

    # Calculate the total heat loss due to temperature difference, wind chill, and cloudiness
    total_heat_loss = temperature_difference + wind_chill + cloudiness_effect

    # Calculate the volume of the house
    house_volume = house_size  # Assuming 1 sqm = 1 m3 for simplicity

    # Calculate the mass of the air in the house
    mass_air = DENSITY_AIR * house_volume

    # Calculate the energy needed to heat the air in the house by the temperature difference
    energy_needed = mass_air * HEAT_CAPACITY_AIR * total_heat_loss  # in kJ

    # Adjust for insulation
    energy_needed *= (1 - insulation * INSULATION_FACTOR)

    # Adjust for heating system efficiency
    energy_needed /= EFFICIENCY_HEATING_SYSTEM

    # Calculate heat loss through the walls and windows
    wall_area = house_size * (1 - WINDOW_TO_WALL_RATIO)  # Assuming all walls are external for simplicity
    window_area = house_size * WINDOW_TO_WALL_RATIO
    heat_loss_walls = U_VALUE_WALL * wall_area * temperature_difference
    heat_loss_windows = U_VALUE_WINDOW * window_area * temperature_difference

    # Convert heat loss from W to kJ
    heat_loss_walls *= 3600 / 1000
    heat_loss_windows *= 3600 / 1000

    # Add heat loss through walls and windows to total energy needed
    energy_needed += heat_loss_walls + heat_loss_windows

    # Convert energy from kJ to kWh
    energy_needed /= 3600

    return energy_needed

# Test the function
print(calculate_hourly_energy_consumption(20, 1.3, 5, 0.5, 120, 0.8))
