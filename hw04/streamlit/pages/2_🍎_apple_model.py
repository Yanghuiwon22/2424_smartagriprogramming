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

    color_dic = {'충주': '#1f77b4', '군위': '#ff7f0e', '화성': '#2ca02c', '포천': '#9467bd'}
    y_text = {'tavg': '평균 온도', 'tmin': '최저 온도', 'tmax': '최고온도'}
    y_label = {'tavg': 'Mean temperature(°C)', 'tmin': 'Minimum temperature(°C)', 'tmax': 'Maximum temperature(°C)'}

    # 서브플롯 생성 (1행 3열)
    for y_column in ['tavg', 'tmin', 'tmax']:
        fig = make_subplots(rows=1, cols=2, subplot_titles=("2020", "2021"))

        # 지역별 평균 온도 시각화
        for station in station_dic:
            month_temp = globals()[f"{station_dic[station]}_month_temp"]

            for idx, year in enumerate([2020, 2021]):
                fig.add_trace(go.Bar(
                    x=month_temp[month_temp['year'] == year]["month"],
                    y=month_temp[month_temp['year'] == year][y_column],
                    name=f'{station}',
                    hovertemplate=f'{y_text[y_column]}<br>%{{y}}<extra></extra>',
                    marker = dict(color=color_dic[station]),
                    showlegend=(idx == 0)
                ), row=1, col=idx+1)

        fig.update_layout(
            title={
                'text' : f'{y_text[y_column]} 비교',
                'x': 0.5,
                'xanchor': 'center'
            },
            yaxis_title = y_label[y_column],
            barmode='group',  # 그룹화된 막대그래프
        )

        st.plotly_chart(fig)

    fig3 = go.Figure()

    fig3.update_layout(
        title={
            'text': f"사과 모델 평가",
            'x': 0.5,
            'xanchor': 'center'
        },

        xaxis_title='Observed full bloom date',
        yaxis_title='Predicted full bloom date',

        xaxis_tickformat='%m-%d',
        yaxis_tickformat='%m-%d',

        xaxis=dict(
            tickmode='linear',  # 일정한 간격 설정
            dtick=86400000 * 3,
            type='date',
            range=['1900-03-28', '1900-05-06'],  # 날짜 범위는 연도를 포함한 형식으로 설정
            tickformat='%m-%d'  # 월-일 형식으로 표시
        ),

        # 그래프 크기 설정
        width=800,  # 그래프 너비
        height=800,  # 그래프 높이

        yaxis = dict(
            tickmode='linear',  # 일정한 간격 설정
            dtick=86400000 * 3,
            type='date',
            range=['1900-03-28', '1900-05-06'],  # 날짜 범위는 연도를 포함한 형식으로 설정
            tickformat='%m-%d'  # 월-일 형식으로 표시
        )
    )

    fig3.add_trace(go.Scatter(
        x=['1900-03-28', '1900-05-15'],  # x값 범위
        y=['1900-03-28', '1900-05-15'],  # y=x 이므로 동일한 범위 사용
        mode='lines',
        name='x=y Line',
        line=dict(color='gray'),

    ))

    for key, value in enumerate(station_dic):
        model_result = pd.read_csv(f'./hw04/apple_model/output/{station_dic[value]}/{station_dic[value]}_result.csv')
        model_result_2020_2021 = model_result[(model_result['year'] == 2021)]

        # 첫 번째 선 (예: DVR1)
        fig3.add_trace(go.Scatter(
            x=model_result_2020_2021["obj"],
            y=model_result_2020_2021["dvr1"],
            mode='markers',
            name='DVR1',
            hovertemplate='DVR1<br>%{x} - %{y}<extra></extra>',
            line=dict(color='green'),
            showlegend=(key == 0)  # 첫 번째 선만 범례에 표시

        ))

        # 두 번째 선 (예: DVR2)
        fig3.add_trace(go.Scatter(
            x=model_result_2020_2021["obj"],
            y=model_result_2020_2021["dvr2"],
            mode='markers',
            name='DVR2',
            hovertemplate='DVR2<br>%{x} - %{y}<extra></extra>',
            line=dict(color='brown'),
            showlegend=(key == 0)  # 첫 번째 선만 범례에 표시
        ))

        fig3.add_trace(go.Scatter(
            x=model_result_2020_2021["obj"],
            y=model_result_2020_2021["cd"],
            mode='markers',
            name='CD',
            hovertemplate='CD<br>%{x} - %{y}<extra></extra>',
            line=dict(color='#ff7f0e'),
            showlegend=(key == 0)  # 첫 번째 선만 범례에 표시
        ))
    st.plotly_chart(fig3)

# ==========================================================================================================================================

    # 지역별 모델 결과 출력
    station_select = st.selectbox('지역을 선택하세요', options=['충주','군위','화성','포천'])
    station = station_dic[station_select]

    model_result = pd.read_csv(f'./hw04/apple_model/output/{station}/{station}_result.csv')



    # fig2 = go.Figure()
    # fig2.update_layout(
    #     title={
    #         'text': f"{station_select} 지역 후지 사과 개화일",
    #         'x': 0.5,
    #         'xanchor': 'center'
    #     },
    #     xaxis_title='Year',
    #     yaxis_title='Full Bloom Date',
    #     yaxis_tickformat='%m-%d',
    #     xaxis=dict(
    #         tickmode='linear',  # 일정한 간격 설정
    #         dtick=1  # 1년 단위로 간격 설정
    #     )
    # )
    #
    # fig2.add_trace(go.Scatter(
    #     x=model_result["year"],
    #     y=model_result["dvr1"],
    #     mode='lines',
    #     name='DVR1',
    #     hovertemplate='DVR1<br>%{x}-%{y}<extra></extra>'
    # ))
    # fig2.add_trace(go.Scatter(
    #     x=model_result["year"],
    #     y=model_result["dvr2"],
    #     mode='lines',
    #     name='DVR2',
    #     hovertemplate='DVR2<br>%{x}-%{y}<extra></extra>'
    # ))
    # fig2.add_trace(go.Scatter(
    #     x=model_result["year"],
    #     y=model_result["cd"],
    #     mode='lines',
    #     name='CD',
    #     hovertemplate='CD<br>%{x}-%{y}<extra></extra>'
    # ))
    # fig2.add_trace(go.Scatter(
    #     x=model_result["year"],
    #     y=model_result["obj"],
    #     mode='lines',
    #     name='obj',
    #     hovertemplate='obj<br>%{x}-%{y}<extra></extra>'
    # ))
    #
    # # Streamlit에서 개화일 그래프 출력
    # st.plotly_chart(fig2)

    # =========== 모델 결과 그래프 =============

#
#
# elif choice == "DVR 모델":
#     st.write("🍎 DVR 모델을 선택하셨습니다.")
#     st.write("DVR 모델은 사과 개화 예측에 사용되는 모델입니다.")
#     # 모델 관련 세부 정보 추가 가능
#
# elif choice == "mDVR 모델":
#     st.write("🍎 mDVR 모델을 선택하셨습니다.")
#     st.write("mDVR 모델은 사과 개화 예측에 사용되는 확장된 모델입니다.")
#     # 모델 관련 세부 정보 추가 가능
#
# elif choice == "CD 모델":
#     st.write("🍎 CD 모델을 선택하셨습니다.")
#     st.write("CD 모델은 다른 특성을 활용한 개화 예측 모델입니다.")
