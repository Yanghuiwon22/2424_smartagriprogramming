import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
from PIL import Image
import glob

st.title('🍐 신고 배 개화예측 모델')
st.header('개화예측 모델 비교')

# 이미지 저장
# img = Image.open('data/image.jpg')
# hw04/output/Icheon/dvs_Icheon_graph.png
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
    sidebar()
    load_images()
    show_images()
#     page()

if __name__ == '__main__' :
    main()


