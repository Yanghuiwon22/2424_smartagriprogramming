import requests

# FastAPI 서버의 주소
BASE_URL = "http://113.198.63.27:30250"

# 센서 데이터 가져오기
def get_sensor_data():
    try:
        # response = requests.get(f"{BASE_URL}/temp_hum")
        response = requests.get(f"{BASE_URL}/temp_hum")
        if response.status_code == 200:
            data = response.json()
            print(data)

        else:
            print(f"요청 실패: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"에러 발생: {e}")


def get_distance_data():
    try:
        response = requests.get(f"{BASE_URL}/distance")
        if response.status_code == 200:
            data = response.json()
            print(data)

        else:
            print(f"요청 실패: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    get_sensor_data()
