import os.path
import time
from datetime import datetime
import streamlit as st
import pandas as pd
from settings import *
import requests
from bs4 import BeautifulSoup

def display():
    st.markdown("<h1 style='text-align: center; color: black;'>🖥️전북대 기상대 모니터링 카카오톡으로 알람받기🖥️</h1>",
                unsafe_allow_html=True)  # 제목 + 가운데 정렬

    if "email" not in st.session_state:
        st.session_state.email = ""

    # 이메일 입력 받기
    kakao_email = st.text_input("이메일을 입력하세요:", st.session_state.email)

    if kakao_email:
        st.session_state.email = kakao_email
    else:
        print('값이 전달되지 않음.')

    print(st.session_state.email)

    # Enter 누르면 세션 상태에 이메일 값을 업데이트
    # if email:
    #     st.session_state.email = email
    #
    # # 확인 출력
    # st.write("입력한 이메일:", st.session_state.email)
    # with st.form(key="my_form"):
    #     col1, col2 = st.columns([3, 1])  # col1, col2 레이아웃 생성
    #
    #     with col1:
    #         kakao_email = st.text_input("카카오톡 이메일", label_visibility="collapsed")
    #
    #     with col2:
    #         kakao_button = st.form_submit_button("확인")
    #
    # if kakao_button:
    #     st.write("입력된 이메일:", kakao_email)  # Streamlit에서 출력
    #     print("입력된 이메일:", kakao_email)  # 콘솔에서 출력
    # else:
    #     st.write("이메일이 입력되지 않았습니다.")
    #     print("이메일이 입력되지 않았습니다.")
    #
    #
    if not os.path.exists(os.path.join(FILE_PATH, 'kakao_email.csv')):
        df_email = pd.DataFrame(columns=['date','time', 'email', 'status'])

    else:
        df_email = pd.read_csv(os.path.join(FILE_PATH, 'kakao_email.csv'))

    print(df_email)

    if len(df_email[df_email['email'] == kakao_email]) != 0:
        matching_rows = df_email[df_email['email'] == kakao_email]
        st.write(f'현재 진행 상태 : {matching_rows["status"].values[0]}')
        st.write(f"최초 제출 날짜 : {matching_rows['date'].values[0]} {matching_rows['time'].values[0]}")
    else :
        if kakao_email != '':
            email_dic = {
                'date': datetime.now().date(),
                'time': datetime.now().time().strftime("%H:%M:%S"),
                'email': kakao_email,
                'status': '제출됨'
            }

            st.write('처음 등록하는 이메일입니다.')
            df = pd.DataFrame([email_dic])
            df_email = pd.concat([df, df_email])

    df_email.to_csv(os.path.join(FILE_PATH, 'kakao_email.csv'), index=False)
    #
    st.write('---')
    st.markdown(""" <h3>진행 상태 안내</h3>
    <strong>이메일 처음 등록 시</strong><br>
    '처음 등록하는 이메일입니다' 문구 출력<br>
    <br>
    <strong>이메일 재등록 시</strong><br>
    현재 입력된 이메일의 진행상태를 표시<br>
    제출됨 -> 등록됨(카카오톡으로 알람을 받을 수 있습니다)<br>
    """, unsafe_allow_html=True)
    #
    #
    #
    #
    #
