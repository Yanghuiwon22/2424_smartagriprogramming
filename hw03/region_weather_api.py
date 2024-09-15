import requests
import xmltodict
import json

# api를 통해 데이터를 얻기 위한 파라미터
key = 'cnFWOksdH2rQuZ9YQs2IR3frMjm2kgy8eauRY4ujdTSTvGEeDGXulTzCIJtU7htSZeFnoof4l6RGh3EpVIbo1Q%3D%3D'
page_no = '1'
page_size = '144'
date = '2018-01-01'
time = ''
obsr_spot_np = '익산시 영등동 하나로13길 24'
obsr_spot_code = ''

# api를 통해 데이터 얻기
url = f'https://apis.data.go.kr/1390802/AgriWeather/WeatherObsrInfo/V2/GnrlWeather/getWeatherTenMinList?serviceKey={key}&Page_No={page_no}&Page_Size={page_size}&date={date}&time={time}&obsr_Spot_Nm={obsr_spot_np}&obsr_Spot_Code={obsr_spot_code}'
response = requests.get(url)
content_xml = response.text

# xml -> dict -> json
content_dict = xmltodict.parse(content_xml)
content_json = json.dumps(content_dict, indent=4)

# json데이터에서 필요한 부분 추출하기


