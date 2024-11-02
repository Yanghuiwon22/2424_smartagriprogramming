import streamlit as st
import time
from datetime import datetime, timedelta
from func import jbnu_aws_data
import altair as alt

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
        height: 150px;
        border: 5px solid black;
        margin: 10px auto;
        border-radius: 20px;
    }
    
    .box-title {
        text-align: center;
        padding: 3px;
        font-size: 30px;
        padding-top : 10px;
        color : black

    }
    
    .box-content {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        color : black
    }
    
    </style>
    """,
    unsafe_allow_html=True,
)

# =================================================== streamlit content 구성 ============================================

data = jbnu_aws_data()  # 데이터를 가져오고 변환

# 데이터가 존재하는지 확인
if not data.empty:  # 데이터프레임이 비어 있지 않다면
    # 가장 최근 데이터
    latest_data = data.iloc[-1]  # 첫 번째 행을 선택

    updated_time = latest_data['Date']
    # 실시간 데이터 출력

    if float(latest_data['온도']) > 30.0:
        temperature_color = RED
    elif float(latest_data['온도']) <= 10.0:
        temperature_color = BLUE
    else:
        temperature_color = DEFAULT_COLOR

    if float(latest_data['습도']) > 80.0:
        humidity_color = RED
    elif float(latest_data['습도']) <= 20.0:
        humidity_color = BLUE
    else:
        humidity_color = DEFAULT_COLOR

    if float(latest_data['일사량']) > 700.0:
        lux_color = RED
    elif float(latest_data['일사량']) <= 300.0:
        lux_color = BLUE
    else:
        lux_color = DEFAULT_COLOR

    if float(latest_data['풍속']) > 1.5:
        wind_speed_color = RED
    elif float(latest_data['풍속']) <= 0.3:
        wind_speed_color = BLUE
    else:
        wind_speed_color = DEFAULT_COLOR

    if float(latest_data['강우']) > 0.0:
        rain_color = BLUE
    else:
        rain_color = DEFAULT_COLOR

    # st.write(f"Temperature: {latest_data['온도']}°C")
    # st.write(f"Humidity: {latest_data['습도']}%")
    # st.write(f"Lux: {latest_data['일사량']}")
    # st.write(f"Wind direction: {latest_data['풍향']}")
    # st.write(f"Wind speed: {latest_data['풍속']} m/s")
    # st.write(f"Rain: {latest_data['강우']} mm")
    # st.write(f"Battery: {latest_data['베터리 전압']}")
# ============================================== steamlit layout 구성 ==================================================
st.markdown("<h1 style='text-align: center; color: black;'>🖥️전북대 기상대 활용한 모니터링 시스템🖥️</h1>", unsafe_allow_html=True) # 제목 + 가운데 정렬


# st.markdown("<h3 style='text-align: center; color: black;'>실시간 기상 데이터</h1>", unsafe_allow_html=True) # 제목 + 가운데 정렬
# 네모난 상자 출력
monitoring_elements = {'🌡️온도🌡️': {'data': f"{latest_data['온도']}°C", 'color': temperature_color},
                       '💧습도💧' : {'data': f"{latest_data['습도']}%", 'color': humidity_color},
                       '🌞일사량🌞' : {'data': f"{latest_data['일사량']}", 'color': lux_color},
                       '🧭풍향🧭' : {'data': f"{latest_data['풍향']}", 'color': DEFAULT_COLOR},
                       '💨풍속💨' : {'data': f"{latest_data['풍속']}m/s", 'color': wind_speed_color},
                       '🌧️강우🌧️' : {'data': f"{latest_data['강우']}mm", 'color': rain_color},
                       '🔋배터리전압🔋' : {'data': f"{latest_data['베터리 전압']}", 'color': DEFAULT_COLOR}}

st.markdown(
'<div class="box" style="width:100%; display: flex; flex-direction: column; border: dashed">'+
"<h3 style='text-align: center; color: black;'>실시간 기상 데이터</h3>" +
    '<div class="boxes">' + ''.join(
    [f'<div class="box" style="background-color: {value["color"]}"><div class="box-title">{key}</div><div class="box-content">{value["data"]}</div></div>' for key, value in monitoring_elements.items()]
) + '</div>' + '</div>', unsafe_allow_html=True)








# Add a hint about the rerun
# st.write("This app will rerun in 5 seconds...")
#
# data = jbnu_aws_data()  # 데이터를 가져오고 변환
#
# # 데이터가 존재하는지 확인
# if not data.empty:  # 데이터프레임이 비어 있지 않다면
#     # 가장 최근 데이터
#     latest_data = data.iloc[-1]  # 첫 번째 행을 선택
#
#     updated_time = latest_data['Date']
#     st.write(f'Updated Time: {updated_time}')
#
#     # 실시간 데이터 출력
#     # st.write(f"Temperature: {latest_data['온도']}°C")
#     # st.write(f"Humidity: {latest_data['습도']}%")
#     # st.write(f"Lux: {latest_data['일사량']}")
#     # st.write(f"Wind direction: {latest_data['풍향']}")
#     # st.write(f"Wind speed: {latest_data['풍속']} m/s")
#     # st.write(f"Rain: {latest_data['강우']} mm")
#     # st.write(f"Battery: {latest_data['베터리 전압']}")
#
#     st.write(data)
#
#     # 24시간 데이터 시각화
#     chart = alt.Chart(data).mark_line().encode(
#         x='Date',
#         y=alt.Y('온도:Q',
#                 scale=alt.Scale(domain=[10, 45]),
#                 axis=alt.Axis(tickMinStep=5)
#                 )  # y축 최소값 0, 최대값 50 설정
#     )
#
#
#     st.altair_chart(chart, use_container_width=True)
#
#
# else:
# #     st.write("No data available.")
#
# time.sleep(60*10)
# st.rerun()