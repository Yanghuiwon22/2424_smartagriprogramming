from flask import Flask, render_template, jsonify
import requests

import json
import csv
import os
import datetime
app = Flask(__name__)

# 데이터 저장 파일 경로 설정
TEMP_HUM_FILE = "temp_hum_data.csv"
DISTANCE_FILE = "water_distance_data.csv"

# 기존 데이터를 파일에서 로드
def load_existing_data(file_path):
    data = []
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
    return data

# 데이터 파일 초기화
temp_hum_data = load_existing_data(TEMP_HUM_FILE)
distance_data = load_existing_data(DISTANCE_FILE)

@app.route('/')
def home():
    data = get_water_distance()
    return render_template('index.html', data=data)

# 센서 받아오기
# 1. 온습도
@app.route('/temp-hum-data', methods=['GET'])
def get_temp_hum_distance():
    print("수위센서 데이터를 가져옵니다.")
    url_temp_hum = "http://113.198.63.27:30250/temp_hum"
    try:
        response_temp_hum = requests.get(url_temp_hum, timeout=10)  # 타임아웃 추가


        print(f"HTTP 상태 코드: {response_temp_hum.status_code}")
        print(f"응답 내용: {response_temp_hum.text}")
        response_temp_hum.raise_for_status()  # HTTP 오류 발생 시 예외 처리

        data = json.loads(response_temp_hum.text)
        print(data, type(data))

        # 데이터를 파일에 저장
        save_data_to_csv(TEMP_HUM_FILE, temp_hum_data, data)

        return jsonify(data)
    except requests.exceptions.RequestException as e:
        print(f"에러 발생: {e}")
        return jsonify({"error": "센서 데이터를 가져오지 못했습니다."}), 500


# # 임의 데이터 생성해서 그래프 그려보기
# @app.route('/temp-data')
# def temp_data():
#     # 가짜 데이터 생성: 시간, 온도 (°C)
#     max_data_points = 20  # 최대 데이터 수
#     data = {
#         'labels': [f'Time {i}' for i in range(max_data_points)],
#         'data': [random.uniform(20, 30) for _ in range(max_data_points)]  # 20 ~ 30 사이의 임의 온도 데이터
#     }
#     return jsonify(data)
# # 여기까지 그래프 테스트

# 2. 로드셀
# 3. 수위센서
@app.route('/distance-data', methods=['GET'])
def get_water_distance():
    print("수위센서 데이터를 가져옵니다.")
    url = "http://113.198.63.27:30250/temp_hum"
    try:
        response = requests.get(url, timeout=10)  # 타임아웃 추가
        print(f"HTTP 상태 코드: {response.status_code}")
        print(f"응답 내용: {response.text}")
        response.raise_for_status()  # HTTP 오류 발생 시 예외 처리

        data = response.json()

        # 데이터를 파일에 저장
        save_data_to_csv(DISTANCE_FILE, distance_data, data)

        return jsonify(data)
    except requests.exceptions.RequestException as e:
        print(f"에러 발생: {e}")
        return jsonify({"error": "센서 데이터를 가져오지 못했습니다."}), 500


# 데이터 저장 함수
def save_data_to_csv(file_path, data_list, new_data):
    """
    CSV 파일에 데이터를 저장합니다.
    :param file_path: 저장할 파일 경로
    :param data_list: 기존 데이터 리스트
    :param new_data: 새로 추가할 데이터
    """
    if new_data:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data['timestamp'] = timestamp
        data_list.append(new_data)  # 새 데이터를 기존 리스트에 추가
    else:
        new_data = {}

    fieldnames = ['timestamp'] + list(new_data.keys())

    with open(file_path, "w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not os.path.exists(file_path):
            writer.writeheader()  # 헤더 작성
        writer.writerows(data_list)  # 리스트 데이터를 파일에 기록

    print(f"데이터가 {file_path}에 저장되었습니다.")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8000)
