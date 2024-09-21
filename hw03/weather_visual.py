import requests
import xmltodict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

# 요청 인자
page_no = "1"
page_size = "20"
spot_nm = "가평군 "
spot_code = ""

# key
service_key = "cnFWOksdH2rQuZ9YQs2IR3frMjm2kgy8eauRY4ujdTSTvGEeDGXulTzCIJtU7htSZeFnoof4l6RGh3EpVIbo1Q%3D%3D"

# 시작 날짜 및 기간
# start_date = datetime(2024, 1, 10)
days = 7
time_format = "%H%M"
start_time = datetime.strptime("0010", time_format)

# 결과를 저장할 리스트
results = []
def get_address(address_input):

    address_do = address_input.split(' ')[0]
    address_si = address_input.split(' ')[1]

    # df = pd.read_csv('static/spot_nm.txt')
    #
    # df = df[['도명', '지점명', '지점코드']]
    # df['지점명1'] = df['지점명'].apply(lambda x: x.split(' ')[0])
    # df['지점명2'] = df['지점명'].apply(lambda x: x.split(' ')[1])
    #
    # df.insert(1, '지점명1', df.pop('지점명1'))
    # df.insert(2, '지점명2', df.pop('지점명2'))
    # df = df.drop(columns=['지점명'])
    # df.to_csv('static/df_after.csv')

    df = pd.read_csv('static/df_after.csv')
    try:
        if address_do in df['도명'].values:
            if address_si in df['지점명1'].values:
                print(address_do, address_si)
                index = df[df['지점명1'] == address_si].index
                print(df['지점코드'][index])
                return f'{address_do} {address_si}'
            else:
                return f'{address_do} {address_si}에 대한 데이터 없습니다.'
        else:
            print(f'{address_do}에 대한 데이터 없습니다')
            return f'{address_do}에 대한 데이터 없습니다'
    except:
        return '로드 실패 : 관리자에게 문의'

def fetch_weather_data(date, time, spot_code):

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


def api_get(start_date=datetime.now()):
# 병렬 처리로 데이터를 가져옴
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for i in range(days):
            end_date = start_date - timedelta(days=i)
            print(end_date)
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


    df.to_csv('static/weather_data.csv', index=False)

    draw_graph()




def draw_graph():
    df = pd.read_csv('static/weather_data.csv')
    # 날짜와 시간을 결합하여 x축 데이터 생성
    print(df.head(144))

    plt.rcParams['font.family'] = 'NanumGothic'
    plt.rcParams['axes.unicode_minus'] = False

    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'].str[:2] + ':' + df['time'].str[3:])

    # 기온 그래프 그리기
    fig, ax1 = plt.subplots(figsize=(10,5))

    ax1.plot(df['datetime'], df['temp'], color = '#f05650', lw=2, label='온도')
    ax1.grid(axis="y", alpha=0.5)
    ax1.set_title("일주일 기온")
    ax1.set_xlabel('날짜 및 시간')
    ax1.set_ylabel('기온 (°C)')
    ax1.spines['left'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.tick_params(axis='y', color='#f05650',labelcolor='#f05650')
    ax1.set_yticks(np.arange(-15, 45.5, 5.5))
    # ax1.set_yticks(np.linspace(-15, 45, 5))

    # 습도 그래프 그리기
    ax2 = ax1.twinx()
    ax2.plot(df['datetime'],df['hum'], color='#1560BD',lw=2, label='습도')
    ax2.grid(axis="y",alpha=0.5, linestyle = '--')
    ax2.set_ylabel('습도')
    # ax2.spines['left'].set_color('#f05650')
    # ax2.spines['right'].set_color('#1560BD')
    ax2.spines['left'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.tick_params(axis='y', color='#1560BD', labelcolor='#1560BD')
    ax2.set_yticks(np.arange(0, 110, 10))
    # ax2.set_yticks(np.linspace(0, 100, 5))


    # 범례
    ax1.legend(loc='lower right',bbox_to_anchor=(0.9,1.0))
    ax2.legend(loc='lower right',bbox_to_anchor=(1.0,1.0))

    fig.tight_layout()
    fig.show()
    fig.savefig('./static/img/temp.png')






# api_get()
# draw_graph()
get_address('전라북도 익산시')