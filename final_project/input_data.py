import requests

def get_water_distance():
    url = "http://113.198.63.27:30250/temp_hum"

    response = requests.get(url)
    data = response.json()
    print(data)

get_water_distance()
