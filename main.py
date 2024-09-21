import requests
import re
from prometheus_client import start_http_server, Summary, Counter
import time

# Prometheus metrics
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
SUCCESSFUL_REQUESTS = Counter('successful_requests', 'Number of successful requests')
FAILED_REQUESTS = Counter('failed_requests', 'Number of failed requests')

# This function tracks how long the request takes
@REQUEST_TIME.time()
def get_Sn(postnummer):
    url = "https://www.hittaid.se/lookup/postalcodedemo"
    data = {"postal_code": postnummer}
    r = requests.post(url, data=data)

    if success_or_not(r):
        SUCCESSFUL_REQUESTS.inc()  # Increment successful request counter
        print(r.text)
        match = re.search(r'Elområde:\s*(\d+)', r.text)
        if match:
            elomrade = match.group(1)
            print(f"Elområde: {elomrade}")
        else:
            print("No match")
    else:
        FAILED_REQUESTS.inc()  # Increment failed request counter

def success_or_not(response):
    if response.status_code == 200:
        print("Success!")
        return True
    else:
        print("Something went wrong. Status code: " + str(response.status_code))
        return False

if __name__ == "__main__":
    # Start Prometheus metrics server on port 8001
    start_http_server(8001)
    print("Prometheus server started on port 8001")

    # Example request, can be removed or modified as needed
    while True:
        get_Sn(97752)
        time.sleep(60)  # Wait for 60 seconds before making another request
