import random

def get_sensor_data():
    """
    센서 데이터를 생성하거나 처리하는 함수.
    추후 데이터베이스 또는 외부 API 연동도 가능.
    """
    return {
        "image_url": "https://example.com/crop_image.jpg",
        "temperature": round(random.uniform(20, 30), 2),  # 임의의 온도 데이터
        "humidity": round(random.uniform(40, 60), 2),    # 임의의 습도 데이터
        "water_level": round(random.uniform(10, 100), 2),  # 임의의 물의 양 데이터
        "irrigation_status": "ON" if random.choice([True, False]) else "OFF"  # 관수 상태
    }
#def draw_graph():
