import streamlit as st
import os
from settings import *
import pandas as pd
from datetime import datetime
def display():

    st.markdown("<h1 style='text-align: center; color: black;'>🖥️전북대 기상대 모니터링 문자로 알람받기🖥️</h1>",
                unsafe_allow_html=True)  # 제목 + 가운데 정렬

    if "phone_number" not in st.session_state:
        st.session_state.message_number = ""

    # 이메일 입력 받기
    message_number = st.text_input("번호를 입력하세요:", st.session_state.message_number)

    if message_number:
        st.session_state.email = message_number
    else:
        print('값이 전달되지 않음.')

    print(st.session_state.message_number)

    if not os.path.exists(os.path.join(FILE_PATH, 'message_number.csv')):
        df_number = pd.DataFrame(columns=['date', 'time', 'number', 'status'])

    else:
        df_number = pd.read_csv(os.path.join(FILE_PATH, 'message_number.csv'))

    if len(df_number[df_number['number'] == message_number]) != 0:
        matching_rows = df_number[df_number['number'] == message_number]
        st.write(f'등록 여부  : {matching_rows["status"].values[0]}')
        st.write(f"최초 등록 날짜 : {matching_rows['date'].values[0]} {matching_rows['time'].values[0]}")
    else:
        if message_number != '':
            number_dic = {
                'date': datetime.now().date(),
                'time': datetime.now().time().strftime("%H:%M:%S"),
                'number': message_number,
                'status': '제출됨'
            }

            st.write('처음 등록하는 휴대번호입니다.')
            df = pd.DataFrame([number_dic])
            df_number = pd.concat([df, df_number])

    df_number.to_csv(os.path.join(FILE_PATH, 'message_number.csv'), index=False)
    #
    st.write('---')
    st.markdown(""" <h3>진행 상태 안내</h3>
    <strong>휴대번호 처음 등록 시</strong><br>
    '처음 등록하는 번호입니다' 문구 출력<br>
    <br>
    <strong>휴대번호 재등록 시</strong><br>
    현재 입력된 휴대번호의 등록 여부를 표시<br>
    """, unsafe_allow_html=True)
    #
    #