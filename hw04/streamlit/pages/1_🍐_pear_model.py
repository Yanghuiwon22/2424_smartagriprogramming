import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
from PIL import Image
import glob
import sys, os
import pathlib

#
# # # hw04/pair_20years.py
# # # 상위 폴더 경로를 추가
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
# # 절대 경로 추가
# # sys.path.append('/absolute/path/to/project/utils')
# # cur_dir = os.getcwd()
# # print(os.path.dirname(os.path.abspath(os.path.dirname(cur_dir))))
# from hw04.pair_20years import get_dvr_graph  # 상위 폴더의 파일을 import




st.title('🍐 신고 배 개화예측 모델')
st.header('개화예측 모델 비교')


def load_images():
    folder_path = ['Cheonan','Icheon','Sangju','Yeongcheon','naju', 'wanju', 'ulju', 'sacheon']
    image_lists = []

    for folder in folder_path:
        try:
            # 폴더에서 이미지를 불러옵니다.
            img = Image.open(f'hw04/output/{folder}/dvs_{folder}_graph.png')
            image_lists.append(img)  # 이미지 리스트에 저장
        except FileNotFoundError:
            st.error(f"{folder} 폴더에서 이미지를 찾을 수 없습니다.")

    return image_lists

def show_images():
    # 이미지 불러오기
    images = load_images()

    # Streamlit 화면에 이미지를 하나씩 띄우기
    for img, folder in zip(images, ['Cheonan', 'Icheon', 'Sangju', 'Yeongcheon', 'Naju', 'Wanju', 'Ulju', 'Sacheon']):
        st.write(f"{folder} 개화모델 비교 ")
        st.image(img)

def draw_graph():
    output_path = '../../output'
    output_list = os.listdir(output_path)
    print(output_list)

    # output_list = ['naju'] # 테스트를 위한 데이터 정리
    for station in output_list:
        print(station)
        # hw04 / output / Cheonan / flowering_date_Cheonan.csv
        obj_date = pd.read_csv(f'output/{station}/flowering_date_{station}.csv')
        obj_date = obj_date[['station', 'year', 'Date']]
        obj_date = obj_date.sort_values(by='year', ascending=True, ignore_index=True)
        obj_date = obj_date.rename(columns={'Date': 'obj_date'})
        obj_date['station'] = station

        dvs_date = pd.read_csv(f'output/{station}/DVS_{station}_model.csv')
        dvs_date['year'] = dvs_date['Date'].str.split('-').str[0].astype(int)
        dvs_date = dvs_date[['Station', 'year', 'Date']]
        dvs_date = dvs_date.rename(columns={'Date': 'dvs_date', 'Station': 'station'})
    print(obj_date)
    print(dvs_date)







def sidebar():
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


def main():

    # sidebar()
    # load_images()
    # show_images()
    draw_graph()
#     page()

if __name__ == '__main__' :
    main()


