import pandas as pd
import requests
import xmltodict
import json

# api를 통해 데이터를 얻기 위한 파라미터
key = 'cnFWOksdH2rQuZ9YQs2IR3frMjm2kgy8eauRY4ujdTSTvGEeDGXulTzCIJtU7htSZeFnoof4l6RGh3EpVIbo1Q%3D%3D'
page_no = '1'
page_size = '144'
date = '2018-01-01'
time = ''
obsr_spot_np = '가평군 가평읍'
obsr_spot_code = ''

# api를 통해 데이터 얻기
url = f'https://apis.data.go.kr/1390802/AgriWeather/WeatherObsrInfo/V2/GnrlWeather/getWeatherTenMinList?serviceKey={key}&Page_No={page_no}&Page_Size={page_size}&date={date}&time={time}&obsr_Spot_Nm={obsr_spot_np}&obsr_Spot_Code={obsr_spot_code}'
response = requests.get(url)
content_xml = response.text

# xml -> dict -> json
content_dict = xmltodict.parse(content_xml)
# content_json = json.dumps(content_dict, indent=4)

# json데이터에서 필요한 부분 추출하기 --> 데이터프레임으로 만들기
contents = content_dict['response']['body']['items']['item']

for content in contents:
    if not 'df' in locals():
        df = pd.DataFrame([content])

    else:
        content_df = pd.DataFrame([content])
        df = pd.concat([df, content_df], ignore_index=True)



df = df.drop(columns=['no', 'stn_Code'])

# 컬럼명 직관적이게 수정
df_key = df.keys()
df_re_key = ['관측지점명', '관측시각', '기온(℃)', '최고기온(℃)', '최저기온(℃)', '습도(%)', '풍향', '풍속(m/s)', '최대풍속(m/s)',
             '강수량(mm)', '일조시간(MM)', '일사량(MJ/m²)', '결로시간(MM)', '초상온도(℃)', '지중온도(℃)', '토양수분보정값(%)']
# df.rename()
print(df)

df.to_csv('weather_data.csv')


