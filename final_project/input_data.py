# import random
#
# def generate_fake_data(num_points=24):
#     """
#     타임스탬프와 센서 데이터를 포함한 임의 데이터 생성.
#     """
#     from datetime import datetime, timedelta
#     data = []
#     current_time = datetime.now()
#     for _ in range(num_points):
#         data.append({
#             "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
#             "temperature": round(random.uniform(20, 30), 1),
#             "humidity": round(random.uniform(40, 60), 1),
#             "water_level": round(random.uniform(10, 100), 1)
#         })
#         current_time -= timedelta(hours=1)
#     return data
#
# def get_latest_sensor_data(fake_data):
#     """
#     가장 최근 센서 데이터를 반환.
#     """
#     return fake_data[0]  # 첫 번째 데이터가 가장 최근 데이터
#
# #def draw_graph():


import requests

def get_water_distance():
    url = "http://113.198.63.27:30250/temp_hum"

    response = requests.get(url)
    data = response.json()
    print(data)

get_water_distance()
