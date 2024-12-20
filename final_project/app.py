from flask import Flask, render_template, jsonify
# from input_data import generate_fake_data, get_latest_sensor_data
import requests
app = Flask(__name__)

@app.route('/')
def home():
    data = get_water_distance()
    return render_template('index.html', data=data)

# 센서 받아오기
# 1. 온습도
# 2. 로드셀

# 3. 수위센서
@app.route('/sensor-data', methods=['GET'])
def get_water_distance():
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

# get_water_distance()
#
# @app.route('/api/sensor_data')
# def sensor_data():
#     """
#     센서 데이터 API 엔드포인트 (가장 최근 데이터 제공)
#     """
#     fake_data = generate_fake_data()
#     latest_data = get_latest_sensor_data(fake_data)
#
#     # 센서 데이터 업데이트 (실시간)
#     get_water_distance()
#     return jsonify(latest_data)
#
# @app.route('/api/sensor_history')
# def sensor_history():
#     """
#     센서 데이터 API 엔드포인트 (전체 데이터 제공)
#     """
#     fake_data = generate_fake_data()
#     return jsonify(fake_data)
#
if __name__ == '__main__':
    app.run(debug=True)