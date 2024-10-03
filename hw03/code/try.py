# base time: 0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300 (1일 8회
import requests
import xmltodict
import datetime
import pandas as pd
from matplotlib import pyplot as plt


# 지역 입력
# data('지역을 입력해 주세요 (ex: 전북특별자치도 전주시 덕진구 송천1동): ')

# 요청인자
service_key = 'wIdqPjRtIkrKsaya4kGkAD%2Bo8FsV1GsN4rIyX6ntn7GlYSZr%2FgP%2FtVa1ZDeRcP04jDjy93oziypc5RMFwFM4Mg%3D%3D'
# base_date = data('날짜를 입력해 주세요 : ')
base_date = '20240919'
base_times = ['0200', '0500', '0800', '1100', '1400', '1700', '2000', '2300']
nx = 63
ny = 97

# 빈 리스트, 딕셔너리
day_time = []
day_temp = []

# time_temp ={}

for base_time in base_times:
    url = f'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey={service_key}&numOfRows=10&pageNo=1&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}'

    response =requests.get(url)
    content =response.text
    # json 변환
    xml_dict = xmltodict.parse(content)
    content = xml_dict['response']['body']['items']['item']
    # day_temp 딕셔너리에 {0200 : 25} 같이 시간과 기온을 저장
    for item in content:
        if item['category'] == 'TMP':
            # time_temp[item['fcstTime']] = item['fcstValue']
            day_time.append(item['fcstTime'])
            day_temp.append(item['fcstValue'])
        # print(item['fcstValue'])

print(day_time)
print(day_temp)

# 시간을 변환하는 함수
def format_time(time_str):
    # '0200'을 받아서 '2시'로 변환
    hour = int(time_str[:2])
    return f"{hour}시"


formatted_time = [format_time(t) for t in day_time]
# 데이터 그래프

x = formatted_time
y = day_temp

# 한글 폰트, 음수 오류 잡기
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

#그래프 그리기
plt.figure(figsize=(10, 5))
plt.plot(x,y, color ='red', marker='o')

plt.title("하루 기온")
plt.xlabel('날짜')
plt.ylabel('기온 (°C)')

plt.show()