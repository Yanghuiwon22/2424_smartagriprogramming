# 2424_smartagriprogramming
멤버 : 양희원, 박나현

## hw03_region_weather_api
* 주소창에 주소를 입력하면 해당 지역의 날씨 정보를 제공

## hw04_pair_20년치 

**코드 실행 순서**
```python

    get_data(2004, 2024)
    get_other_region_data()
    get_flowering_date()
    DVR_model()

```
위의 함수를 실행하면 필요한 데이터가 다 로드된다.

## apple_model
아래의 논문을 참고하여 사과나무 만개일 예측 모델을 구현하였다. <br>
**기온 변화에 따른 우리나라 사과 주산지 만개일 예측을 위한 모델 평가** 

* output/지역/weather_data/*.csv : 기상청에서 다운받은 지역별 날씨 데이터 <br>
* apple.py : 사과나무 만개일 예측 모델 <br>
  * get_data(sy, ey) : sy년부터 ey년까지의 데이터를 로드 (api.taegon.kr 사용)
  * dvr1(), dvr2(), cd_model() : 사과나무 만개일 예측 모델
  * concat_result() : 모델 결과를 하나의 데이터프레임으로 저장
  




