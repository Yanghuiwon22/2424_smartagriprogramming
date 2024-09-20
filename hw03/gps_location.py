import uvicorn
from fastapi import FastAPI
from markupsafe import escape
import requests

app= FastAPI()

# key =  7F232D24-1336-390E-9B68-F17F45877199
url = "https://api.vworld.kr/req/address?"

params = {
	"service": "address",
	"request": "getcoord",
	"crs": "epsg:4326",
	"address": "판교로 242",
	"format": "json",
	"type": "road",
	"key": "7F232D24-1336-390E-9B68-F17F45877199"
}

response = requests.get(url, params=params)
if response.status_code == 200:
	print(response.json())
@app.get("/")
def root():
    return f'Hello World'



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

