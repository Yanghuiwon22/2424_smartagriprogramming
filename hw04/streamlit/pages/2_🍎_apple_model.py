import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
from PIL import Image
import glob

st.title('🍎 후지 사과 개화예측 모델')

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