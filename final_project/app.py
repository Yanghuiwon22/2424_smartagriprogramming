from flask import Flask, render_template, jsonify, request
import requests

import json
import csv
import os
import datetime
app = Flask(__name__)

# 데이터 저장 파일 경로 설정
BASE_DIR = "sensor_data"
os.makedirs(BASE_DIR, exist_ok=True)  # 디렉토리 생성

# DISTANCE_FILE = "water_distance_data.csv"

@app.route('/')
def home():
    data = get_temp_hum_distance()
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

        # 연도별 파일 경로 설정
        current_year = datetime.datetime.now().year
        file_path = get_year_based_file_path(current_year)

        # 데이터를 파일에 저장
        save_data_to_csv(file_path, load_existing_data(file_path), data)

        return jsonify(data)
    except requests.exceptions.RequestException as e:
        print(f"에러 발생: {e}")
        return jsonify({"error": "센서 데이터를 가져오지 못했습니다."}), 500

@app.route("/send_to_fastapi", methods=["POST"])
def send_to_fastapi():
    print("send_to_fastapi 함수 호출됨")
    try:
        print("1. 시도함")
        FASTAPI_URL = "http://113.198.63.27:30250/receive_data"
        print("2. FastAPI URL 설정 완료")

        # Flask에서 받은 데이터를 FastAPI로 전송
        data = request.json.get("data")  # 클라이언트로부터 받은 JSON 데이터
        print(f"2. 받은 데이터: {data}")

        # 데이터 전송
        try:
            response = requests.post(FASTAPI_URL, json={"data": data})  # FastAPI로 전송
            response.raise_for_status()  # 응답 코드 확인 (200이 아니면 예외 발생)
            print("3. Success!")
        except requests.exceptions.RequestException as e:
            print(f"FastAPI 요청 에러: {e}")
            raise

        # FastAPI의 응답 반환
        return jsonify({"fastapi_response": response.json()})
    except Exception as e:
        print(f"1-. 에러 발생함: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})
@app.route('/last-30-plot')
def last_30_plot():
    current_year = datetime.datetime.now().year
    file_path = get_year_based_file_path(current_year)
    data = get_last_30_data(file_path)

    if not data:
        return jsonify({"error": "No data available for plotting."}), 404

    # JSON 데이터 구성
    response_data = {
        "timestamps": [row['timestamp'] for row in data],
        "temp": [float(row['temp']) for row in data],
        "hum": [float(row['hum']) for row in data],
        "distance": [float(row['distance']) for row in data],
        "weight": [float(row['weight']) for row in data],
    }

    return jsonify(response_data)

# 2. 로드셀
# 3. 수위센서

def get_year_based_file_path(year):
    """
    연도별 데이터 파일 경로를 반환합니다.
    """
    return os.path.join(BASE_DIR, f"{year}_sensordata.csv")

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

        if not data_list:  # 데이터가 없을 때만 컬럼명을 추가
            fieldnames = ['timestamp', 'temp', 'hum', 'distance', 'weight']  # 모든 필드명 설정
            with open(file_path, "w", newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()  # 헤더 추가
        else:
            fieldnames = ['timestamp', 'temp', 'hum', 'distance', 'weight']  # 기존 데이터의 필드명 사용

        data_list.append(new_data)  # 새 데이터를 기존 리스트에 추가

    # 데이터를 timestamp 기준으로 정렬
    data_list.sort(key=lambda row: row['timestamp'])

    with open(file_path, "a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerows(data_list)  # 리스트 데이터를 파일에 기록

    print(f"데이터가 {file_path}에 저장되었습니다.")


# 데이터 파일 로드 함수
def load_existing_data(file_path):
    data = []
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
    return data

# 마지막 30개 데이터 가져오기 함수
def get_last_30_data(file_path):
    data = []
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
    return data[-100:] if len(data) >= 100 else data

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8000)
