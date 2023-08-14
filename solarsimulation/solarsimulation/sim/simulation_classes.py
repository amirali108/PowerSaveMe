import pandas as pd 

from datetime import datetime
import json



class House:
    def __init__(self, name, size, heating_type, insulation,heating_efficiency, optimize):
        self.name = name
        self.house_size = size
        self.heating_type = heating_type
        self.insulation = insulation
        self.optimize = optimize
        self.battery = None
        self.devices = []
        self.target_temperature = 19.5
        self.total_consumption= 0.0 
        self.hourly_consumptions = {}
        self.hourly_consumption_price = {}
        self.total_consumption_price = 0.0
        self.HEAT_CAPACITY_AIR = 1.005  # kJ/kg.K
        self.DENSITY_AIR = 1.164  # kg/m3
        self.EFFICIENCY_HEATING_SYSTEM = heating_efficiency  # 90% efficiency
        self.INSULATION_FACTOR = 0.5  # Arbitrary insulation factor
        self.WIND_CHILL_FACTOR = 0.1  # Arbitrary wind chill factor
        self.CLOUDINESS_FACTOR = 0.1  # Arbitrary cloudiness factor
        self.U_VALUE_WALL = 0.35  # Heat transfer coefficient of the wall, W/(m2.K)
        self.U_VALUE_WINDOW = 1.5  # Heat transfer coefficient of the window, W/(m2.K)
        self.WINDOW_TO_WALL_RATIO = 0.2  # Ratio of window area to wall area
    

    def calculate_total_hourly_consumption(self, time, price, outside_temperature, wind_speed, cloudiness, daily_average_price):
        self.hourly_consumptions[time]= self.calculate_hourly_heating_consumption(outside_temperature, wind_speed, cloudiness) + sum([device.calculate_consumption(time.hour) for device in self.devices])

        ##############################
        # optimization block 

        #if the price of the electricity is higher then average price and the solar power is enough to cover the consumption and if the battery has excess power then sell all the power to the grid
        #if the price of the electricity is higher then average price and the solar power is not enough to cover the consumption and if the battery has excess power use the battery to cover the consumption and sell the excess if there is any
        #if the price of the electricity is lower then average price and the solar power is enough to cover the consumption and if the battery has excess power then cover the consumption with it
        #if the price of the electricity is much cheaper <0.5 and the battery is not full then charge the battery
        #if the price of the electricity is much cheaper <0.5 and the battery is full then sell the excess power to the grid

        if(self.optimize and self.battery!=None):
            if(self.hourly_consumptions[time] <= 0): 
                if(daily_average_price <= price):
                    if(self.battery.charge_level > 0):
                        self.hourly_consumptions[time] -= min(2,self.battery.charge_level)
                        self.battery.discharge(min(2,self.battery.charge_level)) 


                if(daily_average_price*0.7 > price):
                    #charge the battery if the prices are low 
                    if(self.battery.charge_level < self.battery.capacity):
                        self.hourly_consumptions[time] += min(2,self.battery.capacity - self.battery.charge_level)
                        self.battery.charge(min(2,self.battery.capacity - self.battery.charge_level))   

                elif(daily_average_price > price):
                    if(self.battery.charge_level <= self.battery.capacity):
                        
                        if(self.battery.charge_level  - self.hourly_consumptions[time] > self.battery.capacity):
                            self.hourly_consumptions[time] += min(2,self.battery.capacity - self.battery.charge_level)
                            self.battery.charge(min(2,self.battery.capacity - self.battery.charge_level))
                            
                        else:
                            self.battery.charge(min(2,-self.hourly_consumptions[time]))
                            self.hourly_consumptions[time] += min(2,-self.hourly_consumptions[time]) 
            

            elif(self.hourly_consumptions[time] > 0):

                #use battery if there some energy
                if(daily_average_price*0.9 <= price):
                    if(self.battery.charge_level > 0):
                        self.hourly_consumptions[time] -= min(2,self.battery.charge_level, self.hourly_consumptions[time])
                        self.battery.discharge(min(2,self.battery.charge_level, self.hourly_consumptions[time]))
                #use battery but give out less energy if the prices are not that high
                elif(daily_average_price*0.7 <= price):
                    if(self.battery.charge_level > 0):
                        self.hourly_consumptions[time] -= min(1,self.battery.charge_level, self.hourly_consumptions[time])
                        self.battery.discharge(min(1,self.battery.charge_level, self.hourly_consumptions[time]))
                # charge otherwise
                else:
                    if(self.battery.charge_level < self.battery.capacity):
                        self.hourly_consumptions[time] += min(2,self.battery.capacity - self.battery.charge_level)
                        self.battery.charge(min(2,self.battery.capacity - self.battery.charge_level))

                    


        ##############################
    
        self.hourly_consumption_price[time] = round(self.hourly_consumptions[time]  * price,2)
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


    def add_battery(self, battery):
        self.battery = battery
    
    def add_device(self, device):
        self.devices.append(device)
    
    def get_total_consumption_price(self):
        return self.total_consumption_price

    def get_hourly_consumption_price(self):
        return self.hourly_consumption_price

    def get_devices(self):
        return self.devices

    def get_total_consumption(self):
        return self.total_consumption
    
    def get_hourly_consumptions(self):
        # serialize Timestamp keys as string
        converted_dict = {}
        for key, value in self.hourly_consumptions.items():
            converted_dict[key.strftime('%Y-%m-%d %H:%M:%S')] = value
        return converted_dict
    
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
        hourly_usage_list = []
        for device in self.devices:
            hourly_usage_list.append(device.get_hourly_usage())
        return hourly_usage_list
    
    


class Device:
    def __init__(self, name, power_rating):
        self.name = name
        self.power_rating = power_rating
        self.hourly_usage = [None]*24
    

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
        return self.hourly_usage
    
    
    
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
        return self.charge_level


#######################

class Simulation:
    def __init__(self, start_date, end_date, hourly_data):
        self.houses = []
        self.start_date = start_date
        self.end_date = end_date
        self.hourly_data = hourly_data.loc[start_date:end_date]
    
    def run_simulation(self):
        for house in self.houses:
            for index,row in self.hourly_data.iterrows():
                house.calculate_total_hourly_consumption(index, row['Price']/100, float(row['Temperature']), float(row['Wind speed']), float(row['Cloudiness']), self.calculate_daily_average_price(index))
              

            # Perform any necessary actions with the total consumption
            
    
    def calculate_daily_average_price(self, index):
        next_day = index + pd.DateOffset(days=1)
        return self.hourly_data.loc[index:next_day]['Price'].mean()/100

