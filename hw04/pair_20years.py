import requests
import pandas as pd

# api를 통해서 데이터 받아오기
def get_data(sy, ey):
    for i in range(ey+1-sy):
        url = 'https://api.taegon.kr/stations/146/'

        params = {
            'sy' : sy+i,
            'ey' : ey+i,
            format : 'csv'
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            content = response.json()
            df = pd.DataFrame(content)
            df.to_csv(f'output/weather_{sy+i}')
            print(f'{sy+i}년도 데이터 저장 완.')
        else:
            print(response.status_code)


get_data(2004, 2023)
