import pandas as pd 

from datetime import datetime

star_period = '2023-07-08'
end_period = '2023-07-12'

# make relative path for the repo 
hourly_data = pd.read_csv(r'C:\Users\suad\Desktop\programming\PowerSaveMe\hourly_data.csv', index_col=0, parse_dates=True)



class House:
    def __init__(self, name, size, heating_type, insulation,heating_efficiency, optimize):
        self.name = name
        self.house_size = size
        self.heating_efficiency = heating_efficiency
        self.heating_type = heating_type
        self.insulation = insulation
        self.optimize = optimize
        self.battery = None
        self.devices = []
        self.target_temperature = 20.5
        self.total_consumption= 0.0
        self.hourly_consumptions = {}
        self.hourly_consumption_price = {}
        self.total_consumption_price = 0.0
        self.HEAT_CAPACITY_AIR = 1.005  # kJ/kg.K
        self.DENSITY_AIR = 1.164  # kg/m3
        self.EFFICIENCY_HEATING_SYSTEM = 0.9  # 90% efficiency
        self.INSULATION_FACTOR = 0.5  # Arbitrary insulation factor
        self.WIND_CHILL_FACTOR = 0.1  # Arbitrary wind chill factor
        self.CLOUDINESS_FACTOR = 0.1  # Arbitrary cloudiness factor
        self.U_VALUE_WALL = 0.35  # Heat transfer coefficient of the wall, W/(m2.K)
        self.U_VALUE_WINDOW = 1.5  # Heat transfer coefficient of the window, W/(m2.K)
        self.WINDOW_TO_WALL_RATIO = 0.2  # Ratio of window area to wall area
    

    def calculate_total_hourly_consumption(self, time, price, outside_temperature, wind_speed, cloudiness):
        self.hourly_consumptions[time]= self.calculate_hourly_heating_consumption(outside_temperature, wind_speed, cloudiness) + sum([device.calculate_consumption(time.hour) for device in self.devices])

        ##############################
        # optimization block 

        if(self.optimize and self.battery):
            if(self.hourly_consumptions[time] < 0):
                if(self.battery.is_full() is not True):
                    self.battery.charge(-self.hourly_consumptions[time])
                    self.hourly_consumptions[time] = 0
            if(self.hourly_consumptions[time] > 0):
                if(self.battery.charge_level > self.hourly_consumptions[time]):
                    self.battery.discharge(self.hourly_consumptions[time])
                    self.hourly_consumptions[time] = 0
                else:
                    self.hourly_consumptions[time] -= self.battery.discharge(self.hourly_consumptions[time])

        ##############################
        

        self.hourly_consumption_price[time] = self.hourly_consumptions[time]  * price
        self.total_consumption += self.hourly_consumptions[time]         
        self.total_consumption_price += self.hourly_consumption_price[time]
    

    def calculate_hourly_heating_consumption(self, outside_temperature, wind_speed, cloudiness):
        if(outside_temperature >= self.target_temperature):
            return 0
        # Calculate the temperature difference
        temperature_difference = self.target_temperature - outside_temperature

        # Calculate the wind chill
        wind_chill = wind_speed * self.WIND_CHILL_FACTOR

        # Calculate the cloudiness effect
        cloudiness_effect = cloudiness * self.CLOUDINESS_FACTOR

        # Calculate the total heat loss due to temperature difference, wind chill, and cloudiness
        total_heat_loss = temperature_difference + wind_chill + cloudiness_effect

        # Calculate the volume of the house
        house_volume = self.house_size  # Assuming 1 sqm = 1 m3 for simplicity

        # Calculate the mass of the air in the house
        mass_air = self.DENSITY_AIR * house_volume

        # Calculate the energy needed to heat the air in the house by the temperature difference
        energy_needed = mass_air * self.HEAT_CAPACITY_AIR * total_heat_loss  # in kJ

        # Adjust for insulation
        energy_needed *= (1 - self.insulation * self.INSULATION_FACTOR)

        # Adjust for heating system efficiency
        energy_needed /= self.EFFICIENCY_HEATING_SYSTEM

        # Calculate heat loss through the walls and windows
        wall_area = self.house_size * (1 - self.WINDOW_TO_WALL_RATIO)  # Assuming all walls are external for simplicity
        window_area = self.house_size * self.WINDOW_TO_WALL_RATIO
        heat_loss_walls = self.U_VALUE_WALL * wall_area * temperature_difference
        heat_loss_windows = self.U_VALUE_WINDOW * window_area * temperature_difference

        # Convert heat loss from W to kJ
        heat_loss_walls *= 3600 / 1000
        heat_loss_windows *= 3600 / 1000

        # Add heat loss through walls and windows to total energy needed
        energy_needed += heat_loss_walls + heat_loss_windows

        # Convert energy from kJ to kWh
        return energy_needed / 3600

        # print(energy_needed / 3600)
        # self.hourly_consumption_price[time] = self.hourly_consumptions[time]  * price
        # print(price)
        # self.total_consumption += self.hourly_consumptions[time]
        # self.total_consumption_price += self.hourly_consumption_price[time]

    
    def add_battery(self, battery):
        self.battery = battery
    
    def add_device(self, device):
        self.devices.append(device)
    
    def get_total_consumption_price(self):
        print(self.total_consumption_price)

    def get_hourly_consumption_price(self):
        print(self.hourly_consumption_price)

    def get_devices(self):
        return self.devices

    def get_total_consumption(self):
        print(self.total_consumption)
    
    def get_hourly_consumptions(self):
        print(self.hourly_consumptions)
    
    def get_power_usage_time_period(self, start_time, end_time):
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    
        extracted_values = {}
        for key, value in self.hourly_consumptions.items():
            if start_time <= key <= end_time:
                extracted_values[key] = value
        
        print(extracted_values)
        print(sum(extracted_values.values()))

    def get_all_devices_hourly_usage(self):
        for device in self.devices:
            device.get_hourly_usage() 
    
    

