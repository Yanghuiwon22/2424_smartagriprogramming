import requests
import json
#

# url = "https://kauth.kakao.com/oauth/token"
# data = {
#     "grant_type" : "authorization_code",
#     "client_id" : "c7f4c9c3247cf4f1765679d63d620b2f",
#     "redirect_url" : "http://localhost:5000",
#     "code" : "5YntWi2-9nqnX9eBXUlzfXV53nKmS8AvBGYgmr2nWVupeyEWyYGKuAAAAAQKPXPrAAABkuDHZ_F-jFVpBnvzXw",
#     "client_secret" : "sNy5KFLhiDPLtk0WWIg7b35zj0MZKNcQ"
# }
# # https://kauth.kakao.com/oauth/authorize?client_id=c7f4c9c3247cf4f1765679d63d620b2f&redirect_uri=https://localhost:5000&response_type=code&scope=talk_message,friends
# response = requests.post(url, data=data)
# tokens = response.json()
# print(tokens)

#
# 카카오톡 메시지 API
url = "https://kauth.kakao.com/oauth/token"
data = {
    "grant_type": "refresh_token",
    "client_id": "c7f4c9c3247cf4f1765679d63d620b2f",
    "refresh_token": "xNB7BEMTZxtMme68mUIJ-bfp9clCOF5uAAAAAgo9cxgAAAGS4MhnurbGP5Eb7W-4",
    "client_secret" : "sNy5KFLhiDPLtk0WWIg7b35zj0MZKNcQ"
}
response = requests.post(url, data=data)
tokens = response.json()
print(f"token : {tokens}")
# kakao_code.json 파일 저장
with open("kakao_code.json", "w") as fp:
    json.dump(tokens, fp)

 # access_token = "65PgysKi8GuM8mRRcymul6ogLjofUEbiAAAAAQoqJVIAAAGS3XJWUM2yTeNnt1bO"
# refresh_token = "Qcmv29iYVs4WQS_mwkBur3fKr7Ej1GKfAAAAAgoqJVIAAAGS3XJWTc2yTeNnt1bO"

#
with open("kakao_code.json", "r") as fp:
    tokens = json.load(fp)
# print(tokens["access_token"])

url = "https://kapi.kakao.com/v1/api/talk/friends" #친구 목록 가져오기
header = {"Authorization": 'Bearer ' + tokens["access_token"]}
result = json.loads(requests.get(url, headers=header).text)
print(f"result : {result}")
friends_list = result.get("elements")
print(f"friends_list : {friends_list}")

friend_id = friends_list[1].get("uuid")
print(friend_id)

url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
header = {"Authorization": 'Bearer ' + tokens["access_token"]}
data={
    'receiver_uuids': '["{}"]'.format(friend_id),
    "template_object": json.dumps({
        "object_type":"text",
        "text":"딥러닝 뉴스",
        "link":{
            "web_url" : "https://www.google.co.kr/search?q=deep+learning&source=lnms&tbm=nws",
            "mobile_web_url" : "https://www.google.co.kr/search?q=deep+learning&source=lnms&tbm=nws"
        },
        "button_title": "뉴스 보기"
    })
}
response = requests.post(url, headers=header, data=data)
print(response.status_code)