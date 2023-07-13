

class House:
    def __init__(self, name, size, heating_type, insulation_factor,heating_efficiency):
        self.name = name
        self.size = size
        self.heating_efficiency = heating_efficiency
        self.heating_type = heating_type
        self.insulation_factor = insulation_factor
        self.devices = []
        self.total_consumption= 0.0
    
    def calculate_total_consumption(self):
        for device in self.devices:
            self.total_consumption += device.calculate_consumption()
        self.total_consumption += self.calculate_heating_consumption()
        return self.total_consumption
    
    def calculate_heating_consumption(self):
        if self.heating_type == "electric":
            return self.size * 10.0  # Example formula for electric heating consumption
        elif self.heating_type == "gas":
            return self.size * 5.0   # Example formula for gas heating consumption
        else:
            return 0.0
    
    def get_devices(self):
        return self.devices
    
    def add_device(self, device):
        self.devices.append(device)

    def get_total_consumption(self):
        print(self.total_consumption)


class Simulation:
    def __init__(self, temperature, cloudiness, wind_speed, start_date, end_date):
        self.houses = []
        self.start_date = start_date
        self.end_date = end_date
        self.temperature = temperature
        self.cloudiness = cloudiness
        self.wind_speed = wind_speed
        self.optimizer = None
    
    def run_simulation(self):
        for house in self.houses:
            total_consumption = house.calculate_total_consumption()
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
house1 = House("House 1", 200, "electric")
device1 = Device("Device 1", 100.0, [0.5, 0.5, 0.5])  # Example usage pattern [0.5, 0.5, 0.5] for 3 hours
device2 = Device("Device 2", 50.0, [0.2, 0.3, 0.1])  # Example usage pattern [0.2, 0.3, 0.1] for 3 hours
house1.add_device(device1)
house1.add_device(device2)

simulation = Simulation()
simulation.houses.append(house1)
simulation.run_simulation()
house1.get_total_consumption()

