import requests
import re

def success_or_not(response):
    if response.status_code == 200:
        print("Success!")
        return True
    else:
        print("Something went wrong. Status code: " + str(response.status_code))
        return False

def get_Sn(postnummer):
    url= "https://www.hittaid.se/lookup/postalcodedemo"
    data = {"postal_code": postnummer}
    r = requests.post(url, data=data)


    if success_or_not(r):
        print(r.text)
        match = re.search(r'Elområde:\s*(\d+)', r.text)
        if match:
            elomrade = match.group(1)
            print(f"Elområde: {elomrade}")
        else:
            print("No match")

get_Sn(97752)