class Simulation:
    def __init__(self, start_date, end_date, hourly_data):
        self.houses = []
        self.start_date = start_date
        self.end_date = end_date
        self.hourly_data = hourly_data.loc[start_date:end_date]
        self.optimizer = None
    
    def run_simulation(self):
        for house in self.houses:
            for index,row in self.hourly_data.iterrows():
                house.calculate_total_hourly_consumption(index, row['Price']/100, row['Temperature'], row['Wind speed'], row['Cloudiness'])

            # Perform any necessary actions with the total consumption
            
        if self.optimizer:
            self.optimizer.optimize_consumption()
    
    

    


class Device:
    def __init__(self, name, power_rating):
        self.name = name
        self.power_rating = power_rating
        self.hourly_usage = {}
    

    def usage_pattern(self, hour):
        # Define a usage pattern based on the hour of the day
        if 0 <= hour < 6:  # Low usage from midnight to 6am
            return 0.2
        elif 6 <= hour < 9:  # High usage from 6am to 9am
            return 0.9
        elif 9 <= hour < 17:  # Medium usage from 9am to 5pm
            return 0.5
        elif 17 <= hour < 23:  # High usage from 5pm to 9pm
            return 0.9
        else:  # Low usage from 9pm to midnight
            return 0.5

    def calculate_consumption(self, hour):
        self.hourly_usage[hour] = self.power_rating * self.usage_pattern(hour)/1000
        return self.hourly_usage[hour]
    
    def get_hourly_usage(self):
        print(self.hourly_usage)
    
    
    

class Solar_Panel(Device):
    def __init__(self, name, power_rating):
        super().__init__(name, power_rating)

    def usage_pattern(self, hour):
        # Define a usage pattern based on the hour of the day
        if 6 <= hour < 18:  # Solar panels generate electricity from 6am to 6pm
            return 1
        else:  # No electricity is generated from 6pm to 6am
            return 0

    def calculate_consumption(self, hour):
        # For solar panels, the "consumption" is actually negative because they generate electricity
        self.hourly_usage[hour] = -self.power_rating * self.usage_pattern(hour)/1000
        return self.hourly_usage[hour]

class Battery():
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.charge_level = 0

    def charge(self, amount):
        # Increase the charge level by the specified amount, up to the battery's capacity
        self.charge_level = min(self.charge_level + amount, self.capacity)
        

    def discharge(self, amount):
        # Decrease the charge level by the specified amount, down to a minimum of 0
        amount_discharged = min(amount, self.charge_level)
        self.charge_level -= amount_discharged
        return amount_discharged  # Return the actual amount discharged
    
    def is_full(self):
        # Return True if the battery is fully charged; False otherwise
        return self.charge_level == self.capacity

    def get_battery_level(self):
        print(self.charge_level)


#######################

# Example usage:
house1 = House("House 1", 120, "electric", 0.9, 0.8, True)
device1 = Device("Device 1", 100.0)  # Example usage pattern [0.5, 0.5, 0.5] for 3 hours
device2 = Device("Device 2", 50.0)  # Example usage pattern [0.2, 0.3, 0.1] for 3 hours
house1.add_device(device1)
house1.add_device(device2)
house1.add_device(Solar_Panel("Solar Panel", 100.0))  
house1.add_device(Solar_Panel("Solar Panel 2", 300.0))
house1.add_device(Solar_Panel("Solar Panel 3", 500.0))


house1.add_battery(Battery("Battery 1", 10.0))

simulation = Simulation(star_period, end_period, hourly_data)
simulation.houses.append(house1)
simulation.run_simulation()



house1.get_power_usage_time_period('2023-07-8 00:00:00', '2023-07-12 23:00:00')

house1.get_all_devices_hourly_usage()
house1.get_total_consumption()

house1.battery.get_battery_level()