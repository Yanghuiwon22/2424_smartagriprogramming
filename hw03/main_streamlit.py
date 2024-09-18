import streamlit as st
import requests
from bs4 import BeautifulSoup

# fastapi데이터 받아오기
response = requests.get("http://127.0.0.1:8000")
data = response.json()

# streamlit으로 표현하기
st.title('지역기반 기상 데이터 제공 서비스')
address = st.text_input('주소를 입력하세요 : ')

# 버튼을 누르면 FastAPI에 값을 보냄
if address:
    response = requests.get("http://127.0.0.1:8000/address/", params={'address_input': address})
    result = response.json()

    # FastAPI로부터 처리된 결과를 출력
    st.write(f"**FastAPI에서 처리된 값**: {result['address_text']}")

st.markdown('---')
st.markdown(
    """
    <h3 style="text-align: center;">실시간 데이터</h3>""",
    unsafe_allow_html=True
)

# 1. 실시간 온도, 습도, 풍속
col1, col2, col3 = st.columns(3)

# 네이버 날씨 크롤링



# markdown style
style_box = ('width: 100%; height: 100%; background-color: rgb(128, 128, 128); color: white; border-radius: 20px; '
             'text-align: center; align-items: center; justify-content: center;')
style_boxheader = 'padding-top: 10px; margin-bottom: 0px; font-size:20px;'
style_boxcontent = 'font-size: 40px; margin: 0px;'


# 첫 번째 열에 사각형 추가
with col1:
    st.markdown(
        f"""
        <div style="{style_box}">
            <p style="{style_boxheader}">온도(°C)</p>
            <p style="{style_boxcontent}">99.9</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# 두 번째 열에 다른 내용 추가

with col2:
    st.markdown(
        f"""
        <div style="{style_box}">
            <p style="{style_boxheader}">습도(%)</p>
            <p style="{style_boxcontent}">99.9</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        f"""
        <div style="{style_box}">
            <p style="{style_boxheader}">풍속(m/s)</p>
            <p style="{style_boxcontent}">99.9</p>
        </div>
        """,
        unsafe_allow_html=True
    )
