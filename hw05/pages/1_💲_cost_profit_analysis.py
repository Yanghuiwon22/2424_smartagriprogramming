import matplotlib
import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib.dates as mdates
from datetime import datetime
import seaborn as sns

st.title("💲농작물 비용 및 수익 분석 계산기")


# 연도와 월
st.header("기간 입력")
selected_year = st.selectbox("연도 선택", range(2020, 2031))  # 2020년부터 2030년까지 선택 가능
selected_month = st.selectbox("월 선택", range(1, 13))  # 1월부터 12월까지 선택 가능

st.write(f"선택된 기간: {selected_year}년 {selected_month}월")

# 입력
st.header("비용 입력")
seed_cost = st.text_input("종자 비용 (₩)", "", placeholder=" 종자 비용을 입력해 주세요")
fertilizer_cost = st.text_input("비료 비용 (₩)", "", placeholder=" 비료 비용을 입력해 주세요")
pesticide_cost = st.text_input("농약 비용 (₩)", "", placeholder=" 농약 비용을 입력해 주세요")
labor_cost = st.text_input("인건비 (₩)", "", placeholder=" 인건비를 입력해 주세요")
other_cost = st.text_input("기타 비용 (₩)", "", placeholder=" 기타 비용을 입력해 주세요")

# 입력값 확인
try:
    seed_cost = int(seed_cost) if seed_cost else 0
    fertilizer_cost = int(fertilizer_cost) if fertilizer_cost else 0
    pesticide_cost = int(pesticide_cost) if pesticide_cost else 0
    labor_cost = int(labor_cost) if labor_cost else 0
    other_cost = int(other_cost) if other_cost else 0
except ValueError:
    st.error("모든 비용 입력값은 숫자여야 합니다.")
    seed_cost = fertilizer_cost = pesticide_cost = labor_cost = other_cost = 0

total_cost = seed_cost + fertilizer_cost + pesticide_cost + labor_cost + other_cost
st.write(f"총 비용: ₩{total_cost}")

# 입력
st.header("수익 입력")
selling_price_per_kg = st.text_input("판매 가격 (₩/kg)", "", placeholder=" 판매 가격을 입력해 주세요")
production_quantity = st.text_input("생산량 (kg)", "", placeholder=" 생산량을 입력해 주세요")

# 입력값 확인
try:
    selling_price_per_kg = int(selling_price_per_kg) if selling_price_per_kg else 0
    production_quantity = int(production_quantity) if production_quantity else 0
except ValueError:
    st.error("판매 가격과 생산량은 숫자여야 합니다.")
    selling_price_per_kg = production_quantity = 0

total_revenue = selling_price_per_kg * production_quantity
profit = total_revenue - total_cost

st.write(f"{selected_year}년 {selected_month}월의 총 수익: ₩{total_revenue}")
st.write(f"{selected_year}년 {selected_month}월의 순이익: ₩{profit}")

# 버튼
col1, col2 = st.columns(2)

# 왼쪽에 Bar 차트
with col1:
    if st.button('비용 vs 수익 bar 차트 보기'):
        if total_revenue > 0:
            st.subheader(f"{selected_year}년 {selected_month}월 비용 vs 수익 ")
            fig, ax = plt.subplots()
            ax.bar(["비용", "수익"], [total_cost, total_revenue], color=['red', 'green'])
            ax.set_title("비용 vs 수익")
            ax.set_ylabel("금액 (₩)")
            st.pyplot(fig)
        else:
            st.write(" bar 차트를 보려면 수익을 입력하세요.")

# 오른쪽에 Pie 차트
with col2:
    if st.button('비용 비율 pie 차트 보기'):
        if seed_cost > 0 or fertilizer_cost > 0 or pesticide_cost > 0 or labor_cost > 0 or other_cost > 0:
            st.subheader(f"{selected_year}년 {selected_month}월 비용 비율 (Pie 차트)")
            labels = ['종자 비용', '비료 비용', '농약 비용', '인건비', '기타 비용']
            values = [seed_cost, fertilizer_cost, pesticide_cost, labor_cost, other_cost]

            # pie 그래프
            fig = px.pie(values=values, names=labels, title="비용 비율")
            st.plotly_chart(fig)
        else:
            st.write(" pie 차트를 보려면 비용을 입력하세요.")