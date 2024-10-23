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

# jbnu aws 기상대 데이터 실시간 로드
jbnu_aws_data = jbnu_aws_data()
updated_time = datetime.strptime(jbnu_aws_data[1]['created_at'].split('T')[1].split('Z')[0], '%H:%M:%S')+timedelta(hours=9)
st.write(f'updated_time : {updated_time.strftime("%H:%M:%S")}')
st.write(f"Temperature: {jbnu_aws_data[1]['field1']}°C")
st.write(f"Humidity: {jbnu_aws_data[2]['field2']}%")
st.write(f"Lux: {jbnu_aws_data[3]['field3']}")
st.write(f"Wind direction: {jbnu_aws_data[4]['field4']}")
st.write(f"Wind speed: {jbnu_aws_data[5]['field5']}m/s")
st.write(f"Rain: {jbnu_aws_data[6]['field6']}mm")
st.write(f"battery: {jbnu_aws_data[7]['field7']}")

# Sleep for 60 seconds before rerunning
time.sleep(5)
st.rerun()