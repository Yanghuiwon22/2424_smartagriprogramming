import requests
import pprint
import json
import xmltodict

#요청인자
page_no = "1"
page_size ="20"
date = "2024-01-01"
time= "1300"
spot_nm ="전주시 송천동"
spot_code = ""

#url, key
service_key = "wIdqPjRtIkrKsaya4kGkAD%2Bo8FsV1GsN4rIyX6ntn7GlYSZr%2FgP%2FtVa1ZDeRcP04jDjy93oziypc5RMFwFM4Mg%3D%3D"

url =f"http://apis.data.go.kr/1390802/AgriWeather/WeatherObsrInfo/V2/GnrlWeather/getWeatherTenMinList?serviceKey={service_key}&Page_No={page_no}&Page_Size={page_size}&date={date}&time={time} & obsr_Spot_Nm={spot_nm}&obsr_Spot_Code={spot_code}"

response =requests.get(url)
content =response.text
# json 변환
xml_dict = xmltodict.parse(content)
json_data = json.dumps(xml_dict)

print(json_data)
