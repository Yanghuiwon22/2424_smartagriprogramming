import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

st.title('🏠 HOME')
st.header('어서오세요. 옆에서 페이지를 눌러주세요')

if st.button("Click me"):
    st.write("어서오세요🤗")
    st.balloons()

# app-indicator
def sidebar():
    with st.sidebar:
        choice = option_menu("연습", ["Home", "Task", "about"],
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
        return choice


# def main():
    # sidebar()
#
# if __name__ == '__main__' :
#     main()
