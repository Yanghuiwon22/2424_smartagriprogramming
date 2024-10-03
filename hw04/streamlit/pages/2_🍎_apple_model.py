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
    choice = option_menu("모델 선택", ["전체 모델 비교","DVR 모델", "mDVR 모델", "CD 모델"],
                         icons=['bar-chart-line-fill','house', 'kanban', 'envelope'],
                         menu_icon="folder", default_index=0,
                         styles={
                             "container": {"padding": "4!important", "background-color": "#fafafa"},
                             "icon": {"color": "black", "font-size": "25px"},
                             "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                          "--hover-color": "#fafafa"},
                             "nav-link-selected": {"background-color": "#08c7b4"},
                         }
                         )
    st.write(choice)
if choice == "전체 모델 비교":
    st.write("🍎 후지 사과 개화 예측 모델을 비교합니다.")

    df = pd.read_csv('./hw04/streamlit/pages/Chungju_result.csv')

    fig = go.Figure()
    fig.update_layout(
        title={
            'text': "후지 사과 개화 예측 모델 ",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='year',
        yaxis_title='full bloom date',
        yaxis_tickformat='%m-%d'

    )

    fig.add_trace(go.Scatter(x=df["year"], y=df["dvr1"], mode='lines', name='DVR1'))
    fig.add_trace(go.Scatter(x=df["year"], y=df["dvr2"], mode='lines', name='DVR2'))
    fig.add_trace(go.Scatter(x=df["year"], y=df["cd"], mode='lines', name='CD'))
    fig.add_trace(go.Scatter(x=df["year"], y=df["obj"], mode='lines', name='obj'))

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