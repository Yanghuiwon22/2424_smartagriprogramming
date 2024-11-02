import pandas as pd
import vonage
from dotenv import load_dotenv
import os
from settings import *

load_dotenv()  # .env 파일 로드
api_key = os.getenv("VONAGE_API_KEY")
secret_key = os.getenv("VONAGE_SECRET")

def send_sms(message):
    client = vonage.Client(key=api_key, secret=secret_key)

    message_df = pd.read_csv(os.path.join(FILE_PATH, 'message_number.csv'))

    for index, row in message_df.iterrows():
        if row['조건'] == 'default':
            print(f"+820{row['number']}")
            print(f"text : {message}")


        # response = client.sms.send_message({
        #     'from': 'VonageSMS',
        #     'to': f'+82{user['number']}',
        #     'text': '안녕하세요! Vonage에서 보낸 메시지입니다.',
        #     'type': 'unicode'  # UCS-2 인코딩을 사용
        # })
    #
    # if response['messages'][0]['status'] == '0':
    #     print('메시지 전송 성공!')
    # else:
    #     print(f"메시지 전송 실패: {response['messages'][0]['error-text']}")

if __name__ == '__main__':
    send_sms()