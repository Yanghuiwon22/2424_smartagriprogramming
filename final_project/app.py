from flask import Flask, render_template, jsonify
from input_data import get_sensor_data

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/sensor_data')
def sensor_data():
    """
    센서 데이터 API 엔드포인트
    """
    data = get_sensor_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)