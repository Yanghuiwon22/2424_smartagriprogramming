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
    with col2:
        end_date = st.date_input("종료 날짜를 선택하세요:", key='end_date', value=date.today(), min_value=min_date, max_value=date.today())

    if end_date < start_date:
        st.warning("경고: 종료 날짜가 시작 날짜보다 이전입니다. 올바른 날짜를 선택해주세요.")
    else:
        st.markdown(f"<h3 style='text-align: center; color: black;'>{start_date}부터 {end_date}까지</h3>",
                    unsafe_allow_html=True)

    # github로부터 df 가져오기
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)

    print(date_list)
    df_total = pd.DataFrame()
    for target_date in date_list:
        url = f"https://raw.githubusercontent.com/Yanghuiwon22/2424_smartagriprogramming/refs/heads/main/hw08/output/AWS/{target_date.year}_{target_date.month}.csv"
        print(url)
        df = pd.read_csv(url)

        df_total = pd.concat([df_total, df])
    print(df_total)



    # CSV 파일 읽어오기
