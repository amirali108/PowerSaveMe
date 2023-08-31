from django.shortcuts import render
from .sim.get_user_info import main as get_user_info
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from .sim.simulation_classes import House, Device, Solar_Panel, Battery, Simulation
import pandas as pd
import json

@permission_classes(["AllowAny"])
@parser_classes(["JSONParser"])
@api_view(['POST'])


def simulate(request):

    if not request.data.get("houses"):
        return Response("No houses found")
    
    if not request.data.get("start_period"):
        return Response("No start_period found")
    
    if not request.data.get("end_period"):
        return Response("No end_period found")

    simulations = []

    houses = request.data.get("houses")

    if type(houses) != list:
        houses = json.loads(houses)

    for house in houses:
        hourly_data = get_user_info(house["adress"])
        simulations.append(Simulation(request.data.get("start_period"), request.data.get("end_period"), hourly_data))
        current_house1 = House(house["name"], house["size"], house["heating"], house["heating_efficiency"], house["cooling_efficiency"], house["has_battery"])
        for device in house["devices"]:
            if device["type"] == "solar":
                current_house1.add_device(Solar_Panel(device["name"], device["power"]))
            else:
                current_house1.add_device(Device(device["name"], device["power"]))

        for battery in house["batteries"]:
            current_house1.add_battery(Battery(battery["name"], battery["capacity"]))
        simulations[-1].houses.append(current_house1)

    for simulation in simulations:
        simulation.run_simulation()

    house_data = {}
    for simulation in simulations:
        house = simulation.houses[0]
        house_data[house.name] = {"hourly_usage": house.get_all_devices_hourly_usage(), "hourly_consumptions": house.get_hourly_consumptions(), "total_consumption": house.get_total_consumption(), "total_consumption_price": house.get_total_consumption_price(), "battery_level": house.battery.get_battery_level()}

    return Response(house_data)