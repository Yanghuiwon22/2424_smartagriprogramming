from flask import Flask, render_template, jsonify
from input_data import generate_fake_data, get_latest_sensor_data
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
    url = "http://192.168.50.243:5000/temp_hum"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return jsonify({"error": "센서 데이터를 가져오지 못했습니다."})
    print(data)


if __name__ == '__main__':
    app.run(debug=True)

