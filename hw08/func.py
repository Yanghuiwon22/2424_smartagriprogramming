import requests
import concurrent.futures

def fetch_data(i):
    url = f'https://thingspeak.mathworks.com/channels/2328695/field/{i}.json'
    response = requests.get(url)
    if response.status_code == 200:
        return i, response.json()['feeds'][-1]
    return i, None

def jbnu_aws_data():
    result = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_data, i) for i in range(1, 8)]
        for future in concurrent.futures.as_completed(futures):
            i, data = future.result()
            if data:
                result[i] = data

    return result
jbnu_aws_data()

