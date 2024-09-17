import streamlit as st
import requests

# fastapi데이터 받아오기
response = requests.get("http://127.0.0.1:8000/")
data = response.json()

# streamlit으로 표현하기
st.title('지역기반 기상 데이터 제공 서비스')
address = st.text_input('주소를 입력하세요 : ')

# 버튼을 누르면 FastAPI에 값을 보냄
if address:
    response = requests.get("http://127.0.0.1:8000/address/", params={'address_input':address})
    result = response.json()

    # FastAPI로부터 처리된 결과를 출력
    st.write(f"**FastAPI에서 처리된 값**: {result['address_text']}")