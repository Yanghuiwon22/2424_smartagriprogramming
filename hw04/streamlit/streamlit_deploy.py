import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd

st.title('streamlit example')

# st.header('this is header')
# st.subheader('this is subheader')
# st.checkbox('this is checkbox1')
col1,col2 = st.columns([2,3])
col1.title(' i am column1  title !! ')
col2.title(' i am column2  title !! ')
col2.checkbox('this is checkbox2 in col2 ')

tab1, tab2= st.tabs(['Tab A' , 'Tab B'])
tab1. write('Hello')
tab2. write('i want to go home')

# app-indicator
with st.sidebar:
    choice = option_menu("app menu", ["페이지1", "project", "페이지3"],
                         icons=['house', 'kanban', 'envelope'],
                         menu_icon="folder", default_index=0,
                         styles={
                             "container": {"padding": "4!important", "background-color": "#fafafa"},
                             "icon": {"color": "black", "font-size": "25px"},
                             "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                          "--hover-color": "#fafafa"},
                             "nav-link-selected": {"background-color": "#08c7b4"},
                         }
                         )

# st.sidebar.title('this is sidebar')
# st.sidebar.checkbox('체크박스에 표시될 문구')

map_data = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [37.514575, 127.0495556],
    columns=['lat', 'lon'])

st.map(map_data)
