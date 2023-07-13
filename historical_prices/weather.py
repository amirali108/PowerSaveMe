import requests
import json
import datetime
import pandas as pd

combined_data = {}

headers = {
    "User-Agent": "Your User Agent"
}





# List of API endpoints for temperature and wind speed
endpoints = [
    'https://opendata-download-metobs.smhi.se/api/version/latest/parameter/1/station/162860/period/latest-months/data.json',
    'https://opendata-download-metobs.smhi.se/api/version/latest/parameter/16/station/162860/period/latest-months/data.json',
    'https://opendata-download-metobs.smhi.se/api/version/latest/parameter/4/station/162860/period/latest-months/data.json'
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
        print('Request failed with status code:', response.status_code)
        print('Reason:', response.reason)

start_date = (list(combined_data.keys())[0]).date()
end_date = (list(combined_data.keys())[-1]).date()                           

res= requests.get('https://www.vattenfall.se/api/price/spot/pricearea/'+str(start_date)+'/'+str(end_date)+'/SN3', headers=headers)

if res.status_code == 200:
    # Parse the JSON response
    parsed_data = res.json()

    # Iterate over the data
    for entry in parsed_data:
        date = entry["TimeStamp"]
        price = entry["Value"]

        # haram code 
        date = date.split('T')[0] + ' ' + date.split('T')[1].split(':')[0] + ':00:00'
        print(date)
        try:
            combined_data[datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')].append(price)
        except:
            pass
else:
    print(f"Error: {res.status_code} - {res.reason}")


# Create a DataFrame from the combined data dictionary
df = pd.DataFrame(combined_data.items(), columns=['Date', 'Values'])

# Split the 'Values' column into separate columns for Temperature and Cloudiness
df[['Temperature', 'Cloudiness','Wind speed', 'Price']] = pd.DataFrame(df['Values'].tolist(), index=df.index)

# Forward fill missing Wind Speed values
df['Cloudiness'] = df['Cloudiness'].fillna(method='ffill')
df['Wind speed'] = df['Wind speed'].fillna(method='ffill')
df['Price'] = df['Price'].fillna(method='ffill')

# Keep only Date, Temperature, and Wind Speed columns
df = df[['Date', 'Temperature', 'Cloudiness','Wind speed', 'Price']]

# Save the modified data to a CSV file
df.to_csv('hourly_data.csv', index=False)