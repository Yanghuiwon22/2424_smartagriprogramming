import requests
import xmltodict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
import pandas as pd
from matplotlib import pyplot as plt

# 요청 인자
page_no = "1"
page_size = "20"
spot_nm = "가평군 "
spot_code = ""

# key
service_key = "cnFWOksdH2rQuZ9YQs2IR3frMjm2kgy8eauRY4ujdTSTvGEeDGXulTzCIJtU7htSZeFnoof4l6RGh3EpVIbo1Q%3D%3D"

# 시작 날짜 및 기간
start_date = datetime(2024, 1, 10)
days = 7
time_format = "%H%M"
start_time = datetime.strptime("0010", time_format)

# 결과를 저장할 리스트
results = []

def fetch_weather_data(date, time):
    """날짜와 시간을 받아 API로부터 데이터를 가져오는 함수"""
    if time == '0000':
        time = "2400"
    url = f"http://apis.data.go.kr/1390802/AgriWeather/WeatherObsrInfo/V2/GnrlWeather/getWeatherTenMinList?serviceKey={service_key}&Page_No={page_no}&Page_Size={page_size}&date={date}&time={time}&obsr_Spot_Nm={spot_nm}&obsr_Spot_Code={spot_code}"
    response = requests.get(url)
    content = response.text
    xml_dict = xmltodict.parse(content)

    # 필요한 데이터 추출
    if 'response' in xml_dict and 'body' in xml_dict['response']:
        content = xml_dict['response']['body']['items']['item']
        date__ = content['date'].split(' ')[0]
        time__ = content['date'].split(' ')[1]

        # print(date__, time__, content['temp'])
        if time__ == "24:00":
            time__ = "00:00"
            date__ = (datetime.strptime(date__, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")

            return (date__, time__, content['temp'], content['hum'], content['wind'])

        else:
            return (date__, time__, content['temp'], content['hum'], content['wind'])


def api_get():
# 병렬 처리로 데이터를 가져옴
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for i in range(days):
            end_date = start_date + timedelta(days=i)
            date = end_date.strftime("%Y-%m-%d")
            current_time = start_time

            # 10분 간격으로 날씨 데이터를 가져오는 작업을 병렬로 처리
            for j in range(24 * 7):
                time = current_time.strftime(time_format)
                a = executor.submit(fetch_weather_data, date, time)
                futures.append(a)
                current_time += timedelta(minutes=10)

        # 결과 처리
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

        # 리스트를 데이터프레임으로 변환
    df = pd.DataFrame(results, columns=['date', 'time', 'temp', 'hum', 'wind'])

    # 데이터프레임 확인
    df.sort_values(by=['date', 'time'], inplace=True)  # 날짜와 시간 순으로 정렬
    df.to_csv('weather_data.csv', index=False)



def draw_graph():
    df = pd.read_csv('weather_data.csv')
    # 날짜와 시간을 결합하여 x축 데이터 생성
    print(df.head(144))

    plt.rcParams['font.family'] = 'NanumGothic'
    plt.rcParams['axes.unicode_minus'] = False

    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'].str[:2] + ':' + df['time'].str[3:])

    # 그래프 그리기
    plt.figure(figsize=(10, 5))
    plt.plot(df['datetime'], df['temp'], color='red', marker='o')

    plt.title("일주일 기온")
    plt.xlabel('날짜 및 시간')
    plt.ylabel('기온 (°C)')

    plt.xticks(rotation=45)  # x축 라벨 회전
    plt.tight_layout()
    plt.show()

api_get()
# draw_graph()