from flask import Flask, render_template, jsonify, request
# from input_data import generate_fake_data, get_latest_sensor_data
import requests

import random
import json

app = Flask(__name__)

water_pump_status = False

@app.route('/')
def home():
    # print("수위센서 데이터를 가져옵니다.")
    # return render_template('index.html')
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
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        print(f"에러 발생: {e}")
        return jsonify({"error": "센서 데이터를 가져오지 못했습니다."}), 500

@app.route('/toggle-water-pump', methods=['POST'])
def toggle_water_pump():
    global water_pump_status
    water_pump_status = not water_pump_status
    status_message = "water_pump on" if water_pump_status else "water_pump off"
    print(status_message)  # 터미널에 출력
    return jsonify({"message": status_message}), 200


@app.route("/send_to_fastapi", methods=["POST"])
def send_to_fastapi():
    print("send_to_fastapi 함수 호출됨")
    try:
        print("1. 시도함")
        FASTAPI_URL = "http://113.198.63.27:30250/receive_data"
        # Flask에서 받은 데이터를 FastAPI로 전송
        data = request.json.get("data")  # 클라이언트로부터 받은 JSON 데이터
        print("2. 데이터 전송 시도함")
        # response = requests.post(FASTAPI_URL, json={"data": data})  # FastAPI로 전송
        # print("3. Success!")

        # 디버깅
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
        print("1-. 에러 발생함")
        return jsonify({"status": "error", "message": str(e)})



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8000)
