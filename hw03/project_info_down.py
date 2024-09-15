import requests
import pprint
import json
import ssl
print(ssl.OPENSSL_VERSION)
service_key = "cnFWOksdH2rQuZ9YQs2IR3frMjm2kgy8eauRY4ujdTSTvGEeDGXulTzCIJtU7htSZeFnoof4l6RGh3E"
# url = ("http://apis.data.go.kr/1390802/AgriWeather/WeatherObsrInfo/V2/GnrlWeather/getWeatherTenMinList?serviceKey={service_key}&Page_No=1&Page_Size=20&date=2018-01-01&obsr_Spot_Nm=가평군 가평읍&obsr_Spot_Code=477802A001")
# url = f"https://apis.data.go.kr/1390802/AgriWeather/WeatherObsrInfo/V2/GnrlWeather/getWeatherTenMinList?serviceKey={service_key}&Page_No=1&Page_Size=20&date=2018-01-01&time=1300&obsr_Spot_Nm=%EA%B0%80%ED%8F%89%EA%B5%B0%20%EA%B0%80%ED%8F%89%EC%9D%8D&obsr_Spot_Code=477802A001"
url = f"http://apis.data.go.kr/1390802/AgriWeather/WeatherObsrInfo/V2/GnrlWeather/getWeatherTenMinList?serviceKey=wIdqPjRtIkrKsaya4kGkAD%2Bo8FsV1GsN4rIyX6ntn7GlYSZr%2FgP%2FtVa1ZDeRcP04jDjy93oziypc5RMFwFM4Mg%3D%3D&Page_No=1&Page_Size=20&date=2018-01-01&time=1300&obsr_Spot_Nm=%EA%B0%80%ED%8F%89%EA%B5%B0%20%EA%B0%80%ED%8F%89%EC%9D%8D&obsr_Spot_Code=477802A001"
response =requests.get(url, verify=False)
content =response.text

print(response.content)
