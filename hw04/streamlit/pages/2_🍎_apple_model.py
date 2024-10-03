import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
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
    station_select = st.selectbox('지역을 선택하세요', options=['충주','군위','화성','포천'])
    station = station_dic[station_select]

    st.write(f"🍎 {station_select} 지역의 후지 사과 개화 예측 모델 비교")

    df = pd.read_csv(f'./hw04/apple_model/output/{station}/{station}_result.csv')

    fig = go.Figure()
    fig.update_layout(
        title={
            'text': f"{station_select} 지역 후지 사과 개화일",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='year',
        yaxis_title='full bloom date',
        yaxis_tickformat='%m-%d',
        xaxis=dict(
            tickmode='linear',  # 일정한 간격 설정
            dtick=1  # 1년 단위로 간격 설정
        )

    )

    fig.add_trace(go.Scatter(
        x=df["year"],
        y=df["dvr1"],
        mode='lines',
        name='DVR1',
        hovertemplate='DVR1<br>%{x}-%{y}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=df["year"],
        y=df["dvr2"],
        mode='lines',
        name='DVR2',
        hovertemplate='DVR2<br>%{x}-%{y}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=df["year"],
        y=df["cd"],
        mode='lines',
        name='CD',
        hovertemplate='CD<br>%{x}-%{y}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=df["year"],
        y=df["obj"],
        mode='lines',
        name='obj',
        hovertemplate='obj<br>%{x}-%{y}<extra></extra>'
    ))

    st.plotly_chart(fig)

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
