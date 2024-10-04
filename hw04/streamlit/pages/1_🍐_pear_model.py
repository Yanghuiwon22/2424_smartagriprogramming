import streamlit as st
from streamlit_option_menu import option_menu
import sys, os
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

import csv
import requests
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import glob
import pathlib
import matplotlib.dates as mdates
import math


# 아이콘 사이트
# https://icons.getbootstrap.com/?q=chart
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
    output_path = 'C:/code/2424_smartagriprogramming/hw04/output'
    output_list = os.listdir(output_path)
    # print(output_list)
    # st.write(f"Current working directory: {os.getcwd()}")

    # C:\code\2424_smartagriprogramming 현재 directory
# 파일 절대 경로
    # C:\code\2424_smartagriprogramming\hw04\output\Cheonan\DVS_Cheonan_model.csv

    # output_list = ['Cheonan'] # 테스트를 위한 데이터 정리
    for station in output_list:
        print(station)
        # hw04 / output / Cheonan / flowering_date_Cheonan.csv
        # df = pd.read_csv('./hw04/streamlit/pages/Chungju_result.csv')
        # 파일의 절대경로 읽어옴 -> 상대경로로 어려움,,, 모르겠음,,,
        # ovj 데이터 읽어오기
        obj_date = pd.read_csv(f'C:/code/2424_smartagriprogramming/hw04/output/{station}/flowering_date_{station}.csv')
        obj_date = obj_date[['station', 'year', 'Date']]
        obj_date = obj_date.sort_values(by='year', ascending=True, ignore_index=True)
        obj_date = obj_date.rename(columns={'Date': 'obj_date'})
        obj_date['station'] = station
        # dvs 데이터 읽어오기
        # dvs_date = pd.read_csv(f'output/{station}/DVS_{station}_model.csv')
        dvs_date = pd.read_csv(f'C:/code/2424_smartagriprogramming/hw04/output/{station}/DVS_{station}_model.csv')
        dvs_date['year'] = dvs_date['Date'].str.split('-').str[0].astype(int)
        dvs_date = dvs_date[['Station', 'year', 'Date']]
        dvs_date = dvs_date.rename(columns={'Date': 'dvs_date', 'Station': 'station'})

        # mdvr 데이터 읽어오기
        mdvr_date = pd.read_csv(f'C:/code/2424_smartagriprogramming/hw04/output/{station}/mDVR/{station}_mDVR_date.csv')
        # mdvr_date = pd.read_csv(f'output/{station}/mDVR/{station}_mDVR_date.csv')
        mdvr_date = mdvr_date.rename(columns={'Date': 'mdvr_date'})

        # cd데이터 읽어오기
        cd_date = pd.read_csv(f'C:/code/2424_smartagriprogramming/hw04/output/{station}/cd_{station}_date.csv')
        # cd_date = pd.read_csv(f'output/{station}/cd_{station}_date.csv')
        cd_date = cd_date.rename(columns={'예상 만개일': 'cd_date'})

        # 데이터 정리
        obj_date['station'] = obj_date['station'].str.strip()
        dvs_date['station'] = dvs_date['station'].str.strip()
        df = pd.merge(obj_date, dvs_date, on=['station','year'], how='outer')
        df = pd.merge(df, mdvr_date, on=['station','year'], how='outer')
        df = pd.merge(df, cd_date, on=['year','station'], how='outer')

        df = df.sort_values(by='year', ignore_index=True)

        df['obj_date'] = df['obj_date'].apply(lambda x: x.split('-')[1] + '-' + x.split('-')[2] if pd.notna(x) else x)
        df['dvs_date'] = df['dvs_date'].apply(lambda x: x.split('-')[1] + '-' + x.split('-')[2] if pd.notna(x) else x)
        df['mdvr_date'] = df['mdvr_date'].apply(lambda x: x.split('-')[1] + '-' + x.split('-')[2] if pd.notna(x) else x)
        df['cd_date'] = df['cd_date'].apply(lambda x: x.split('-')[1] + '-' + x.split('-')[2] if pd.notna(x) else x)

        df['obj_date'] = pd.to_datetime(df['obj_date'], format='%m-%d')
        df['dvs_date'] = pd.to_datetime(df['dvs_date'], format='%m-%d')
        df['mdvr_date'] = pd.to_datetime(df['mdvr_date'], format='%m-%d')
        df['cd_date'] = pd.to_datetime(df['cd_date'], format='%m-%d')

        fig, ax = plt.subplots(figsize=(10, 6))


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
    if choice == "전체 모델 비교":
        station_dic = {'천안': 'Cheonan', '이천': 'Icheon', '나주': 'naju', '사천': 'sacheon','상주':'Sangju',
                       '울주':'ulju', '완주':'wanju', '영천':'Yeongcheon'}
        station_select = st.selectbox('지역을 선택하세요', options=['천안', '이천', '나주', '사천',
                                                            '상주','울주','완주','영천'])
        station = station_dic[station_select]

        st.write(f"🍐 {station_select} 지역의 신고 배 개화 예측 모델 비교")

    elif choice == "DVR 모델":
        st.write("🍐 DVR 모델을 선택하셨습니다.")
        st.write("DVR 모델은 배 개화 예측에 사용되는 모델입니다.")
        # 모델 관련 세부 정보 추가 가능

    elif choice == "mDVR 모델":
        st.write("🍐 mDVR 모델을 선택하셨습니다.")
        st.write("mDVR 모델은 배 개화 예측에 사용되는 확장된 모델입니다.")
        # 모델 관련 세부 정보 추가 가능

    elif choice == "CD 모델":
        st.write("🍐 CD 모델을 선택하셨습니다.")
        st.write("CD 모델은 다른 특성을 활용한 개화 예측 모델입니다.")





def main():

    sidebar()
    # load_images()
    # show_images()
    draw_graph()
#     page()

if __name__ == '__main__' :
    main()


