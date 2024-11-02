import streamlit as st


email = st.text_input('email')
if email:
    print(email)

else:
    print('none')
