import pandas as pd
import vonage
from dotenv import load_dotenv
import os
from settings import *

load_dotenv()  # .env 파일 로드
api_key = os.getenv("VONAGE_API_KEY")
secret_key = os.getenv("VONAGE_SECRET")

def send_sms(message, url):
    client = vonage.Client(key=api_key, secret=secret_key)

    message_df = pd.read_csv(os.path.join(FILE_PATH, 'message_number.csv'))
    full_message = f"{message}\n{url}"
    print(message_df['number'])

    for index, row in message_df.iterrows():
        if row['조건'] == 'default':
            print(f"+820{row['number']}")
            print(f"text : {message}")

# 무료 크레딧 소모로 주석처리해놓음
    #     response = client.sms.send_message({
    #         'from': 'VonageSMS',
    #         'to': f'+82{user['number']}',
    #         'text': full_message,
    #         'type': 'unicode'  # UCS-2 인코딩을 사용
    #     })
    #
    # if response['messages'][0]['status'] == '0':
    #     print('메시지 전송 성공!')
    # else:
    #     print(f"메시지 전송 실패: {response['messages'][0]['error-text']}")


if __name__ == '__main__':
    message_content = "전북대학교 기상대 모니터링 서비스입니다"
    url_to_send = "https://yanghuiwon22-hw08.streamlit.app/"  # 보내고자 하는 URL

    send_sms(message_content, url_to_send)  # 수신자 번호, 메시지 내용, URL 입력

