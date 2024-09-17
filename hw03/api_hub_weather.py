import requests
import pandas as pd
from io import StringIO

#기상청 API허브 --> 시단위 제공
def get_si_data():

    authKey = '1XPJ7YqLRkuzye2KiyZLhg'
    # URL 문자열
    url = f'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php?tm=202211300900&stn=0&help=1&authKey={authKey}'

    # 헤더 설정
    headers = {'Content-Type': 'application/xml'}

    # GET 요청을 보내고 응답을 받습니다.
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        df = pd.read_fwf(StringIO(response.text),
                         widths=[12, 4, 4, 5, 4, 6, 4, 7, 7, 3, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 2, 2, 26, 4, 4, 4, 9,
                                 5, 5, 5, 9, 4, 5, 4, 6, 7, 7, 7, 7, 4, 4, 4, 4])

        df.columns = df.iloc[51].values  ## chatGPT
        df = df[53:].reset_index(drop=True)  ## chatGPT

    else:
        print(response.status_code)


