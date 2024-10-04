import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

st.title('🏠어서오세요 홈입니다.')

# 파일 읽어오기
flower_2020 = pd.read_csv('hw05/2020_flower.csv', encoding='EUC-KR')
flower_2021 = pd.read_csv('hw05/2021_flower.csv', encoding='EUC-KR')

# flower_2020 = flower_2020['시도별', '농가수(호)', '면적(ha)','판매량(천본_분_주)','판매액(천원)']
flower_2020_selected = flower_2020[['시도별', '농가수(호)', '면적(ha)', '판매량(천본_분_주)', '판매액(천원)']]

plt.figure(figsize=(10, 6))
# sns.barplot(x='시도별', y='판매량(천본_분_주)', data=flower_2020_selected)
#
# def plot_data(year, data):
#     plt.figure(figsize=(10, 6))
#     sns.barplot(x='시도별', y='판매량(천본_분_주)', data=data)
#     plt.title(f'{year}년 시도별 판매량')
#     plt.xlabel('시도별')
#     plt.ylabel('판매량(천본/분/주)')
#     plt.xticks(rotation=45)
#     st.pyplot(plt)
#
# # 2020년 데이터 시각화
# st.subheader('2020년 시도별 판매량')
# plot_data(2020, flower_2020_selected)
# # 2021년 데이터 시각화
# st.subheader('2021년 시도별 판매량')
# plot_data(2021, flower_2021_selected)

st.pyplot(plt)
# city = flower_2020.loc[['서울특별시', '인천', '대전', '대구', '광주', '부산', '울산']]
#
# st.write(flower_2020.head(20))
# st.write(flower_2020.columns)
# st.write(flower_2020['면적(ha)'])
#
# x = flower_2020['시도별']
# y = flower_2020['면적(ha)']


# fig , ax = plt.subplots(figsize=(10, 6))
#
# plt.plot(x, y, label='dvs', color='b', marker='o')
# st.pyplot(fig)
# st.plotly_chart(fig)



col1, col2 = st.columns(2)
def col1():
    with col1:
        st.header('2020화훼 농가 ')
        st.write(flower_2020.head(20))
def col2():
    with col2:
        st.header('2021화훼 농가 ')
        st.write(flower_2021.head(20))

# st.subheader('this is subheader')
# st.checkbox('this is checkbox1')

def tab():
    tab1, tab2, tab3 = st.tabs(['뭐', '로', '하'])
    tab1. write('뭐하지')
    tab2. write('i want to go home')
    tab3.write(st.text_input('이름을 입력하세요!'))

# if st.button("Click me"): st.write("Button clicked!"),st.balloons()

def home():
    st.title('🏠어서오세요 홈입니다.')

# app-indicator
def sidebar():
    with st.sidebar:
        choice = option_menu("메인메뉴", ["Home", "Task", "Pictures"],
                             icons=['house', 'list-task', 'image'],
                             menu_icon="folder", default_index=0,
                             styles={ 'menu_title': {'icon':'envelope','color': '#9ed916'},
                                 "container": {"padding": "4!important", "background-color": "#fafafa"},
                                 "icon": {"color": "#9ed916", "font-size": "25px"},
                                 "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                              "--hover-color": "#fafafa"},
                                 "nav-link-selected": {"background-color": "#579dd1"}
                                 ,
                          }
                          )
        if choice == 'Home':
            col1()
            st.write('welcome back home')

    # map_data = pd.DataFrame(
#     np.random.randn(100, 2) / [50, 50] + [37.514575, 127.0495556],
#     columns=['lat', 'lon'])
# st.map(map_data)

def main():
    # tab()
    sidebar()
    # home()
    plot_data


if __name__ == '__main__' :
    main()
