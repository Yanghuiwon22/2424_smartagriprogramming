import streamlit as st
from settings import *
from datetime import date, timedelta
import pandas as pd

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