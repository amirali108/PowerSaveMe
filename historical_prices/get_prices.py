import requests
import json
import datetime

start_period = '2023-03-04'
end_period = '2023-03-10'
headers = {
    "User-Agent": "Your User Agent"
}

res= requests.get('https://www.vattenfall.se/api/price/spot/pricearea/2023-07-13/2023-07-13/SN3', headers=headers)

if res.status_code == 200:
    # Parse the JSON response
    parsed_data = res.json()

    # Iterate over the data
    for entry in parsed_data:
        timestamp = entry["TimeStamp"]
        price = entry["Value"]
        unit = entry["Unit"]

        print(f"At {timestamp}, the price per kWh is {price} {unit}.")
else:
    print(f"Error: {res.status_code} - {res.reason}")