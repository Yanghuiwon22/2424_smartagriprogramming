import streamlit as st
from settings import *
from datetime import date, timedelta
import pandas as pd
import matplotlib.pyplot as plt

def plot_graph(data, metric):
    # Matplotlib의 한글 폰트 설정
    plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False

    if not data.empty:

        data['datetime'] = pd.to_datetime(data['datetime'], errors='coerce')
        st.line_chart(data.set_index('datetime')[metric], use_container_width=True)

        # 주석 추가
        start_time = data['datetime'].min()
        end_time = data['datetime'].max()
        annotation_text = f"<{start_time.strftime('%Y-%m-%d %H:%M')} ~ {end_time.strftime('%Y-%m-%d %H:%M')} 그래프>"
        st.markdown(f"<div style='text-align: center; font-size: 12px;'>{annotation_text}</div>",
                    unsafe_allow_html=True)

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

        # 처음과 마지막 데이터 포인트 추출
        start_time = data['datetime'].min()
        end_time = data['datetime'].max()


        # 주석 추가
        annotation_text = f"<{start_time.strftime('%Y-%m-%d %H:%M')} ~ {end_time.strftime('%Y-%m-%d %H:%M')} 그래프>"
        st.markdown(f"<div style='text-align: center; font-size: 12px;'>{annotation_text}</div>",
                    unsafe_allow_html=True)

    else:
        st.write("데이터가 없습니다.")


def display():
    st.markdown("<h1 style='text-align: center; color: black;'>🖥️전북대 기상대 기상 조회하기🖥️</h1>",
                unsafe_allow_html=True)  # 제목 + 가운데 정렬


    min_date = date(2024, 11, 1)
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("시작 날짜를 선택하세요:", key='start_date', value=date.today(), min_value=min_date, max_value=date.today())
        # start_date = pd.to_datetime(start_date)
    with col2:
        end_date = st.date_input("종료 날짜를 선택하세요:", key='end_date', value=date.today(), min_value=min_date, max_value=date.today())
        # end_date = pd.to_datetime(end_date)


    if end_date < start_date:
        st.warning("경고: 종료 날짜가 시작 날짜보다 이전입니다. 올바른 날짜를 선택해주세요.")
    else:
        st.markdown(f"<h3 style='text-align: center; color: black;'>{start_date}부터 {end_date}까지</h3>",
                    unsafe_allow_html=True)

    # github로부터 df 가져오기
    date_set = set()  # 중복 방지를 위해 set 사용
    current_date = start_date

    while current_date <= end_date:
        # {year}_{month} 형식으로 추가
        date_set.add(current_date.strftime("%Y_%m"))
        current_date += timedelta(days=1)

    # 결과를 리스트로 변환 후 정렬
    date_list = sorted(date_set)
    # print("두 날짜 사이의 {year}_{month} 형식 리스트:", date_list)



    df_total = pd.DataFrame()
    for target_date in date_list:
        url = f"https://raw.githubusercontent.com/Yanghuiwon22/2424_smartagriprogramming/refs/heads/main/hw08/output/AWS/{target_date}.csv"
        # print(url)
        df = pd.read_csv(url)

        df_total = pd.concat([df_total, df])

    df_total['date'] = pd.to_datetime(df_total['datetime']).dt.date
    filtered_df = df_total[(df_total['date'] >= start_date) & (df_total['date'] <= end_date)]

    st.dataframe(filtered_df)

# 네모난 상자 출력
    monitoring_elements = {'🌡️온도🌡️': { 'metric': 'temp'},
                           '💧습도💧' : {'metric': 'hum'},
                           '🌞일사량🌞' : {'metric': 'rad'},
                           '🧭풍향🧭' : {'metric': 'wd'},
                           '💨풍속💨' : { 'metric': 'ws'},
                           '🌧️강우🌧️' : {'metric': 'rain'},
                           '🔋배터리전압🔋' : {'metric': 'bv'},}

# 탭 생성 (풍향 탭을 제외)
    filtered_elements = {key: value for key, value in monitoring_elements.items() if key != '🧭풍향🧭'}
    tabs = st.tabs(filtered_elements.keys())

    # 각 탭에 맞는 그래프 추가
    for tab, (key, value) in zip(tabs, filtered_elements.items()):
        with tab:
            metric_name = value['metric']  # 데이터프레임의 열 이름

            st.markdown(f"<h3>{key} 그래프</h3>", unsafe_allow_html=True)  # 그래프 제목

            # 강우 탭에는 막대 그래프로, 그 외는 선 그래프로 그리기
            if metric_name == 'rain':
                plot_bar_graph(filtered_df, metric_name)  # 막대 그래프 함수 호출
            else:
                plot_graph(filtered_df, metric_name)  # 선 그래프 함수 호출
