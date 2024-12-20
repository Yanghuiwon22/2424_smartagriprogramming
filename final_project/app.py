from flask import Flask, render_template, jsonify
# from input_data import generate_fake_data, get_latest_sensor_data
import requests

import matplotlib.pyplot as plt
import io
import base64
import numpy as np

app = Flask(__name__)


# 가짜 데이터 생성
def create_fake_data():
    # 임의의 월별 평균 온도 데이터 생성
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    temperatures = np.random.normal(loc=20, scale=5, size=12)  # 평균 20도, 표준 편차 5도
    temperatures = np.clip(temperatures, 0, 40)  # 범위 제한

    return months, temperatures
@app.route('/data', methods=['GET'])
def get_data():
    months, temperatures = create_fake_data()
    return jsonify({
        'labels': months,
        'data': temperatures
    })



@app.route('/')
def home():
    # print("수위센서 데이터를 가져옵니다.")
    # return render_template('index.html')
    data = get_water_distance()
    return render_template('index.html', data=data)

# 센서 받아오기
# 1. 온습도
@app.route('/temp-hum-data', methods=['GET'])
def get_temp_hum_distance():
    print("수위센서 데이터를 가져옵니다.")
    url = "http://113.198.63.27:30250/temp_hum"
    try:
        response = requests.get(url, timeout=10)  # 타임아웃 추가
        print(f"HTTP 상태 코드: {response.status_code}")
        print(f"응답 내용: {response.text}")
        response.raise_for_status()  # HTTP 오류 발생 시 예외 처리

        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        print(f"에러 발생: {e}")
        return jsonify({"error": "센서 데이터를 가져오지 못했습니다."}), 500
# 2. 로드셀
# 3. 수위센서
@app.route('/distance-data', methods=['GET'])
def get_water_distance():
    print("수위센서 데이터를 가져옵니다.")
    url = "http://113.198.63.27:30250/distance"
    try:
        response = requests.get(url, timeout=10)  # 타임아웃 추가
        print(f"HTTP 상태 코드: {response.status_code}")
        print(f"응답 내용: {response.text}")
        response.raise_for_status()  # HTTP 오류 발생 시 예외 처리

        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        print(f"에러 발생: {e}")
        return jsonify({"error": "센서 데이터를 가져오지 못했습니다."}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8000)
