from flask import Flask, render_template, jsonify
from input_data import generate_fake_data, get_latest_sensor_data

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/sensor_data')
def sensor_data():
    """
    센서 데이터 API 엔드포인트 (가장 최근 데이터 제공)
    """
    fake_data = generate_fake_data()
    latest_data = get_latest_sensor_data(fake_data)
    return jsonify(latest_data)

@app.route('/api/sensor_history')
def sensor_history():
    """
    센서 데이터 API 엔드포인트 (전체 데이터 제공)
    """
    fake_data = generate_fake_data()
    return jsonify(fake_data)

if __name__ == '__main__':
    app.run(debug=True)