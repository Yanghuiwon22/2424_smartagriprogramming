import streamlit as st
from streamlit_option_menu import option_menu
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import numpy as np
import pandas as pd
from PIL import Image
import glob

st.title('🍎 후지 사과 개화 예측 모델')

with st.sidebar:




    choice = option_menu("모델 선택", ["전체 모델 비교", "DVR 모델", "mDVR 모델", "CD 모델"],
                         icons=['bar-chart-line-fill', 'house', 'kanban', 'envelope'],
                         menu_icon="folder", default_index=0,
                         styles={
                             "container": {"padding": "4!important", "background-color": "#fafafa"},
                             "icon": {"color": "black", "font-size": "25px"},
                             "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                          "--hover-color": "#fafafa"},
                             "nav-link-selected": {"background-color": "#08c7b4"},
                         }
                         )

if choice == "전체 모델 비교":
    station_dic = {'충주': 'Chungju', '군위': 'Gunwi', '화성': 'Hwaseong', '포천': 'Pocheon'}


    # 3,4월 tmin, tavg, tmax 막대그래프 그리기
    Chungju_month_temp = pd.read_csv(f'./hw04/apple_model/output/Chungju/Chungju_tmin_tavg_tmax_month.csv')
    Gunwi_month_temp = pd.read_csv(f'./hw04/apple_model/output/Gunwi/Gunwi_tmin_tavg_tmax_month.csv')
    Hwaseong_month_temp = pd.read_csv(f'./hw04/apple_model/output/Hwaseong/Hwaseong_tmin_tavg_tmax_month.csv')
    Pocheon_month_temp = pd.read_csv(f'./hw04/apple_model/output/Pocheon/Pocheon_tmin_tavg_tmax_month.csv')

    # 서브플롯 생성 (1행 3열)
    fig = make_subplots(rows=1, cols=3, subplot_titles=("최고 온도", "평균 온도", "최저 온도"))

    # 지역별 최고 온도 시각화
    for station in station_dic:
        month_temp = globals()[f"{station_dic[station]}_month_temp"]

        fig.add_trace(go.Bar(
            x=month_temp["month"],
            y=month_temp["tmax"],
            name=f'{station}',
            hovertemplate='최고 온도<br>%{y}<extra></extra>'
        ), row=1, col=1)

    # 지역별 평균 온도 시각화
    for station in station_dic:
        month_temp = globals()[f"{station_dic[station]}_month_temp"]

        fig.add_trace(go.Bar(
            x=month_temp["month"],
            y=month_temp["tavg"],
            name=f'{station}',
            hovertemplate='평균온도<br>%{y}<extra></extra>'
        ), row=1, col=2)

    # 지역별 최저 온도 시각화
    for station in station_dic:
        month_temp = globals()[f"{station_dic[station]}_month_temp"]

        fig.add_trace(go.Bar(
            x=month_temp["month"],
            y=month_temp["tmin"],
            name=f'{station}',
            hovertemplate='최저 온도<br>%{y}<extra></extra>'
        ), row=1, col=3)

    # 레이아웃 업데이트
    fig.update_layout(
        title={
            'text': "지역별 온도 비교",
            'x': 0.5,
            'xanchor': 'center'
        },
        yaxis_title='Temperature (°C)',
        barmode='group',  # 그룹화된 막대그래프
    )

    # Streamlit에서 그래프 출력
    st.plotly_chart(fig)

# ==========================================================================================================================================

    # 지역별 모델 결과 출력
    station_select = st.selectbox('지역을 선택하세요', options=['충주','군위','화성','포천'])
    station = station_dic[station_select]

    model_result = pd.read_csv(f'./hw04/apple_model/output/{station}/{station}_result.csv')
    fig2 = go.Figure()
    fig2.update_layout(
        title={
            'text': f"{station_select} 지역 후지 사과 개화일",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Year',
        yaxis_title='Full Bloom Date',
        yaxis_tickformat='%m-%d',
        xaxis=dict(
            tickmode='linear',  # 일정한 간격 설정
            dtick=1  # 1년 단위로 간격 설정
        )
    )

    fig2.add_trace(go.Scatter(
        x=model_result["year"],
        y=model_result["dvr1"],
        mode='lines',
        name='DVR1',
        hovertemplate='DVR1<br>%{x}-%{y}<extra></extra>'
    ))
    fig2.add_trace(go.Scatter(
        x=model_result["year"],
        y=model_result["dvr2"],
        mode='lines',
        name='DVR2',
        hovertemplate='DVR2<br>%{x}-%{y}<extra></extra>'
    ))
    fig2.add_trace(go.Scatter(
        x=model_result["year"],
        y=model_result["cd"],
        mode='lines',
        name='CD',
        hovertemplate='CD<br>%{x}-%{y}<extra></extra>'
    ))
    fig2.add_trace(go.Scatter(
        x=model_result["year"],
        y=model_result["obj"],
        mode='lines',
        name='obj',
        hovertemplate='obj<br>%{x}-%{y}<extra></extra>'
    ))

    # Streamlit에서 개화일 그래프 출력
    st.plotly_chart(fig2)






elif choice == "DVR 모델":
    st.write("🍎 DVR 모델을 선택하셨습니다.")
    st.write("DVR 모델은 사과 개화 예측에 사용되는 모델입니다.")
    # 모델 관련 세부 정보 추가 가능

elif choice == "mDVR 모델":
    st.write("🍎 mDVR 모델을 선택하셨습니다.")
    st.write("mDVR 모델은 사과 개화 예측에 사용되는 확장된 모델입니다.")
    # 모델 관련 세부 정보 추가 가능

elif choice == "CD 모델":
    st.write("🍎 CD 모델을 선택하셨습니다.")
    st.write("CD 모델은 다른 특성을 활용한 개화 예측 모델입니다.")
