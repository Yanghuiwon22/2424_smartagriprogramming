import datetime
import requests
import json
import xmltodict
from matplotlib import pyplot as plt
import matplotlib.font_manager as fm


#요청인자

page_no = "1"
page_size ="20"
spot_nm = "가평군 "
spot_code = ""

# key
service_key = "wIdqPjRtIkrKsaya4kGkAD%2Bo8FsV1GsN4rIyX6ntn7GlYSZr%2FgP%2FtVa1ZDeRcP04jDjy93oziypc5RMFwFM4Mg%3D%3D"
# 데이터 반복해서 가져오기
start_date = datetime.datetime(2024, 1, 10)
days = 7

#일주일 날씨 데이터
week_temp =[]
week_date = []

for i in range(days):
    end_date = start_date - datetime.timedelta(days=i)
    date = end_date.strftime("%Y-%m-%d")

    time = "1300"

    url =f"http://apis.data.go.kr/1390802/AgriWeather/WeatherObsrInfo/V2/GnrlWeather/getWeatherTenMinList?serviceKey={service_key}&Page_No={page_no}&Page_Size={page_size}&date={date}&time={time}&obsr_Spot_Nm={spot_nm}&obsr_Spot_Code={spot_code}"

    response =requests.get(url)
    content =response.text
    # json 변환
    xml_dict = xmltodict.parse(content)

    # 데이터 리스트에 넣기
    if 'response' in xml_dict and 'body' in xml_dict['response']:
        content = xml_dict['response']['body']['items']['item']
        week_temp.append(content['temp'])
        week_date.append(content['date'])

        # 날짜 뒤 13:00 시간 자르기(2024-01-04 13:00 -> 2024-01-04)
        week_date = [date.split()[0] for date in week_date]

week_temp.reverse()
week_date.reverse()
# 리스트 "0.4"-> 0.4 (float 형식)으로 바꾸기
week_temp = [float(temp.replace("'", "")) for temp in week_temp]

print(week_temp)
print(week_date)

# 데이터 그래프
x = week_date
y = week_temp

# 한글 폰트, 음수 오류 잡기
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

#그래프 그리기
plt.figure(figsize=(10, 5))
plt.plot(x,y, color ='red', marker='o')

plt.title("일주일 기온")
plt.xlabel('날짜')
plt.ylabel('기온 (°C)')

plt.show()
