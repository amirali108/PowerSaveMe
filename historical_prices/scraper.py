# import re for reges
import pandas as pd
import requests
import json
import datetime




headers = {
    "User-Agent": "Your User Agent"
}

price_list = []



hourly_data = pd.read_csv(r'C:\Users\suad\Desktop\programming\PowerSaveMe\hourly_data.csv', index_col=0, parse_dates=True)

star_period = '2023-03-04'
end_period = '2023-03-10'




hourly_data = hourly_data.loc[star_period:end_period]
#take only temperature and price columns

for index, row in hourly_data.iterrows():
    print(index)
    print(row['Price'])
# temperature = hourly_data['Temperature'].to_numpy()
# price = hourly_data['Price'].to_numpy()

# print(len(temperature))
# print(len(price))

# print(temperature)

# print(price)

