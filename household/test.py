import pandas as pd 


star_period = '2023-03-04'
end_period = '2023-03-05'

# make relative path for the repo 
hourly_data = pd.read_csv(r'C:\Users\suad\Desktop\programming\PowerSaveMe\hourly_data.csv', index_col=0, parse_dates=True)



class House:
    def __init__(self, name, size, heating_type, insulation_factor,heating_efficiency):
        self.name = name
        self.size = size
        self.heating_efficiency = heating_efficiency
        self.heating_type = heating_type
        self.insulation_factor = insulation_factor
        self.devices = []
        self.target_temperature = 21.5
        self.total_consumption= 0.0
        self.hourly_consumptions = {}
        self.hourly_consumption_price = {}
        self.total_consumption_price = 0.0
    
    

    def calculate_hourly_heating_consumption(self, time, price, temperature):
        self.hourly_consumptions[time] = self.size *(self.target_temperature - temperature)/(self.heating_efficiency * self.insulation_factor)/1000
        self.hourly_consumption_price[time] = self.hourly_consumptions[time]  * price
        print(price)
        self.total_consumption += self.hourly_consumptions[time]
        self.total_consumption_price += self.hourly_consumption_price[time]

    

    
    def get_total_consumption_price(self):
        print(self.total_consumption_price)

    def get_hourly_consumption_price(self):
        print(self.hourly_consumption_price)
    def get_devices(self):
        return self.devices
    
    def add_device(self, device):
        self.devices.append(device)

    def get_total_consumption(self):
        print(self.total_consumption)
    
    def get_hourly_consumptions(self):
        print(self.hourly_consumptions)


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
                house.calculate_hourly_heating_consumption(index, row['Price'], row['Temperature'])

            # Perform any necessary actions with the total consumption
            
        if self.optimizer:
            self.optimizer.optimize_consumption()
    
    

    


class Device:
    def __init__(self, name, power_rating, usage_pattern):
        self.name = name
        self.power_rating = power_rating
        self.usage_pattern = usage_pattern
    
    def calculate_consumption(self):
        return self.power_rating * sum(self.usage_pattern)


# Example usage:
house1 = House("House 1", 200, "electric", 0.9, 0.8)
device1 = Device("Device 1", 100.0, [0.5, 0.5, 0.5])  # Example usage pattern [0.5, 0.5, 0.5] for 3 hours
device2 = Device("Device 2", 50.0, [0.2, 0.3, 0.1])  # Example usage pattern [0.2, 0.3, 0.1] for 3 hours
house1.add_device(device1)
house1.add_device(device2)

simulation = Simulation(star_period, end_period, hourly_data)
simulation.houses.append(house1)
simulation.run_simulation()


house1.get_hourly_consumption_price()
house1.get_total_consumption()

