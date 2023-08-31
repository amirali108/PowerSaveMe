import requests
import re
import asyncio
import json
import datetime
import pandas as pd
from math import radians, sin, cos, sqrt, atan2


from opencage.geocoder import OpenCageGeocode




def get_lat_and_long(adress):
    key = '8059d5c7a5284da497c2979a305070fb'
    geocoder = OpenCageGeocode(key)
    results = geocoder.geocode(adress)
    location = results[0]
    # Extracting latitude and longitude from the 'geometry' key
    latitude = location['geometry']['lat']
    longitude = location['geometry']['lng']

    # Extracting NUTS1 code from the 'NUTS' key under 'annotations'
    nuts1_code = location['annotations']['NUTS']['NUTS1']['code']

    # Extracting city, county, and municipality from the 'components' key
    city = location['components'].get('city', 'N/A')  # Using get() to handle missing keys
    county = location['components'].get('county', 'N/A')
    municipality = location['components'].get('municipality', 'N/A')
    return latitude, longitude, nuts1_code, city, county, municipality





def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Converting coordinates from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Computing differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

def find_closest_station(cur_latitude, cur_longitude):
    # Response from the API
    url="https://opendata-download-metobs.smhi.se/api/version/latest/parameter/1.json"

    response_json = requests.get(url).text
    # Parsing the JSON response
    response = json.loads(response_json)

    # Finding the closest station
    stations = response['station']

    stations_sorted_by_distance = sorted(stations, key=lambda x: calculate_distance(cur_latitude, cur_longitude, x['latitude'], x['longitude']))

    for station in stations_sorted_by_distance:
        if station['active']:
            closest_active_station = station
            break
        
    return closest_active_station['id']





def get_metereological_data(lat, long, eletrical_region):

    combined_data = {}

    types = ['Temperature', 'Cloudiness','Wind speed', 'Price']
 
    endpoints = [
    'https://opendata-download-metobs.smhi.se/api/version/latest/parameter/1/station/' + str(find_closest_station(lat, long))+'/period/latest-months/data.json',
    'https://opendata-download-metobs.smhi.se/api/version/latest/parameter/16/station/'+str(find_closest_station(lat, long))+'/period/latest-months/data.json',
    'https://opendata-download-metobs.smhi.se/api/version/latest/parameter/4/station/'+str(find_closest_station(lat, long))+'/period/latest-months/data.json'
    ]


    for endpoint in endpoints:
    # Make a GET request to the API endpoint
        response = requests.get(endpoint)

        # Check if the request was successful (status code 200 indicates success)
        if response.status_code == 200:
            # Access the JSON data from the response
            json_data = json.loads(response.text)

            # Traverse through the JSON data and extract date and value
            for item in json_data['value']:
                date_seconds = item['date'] / 1000  # Convert milliseconds to seconds
                value = item['value']
                date = datetime.datetime.fromtimestamp(date_seconds)

                # Check if the date is already in the combined data dictionary
                if date in combined_data:
                    # Append the value to the existing list for the respective data type
                    combined_data[date].append(value)
                else:
                    # Create a new list for the date and initialize it with the value
                    combined_data[date] = [value]
        else:
            # If the request was not successful, print the status code and reason
            del types[endpoints.index(endpoint)]
            print('Request failed with status code:', response.status_code)
            print('Reason:', response.reason)

    start_date = (list(combined_data.keys())[0]).date()
    end_date = (list(combined_data.keys())[-1]).date()                           
    
   
    res= requests.get('https://www.vattenfall.se/api/price/spot/pricearea/'+str(start_date)+'/'+str(end_date)+'/'+eletrical_region, headers= {
        "User-Agent": "Your User Agent"
    })

    print(res.status_code)

    if res.status_code == 200:
        # Parse the JSON response
        parsed_data = res.json()

        # Iterate over the data
        for entry in parsed_data:
            date = entry["TimeStamp"]
            price = entry["Value"]
            date = date.split('T')[0] + ' ' + date.split('T')[1].split(':')[0] + ':00:00'
            try:
                combined_data[datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')].append(price)
                print("appended price")
            except:
                print("price dont wok")
                pass
    else:
        del types[-1]
        print(f"Error: {res.status_code} - {res.reason}")
    df = pd.DataFrame(combined_data.items(), columns=['Date', 'Values'])
    print(df)
    # Split the 'Values' column into separate columns for Temperature and Cloudiness
    df[types] = pd.DataFrame(df['Values'].tolist(), index=df.index)

    # Forward fill missing Wind Speed values
    if 'Wind speed' in types:
        df['Wind speed'] = df['Wind speed'].fillna(method='ffill')

    if "Cloudiness" in types:
        df['Cloudiness'] = df['Cloudiness'].fillna(method='ffill')

    if "Price" in types:
        df['Price'] = df['Price'].fillna(method='ffill')

    # Keep only Date, Temperature, and Wind Speed columns
    df = df[['Date'] + types].set_index('Date')
    print(df)
    return df


def main(adress):
    lat, long, nuts1_code, city, county, municipality = get_lat_and_long(adress)
    if("SE" in nuts1_code):
        nuts1_code = nuts1_code.replace("SE", "SN")
    return get_metereological_data(lat, long, nuts1_code)