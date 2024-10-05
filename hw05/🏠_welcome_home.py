import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import seaborn as sns

st.set_page_config(layout="wide")

st.title('🏠홈 ')

# 파일 읽어오기

crop_money = pd.read_csv('hw05/crop_money.csv',encoding='EUC-KR')


crop_money.columns = crop_money.columns.str.replace(r'\(.*?\)', '', regex=True)
crop_money.columns = crop_money.columns.str.strip()
crop_money['연도'] = crop_money['연도'].str.replace('년', '')
crop_money['연도'] = pd.to_datetime(crop_money['연도']).dt.year
crop_money['연도'] = crop_money['연도'].astype(str)

st.write(crop_money)
st.write(crop_money.columns)


matplotlib.rc('font', family='Malgun Gothic')
# 지급건수 그래프 그리기
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(crop_money['연도'], crop_money['지급건수'], color='skyblue')

# 그래프 레이블
ax.set_xlabel('연도')
ax.set_ylabel('지급건수')
ax.set_title('연도별 지급건수')

# 그래프를 Streamlit에 표시
st.pyplot(fig)

# st.pyplot(fig)
# st.plotly_chart(fig)



col1, col2 = st.columns(2)
def col1():
    with col1:
        st.header('2020화훼 농가 ')
        st.write(flower_2020.head(20))
def col2():
    with col2:
        st.header()
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
