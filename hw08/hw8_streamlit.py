import streamlit as st
import time
from datetime import datetime, timedelta
from func import jbnu_aws_data


st.title('전북대 기상대를 활용한 모니터링 시스템')

# Display the current time
current_time = datetime.now().strftime("%H:%M:%S")
st.write(f"Current Time: {current_time}")


# Add a hint about the rerun
# st.write("This app will rerun in 5 seconds...")

data = jbnu_aws_data()  # 데이터를 가져오고 변환

# 데이터가 존재하는지 확인
if not data.empty:  # 데이터프레임이 비어 있지 않다면
    # 가장 최근 데이터
    latest_data = data.iloc[0]  # 첫 번째 행을 선택

    updated_time = latest_data['Date']
    st.write(f'Updated Time: {updated_time}')

    st.write(f"Temperature: {latest_data['온도']}°C")
    st.write(f"Humidity: {latest_data['습도']}%")
    st.write(f"Lux: {latest_data['일사량']}")
    st.write(f"Wind direction: {latest_data['풍향']}")
    st.write(f"Wind speed: {latest_data['풍속']} m/s")
    st.write(f"Rain: {latest_data['강우']} mm")
    st.write(f"Battery: {latest_data['베터리 전압']}")
else:
    st.write("No data available.")

time.sleep(5)
st.rerun()