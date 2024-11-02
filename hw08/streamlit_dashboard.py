import streamlit as st
import time
from datetime import datetime, timedelta
from func import get_aws
import altair as alt
import matplotlib.pyplot as plt
import pandas as pd

import streamlit_kakao_alarm
import streamlit_text_alarm

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
        cursor: pointer;  /* 클릭 가능하게 설정 */
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

# 그래프 생성 함수
def plot_graph(data, metric):
    plt.figure(figsize=(10, 5))
    plt.plot(data['datetime'], data[metric], marker='o')
    plt.title(f"{metric} 시간에 따른 변화")
    plt.xlabel("시간")
    plt.ylabel(metric)
    st.pyplot(plt)

def display():
    # 테스트용

    # ===============


    data = get_aws(datetime.now().date())  # 데이터를 가져오고 변환

    # 상자 클릭 시 상태 저장을 위한 session_state 초기화
    if 'selected_metric' not in st.session_state:
        st.session_state.selected_metric = None


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


        # st.write(f"Temperature: {latest_data['온도']}°C")
        # st.write(f"Humidity: {latest_data['습도']}%")
        # st.write(f"Lux: {latest_data['일사량']}")
        # st.write(f"Wind direction: {latest_data['풍향']}")
        # st.write(f"Wind speed: {latest_data['ws']} m/s")
        # st.write(f"Rain: {latest_data['강우']} mm")
        # st.write(f"Battery: {latest_data['베터리 전압']}")
    # ============================================== steamlit layout 구성 ==================================================
    st.markdown("<h1 style='text-align: center; color: black;'>🖥️전북대 기상대 활용한 모니터링 시스템🖥️</h1>", unsafe_allow_html=True) # 제목 + 가운데 정렬

    # 네모난 상자 출력
    monitoring_elements = {'🌡️온도🌡️': {'data': f"{latest_data['temp']}°C", 'color': temperature_color},
                           '💧습도💧' : {'data': f"{latest_data['hum']}%", 'color': humidity_color},
                           '🌞일사량🌞' : {'data': f"{latest_data['rad']}", 'color': lux_color},
                           '🧭풍향🧭' : {'data': f"{latest_data['wd']}", 'color': DEFAULT_COLOR},
                           '💨풍속💨' : {'data': f"{latest_data['ws']}m/s", 'color': wind_speed_color},
                           '🌧️강우🌧️' : {'data': f"{latest_data['rain']}mm", 'color': rain_color},
                           '🔋배터리전압🔋' : {'data': f"{latest_data['bv']}", 'color': DEFAULT_COLOR}}

    # 상자 출력
    st.markdown(
        '<div class="box" style="width:100%; height:100%; display: flex; flex-direction: column; border: dashed;">' +
        "<h3 style='text-align: center; color: black;'>실시간 기상 데이터</h3>" +
        '<div class="boxes">' + ''.join(
            [f'<div class="box" style="background-color: {value["color"]};" ' +
             f'onclick="window.parent.postMessage({{\'metric\': \'{key}\'}});">' +  # 메트릭을 메시지로 보냄
             f'<div class="box-title">{key}</div><div class="box-content">{value["data"]}</div>' +
             '</div>' for key, value in monitoring_elements.items()]
        ) + '</div>' + '</div>', unsafe_allow_html=True)

    # 선택된 메트릭에 따라 그래프 표시
    metric = st.session_state.get('selected_metric')
    if metric:
        st.markdown(f"<h3>{metric} 그래프</h3>", unsafe_allow_html=True)
        plot_graph(data, metric)  # 여기서 plot_graph(data, metric) 함수 호출

    # st.markdown(
    # '<div class="box" style="width:100%; display: flex; flex-direction: column; border: dashed">'+
    # "<h3 style='text-align: center; color: black;'>실시간 기상 데이터</h3>" +
    #     '<div class="boxes">' + ''.join(
    #     [f'<div class="box" style="background-color: {value["color"]}"><div class="box-title">{key}</div><div class="box-content">{value["data"]}</div></div>' for key, value in monitoring_elements.items()]
    # ) + '</div>' + '</div>', unsafe_allow_html=True)
    #
    # # 클릭한 메트릭을 세션 상태에 저장
    # for key in monitoring_elements.keys():
    #     if st.button(f"{key} 선택"):
    #         st.session_state.selected_metric = key
    #
    # # 선택된 메트릭에 따라 그래프 표시
    # if st.session_state.selected_metric:
    #     metric = st.session_state.selected_metric
    #     st.markdown(f"<h3>{metric} 그래프</h3>", unsafe_allow_html=True)
    #     plot_graph(data, metric)  # 여기서 plot_graph(data, metric) 함수는 구현되어야 함
    #


# 사이드바
option = st.sidebar.radio(
    "옵션을 선택하세요:",
    options=['DASHBOARD', "카카오톡 알람", "문자 알람"],
    index=0  # 기본값을 첫 번째 옵션(옵션 1)으로 설정
)

if option == 'DASHBOARD':
    display()

if option == '카카오톡 알람':
    streamlit_kakao_alarm.display()

if option == '문자 알람':
    streamlit_text_alarm.display()
