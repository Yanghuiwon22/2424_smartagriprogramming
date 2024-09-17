import requests
import pandas as pd
from io import StringIO

authKey = '1XPJ7YqLRkuzye2KiyZLhg'
# URL 문자열
url = 'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php?tm=202211300900&stn=0&help=1&authKey=1XPJ7YqLRkuzye2KiyZLhg'

# 헤더 설정
headers = {'Content-Type': 'application/xml'}

# GET 요청을 보내고 응답을 받습니다.
response = requests.get(url, headers=headers)

if response.status_code == 200:
    df = pd.read_fwf(StringIO(response.text),
                     widths=[12, 4, 4, 5, 4, 6, 4, 7, 7, 3, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 2, 2, 26, 4, 4, 4, 9,
                             5, 5, 5, 9, 4, 5, 4, 6, 7, 7, 7, 7, 4, 4, 4, 4])

    # 필요한 부분만 남기고 df
    df = df[df['#START7777'].apply(lambda x: len(x) == 12)] ## chatGPT
    df['#START7777'] = pd.to_numeric(df['#START7777'], errors='coerce')  ## chatGPT
    df = df[df['#START7777'].notna()]  ## chatGPT
    print(df)


    # with open(response.text)

else:
    print(response.status_code)

# 응답을 JSON 형태로 변환
# json_response = response.json()

# print(json_response)