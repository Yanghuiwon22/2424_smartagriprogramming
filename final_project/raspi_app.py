
from fastapi import FastAPI
import serial
from pydantic import BaseModel

PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200

app = FastAPI()
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
import ast

def get_temp_hum_from_ET():
    if not ser.is_open:  # 포트가 닫혀 있으면 열기
        ser.open()

    # ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {PORT} at {BAUD_RATE} baud.")

    while True:
        try:
            print("Waiting for data...")
            # ET보드로부터 데이터 읽기
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()  # 데이터 읽기 및 디코딩

                data_dict_ast = ast.literal_eval(data)

                print(f"Received: {data_dict_ast}")
                return data_dict_ast
            else:
                data_dict_ast = {"temp": "No data", "hum": "No data", "distance": "No data"}
                return data_dict_ast

        except serial.SerialException as e:
            print(f"Serial error: {e}")
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            if 'ser' in locals() and ser.is_open:
                ser.close()
                print("Serial port closed.")
class DataModel(BaseModel):
    data: str

# flask에서 data 전달받기
@app.post("/receive_data")
def receive_data(data: DataModel):
    return {"status": "success", "received_data": data.data}


@app.get("/")
def index():
    return {"message": "Hello, FastAPI on Raspberry Pi!"}


@app.get("/temp_hum")
def temp_hum():

    data_temp_hum = get_temp_hum_from_ET()

    return {"temp": data_temp_hum['temp'],
         "hum": data_temp_hum['hum'],
         "distance": data_temp_hum['distance'],
         "weight": data_temp_hum['weight']}

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("raspi_app:app", host="0.0.0.0", port=5000, reload=True)
