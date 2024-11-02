import streamlit as st
import time
from datetime import datetime, timedelta
from func import get_aws
import altair as alt
import matplotlib.pyplot as plt
import pandas as pd

import streamlit_kakao_alarm
import streamlit_text_alarm
import kakao_alarm
import vonage_service
import streamlit_weather

st.set_page_config(layout="wide")

# # Display the current time
# current_time = datetime.now().strftime("%H:%M:%S")
# st.write(f"Current Time: {current_time}")

RED = "#F05650"
BLUE = '#617DF8'
DEFAULT_COLOR = 'white'

# ============================================== steamlit css 구성 ==================================================
st.markdown(
    """
    <style>
    .boxes {
        display: flex;
    }

    .box {
        width: 13%;
        height: 100px;
        border: 5px solid black;
        margin: 10px auto;
        border-radius: 20px;
    }
    
    .box-title {
        text-align: center;
        padding: 3px;
        # font-size: 30px;
        padding-top : 10px;
        color : black
    }
    
    .box-content {
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        color : black
    }
    
    </style>
    """,
    unsafe_allow_html=True,
)
# =================================================== streamlit content 구성 ============================================

def plot_graph(data, metric):
    # Matplotlib의 한글 폰트 설정
    plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False

    if not data.empty:

        data['datetime'] = pd.to_datetime(data['datetime'], errors='coerce')
        st.line_chart(data.set_index('datetime')[metric], use_container_width=True)

    else:
        st.write("데이터가 없습니다.")


def plot_bar_graph(data, metric):
    # Matplotlib의 한글 폰트 설정
    plt.rc('font', family='Malgun Gothic')  # Windows의 경우
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 표시

    if not data.empty:
        # datetime 열을 datetime 형식으로 변환
        data['datetime'] = pd.to_datetime(data['datetime'], errors='coerce')  # 변환 시 오류 발생 시 NaT로 설정


        # Streamlit을 사용하여 막대
        st.bar_chart(data.set_index('datetime')[metric])

    else:
        st.write("데이터가 없습니다.")

def display():

    data = get_aws(datetime.now().date())  # 데이터를 가져오고 변환

    # 데이터가 존재하는지 확인
    if not data.empty:  # 데이터프레임이 비어 있지 않다면
        # 가장 최근 데이터
        latest_data = data.iloc[-1]  # 첫 번째 행을 선택

        updated_time = latest_data['datetime']
        # 실시간 데이터 출력

        if float(latest_data['temp']) > 30.0:
            temperature_color = RED
        elif float(latest_data['temp']) <= 10.0:
            temperature_color = BLUE
        else:
            temperature_color = DEFAULT_COLOR

        if float(latest_data['hum']) > 80.0:
            humidity_color = RED
        elif float(latest_data['hum']) <= 20.0:
            humidity_color = BLUE
        else:
            humidity_color = DEFAULT_COLOR

        if float(latest_data['rad']) > 700.0:
            lux_color = RED
        elif float(latest_data['rad']) <= 300.0:
            lux_color = BLUE
        else:
            lux_color = DEFAULT_COLOR

        if float(latest_data['ws']) > 1.5:
            wind_speed_color = RED
        elif float(latest_data['ws']) <= 0.3:
            wind_speed_color = BLUE
        else:
            wind_speed_color = DEFAULT_COLOR

        if float(latest_data['rain']) > 0.0:
            rain_color = BLUE
        else:
            rain_color = DEFAULT_COLOR

    # ============================================== steamlit layout 구성 ==================================================
    st.markdown("<h1 style='text-align: center; color: black;'>🖥️전북대 기상대 활용한 모니터링 시스템🖥️</h1>", unsafe_allow_html=True) # 제목 + 가운데 정렬

    # 네모난 상자 출력
    monitoring_elements = {'🌡온도🌡': {'data': f"{latest_data['temp']}°C", 'color': temperature_color, 'metric': 'temp'},
                           '💧습도💧' : {'data': f"{latest_data['hum']}%", 'color': humidity_color, 'metric': 'hum'},
                           '🌞일사량🌞' : {'data': f"{latest_data['rad']}", 'color': lux_color, 'metric': 'rad'},
                           '🧭풍향🧭' : {'data': f"{latest_data['wd']}", 'color': DEFAULT_COLOR, 'metric': 'wd'},
                           '💨풍속💨' : {'data': f"{latest_data['ws']}m/s", 'color': wind_speed_color, 'metric': 'ws'},
                           '🌧강우🌧' : {'data': f"{latest_data['rain']}mm", 'color': rain_color, 'metric': 'rain'},
                           '🔋배터리전압🔋' : {'data': f"{latest_data['bv']}", 'color': DEFAULT_COLOR, 'metric': 'bv'},}

    st.markdown(
        '<div class="box" style="width:100%; height:100%; display: flex; flex-direction: column; border: dashed;">' +
        "<h3 style='text-align: center; color: black;'>실시간 기상 데이터</h3>" +
        '<div class="boxes">' + ''.join(
        [f'<div class="box" style="background-color: {value["color"]}"><div class="box-title">{key}'
         f'</div><div class="box-content">{value["data"]}</div></div>' for key, value in monitoring_elements.items()]
    ) + '</div>' + '</div>', unsafe_allow_html=True)

    alarm_weather = {}
    if temperature_color != DEFAULT_COLOR:
        alarm_weather['temp'] = latest_data['temp']
    if humidity_color != DEFAULT_COLOR:
        alarm_weather['hum'] = latest_data['hum']
    if lux_color != DEFAULT_COLOR:
        alarm_weather['rad'] = latest_data['rad']
    if wind_speed_color != DEFAULT_COLOR:
        alarm_weather['ws'] = latest_data['ws']
    if rain_color != DEFAULT_COLOR:
        alarm_weather['rain'] = latest_data['rain']

    if alarm_weather:
        kakao_alarm.main(alarm_weather)
        vonage_service.send_sms(alarm_weather)

    # 그래프 생성
    # 탭 생성 (풍향 탭을 제외)
    filtered_elements = {key: value for key, value in monitoring_elements.items() if key != '🧭풍향🧭'}
    tabs = st.tabs(filtered_elements.keys())

    # 각 탭에 그래프 추가
    for tab, (key, value) in zip(tabs, filtered_elements.items()):
        with tab:
            metric_name = value['metric']  # 데이터프레임의 열 이름

            st.markdown(f"<h5 style='text-align: center; color: black;'>오늘의 시간대별 {key[1:-1]} 변화 그래프</h5>",
                        unsafe_allow_html=True)  # 제목 + 가운데 정렬

            # 강우 탭에는 막대 그래프로, 그 외는 선 그래프로 그리기
            if metric_name == 'rain':
                plot_bar_graph(data, metric_name)
            else:
                plot_graph(data, metric_name)


# 사이드바
option = st.sidebar.radio(
    "옵션을 선택하세요:",
    options=['DASHBOARD', "기상 조회","카카오톡 알람", "문자 알람"],
    index=0  # 기본값을 첫 번째 옵션(옵션 1)으로 설정
)

if option == 'DASHBOARD':
    display()

if option == '기상 조회':
    streamlit_weather.display()

if option == '카카오톡 알람':
    streamlit_kakao_alarm.display()

if option == '문자 알람':
    streamlit_text_alarm.display()
