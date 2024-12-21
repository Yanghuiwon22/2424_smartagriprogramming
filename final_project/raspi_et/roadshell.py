from machine import Pin
import time

# 핀 설정 (DT와 SCK를 실제 사용 핀 번호로 설정)
DT_PIN = 2  # 데이터 핀
SCK_PIN = 3  # 클럭 핀

# HX711 초기화
hx = HX711(clock=Pin(SCK_PIN, Pin.OUT), data=Pin(DT_PIN, Pin.IN))

# 영점 조정
print("Taring... Make sure the scale is empty.")
hx.tare(times=15)
print("Tare complete.")

# 스케일 보정 (1그램 단위로 설정)
hx.set_scale(scale=1)

# 무게 측정 루프
while True:
    try:
        weight = hx.get_units()  # 무게 측정
        print("Weight: {:.2f} grams".format(weight))
    except Exception as e:
        print("Error:", e)
    time.sleep(1)
