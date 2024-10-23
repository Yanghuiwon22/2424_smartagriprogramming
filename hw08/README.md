
# st에서 js 작동시키기
https://discuss.streamlit.io/t/how-to-run-a-javascript-code-in-streamlit/51556
### experimental_rerun 오류 해결
https://stackoverflow.com/questions/78834131/streamlit-version-1-37-st-rerun-it-doesnt-work
=> 작동 확인

# jbnu기상대 데이터 가져오기
api 주소 : https://thingspeak.mathworks.com/channels/2328695/

### for문을 사용해서 값을 가져오기 때문에, 시간이 약간 걸림
-> 이를 해결하기 위해 chatgpt를 사용

chatgpt 질문
```python
def jbnu_aws_data():
    result = {}  
    for i in range(1, 8):
    url = f'https://thingspeak.mathworks.com/channels/2328695/field/{i}.json'
            response = requests.get(url)
    if response.status_code == 200:
    result[i] = response.json()['feeds'][-1]
    print(result) 
```
더 속도빠르게 병렬로 처리 가능?

chatgpt 답변
```python
import requests
import concurrent.futures


def fetch_data(i):
    url = f'https://thingspeak.mathworks.com/channels/2328695/field/{i}.json'
    response = requests.get(url)
    if response.status_code == 200:
        return i, response.json()['feeds'][-1]
    return i, None

def jbnu_aws_data():
    result = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_data, i) for i in range(1, 8)]
        for future in concurrent.futures.as_completed(futures):
            i, data = future.result()
            if data:
                result[i] = data

    return result
```
위의 코드를 사용해서 구동해본 결과 로딩시간이 느껴지지 않을만큼 줄은 것을 확인


### 


