import os

import pandas as pd
import requests
import json

from settings import *


def get_code():
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type" : "authorization_code",
        "client_id" : "c7f4c9c3247cf4f1765679d63d620b2f",
        "redirect_url" : "http://localhost:5000",
        "code" : "nKqTLLZt2QDZ-mkUFiLcr3xRHwLuJRci4esrgFK1GT3DbSPso4zLzAAAAAQKKcleAAABkuvpl5ke0jm_MNo9Pw",
        "client_secret" : "sNy5KFLhiDPLtk0WWIg7b35zj0MZKNcQ"
    }
    # https://kauth.kakao.com/oauth/authorize?client_id=c7f4c9c3247cf4f1765679d63d620b2f&redirect_uri=https://localhost:5000&response_type=code&scope=talk_message,friends
    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)

def main(weather_data):
    # get_code()

    print('____')
    # 카카오톡 메시지 API
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": "c7f4c9c3247cf4f1765679d63d620b2f",
        "refresh_token": "dvWLUJyAao7x_rC9VtFfAldtRbuCPjryAAAAAgoqJVIAAAGS6-nsfrbGP5Eb7W-4",
        "client_secret" : "sNy5KFLhiDPLtk0WWIg7b35zj0MZKNcQ"
    }
    response = requests.post(url, data=data)
    tokens = response.json()

    # kakao_code.json 파일 저장
    with open("kakao_code.json", "w") as fp:
        json.dump(tokens, fp)

    with open("kakao_code.json", "r") as fp:
        tokens = json.load(fp)

    url = "https://kapi.kakao.com/v1/api/talk/friends" #친구 목록 가져오기
    header = {"Authorization": 'Bearer ' + tokens["access_token"]}
    result = json.loads(requests.get(url, headers=header).text)
    friends_list = result.get("elements")
    print(f"friends_list : {friends_list}")

    df_email = pd.read_csv(os.path.join(FILE_PATH, 'kakao_email.csv'))
    print(df_email)

    for friend in friends_list:
        friend_id = friend.get("uuid")
        print(friend_id)
        df_now = df_email[df_email['uuid'] == friend_id]

        if df_now['조건'].values == 'default':
            url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
            header = {"Authorization": 'Bearer ' + tokens["access_token"]}
            data = {
                'receiver_uuids': json.dumps([friend_id]),  # JSON 배열로 변경
                "template_object": json.dumps({
                    "object_type": "text",
                    "link": {
                        "web_url": "https://developers.kakao.com",
                        "mobile_web_url": "https://developers.kakao.com"
                    },
                    "text": f"""
                    전북대학교 기상대 모니터링 서비스입니다
                    
                    {weather_data}
                    """
                })
            }
            print(weather_data)
            # response = requests.post(url, headers=header, data=data)
            #
            # if response.status_code == 200:
            #     print("메시지가 성공적으로 전송되었습니다.")
            # else:
            #     print("메시지 전송 실패:", response.json())

if __name__ == '__main__':
    main('sd')