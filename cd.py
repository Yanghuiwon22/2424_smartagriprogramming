import os
import pandas as pd
import math

# 기준온도, 저온요구도, 고온요구도 설정
tc = 5.4
cr = -86.4
Hr = 272


# 냉각량 계산 함수
def chill_days(tmax, tmin, tavg):
    if 0 <= tc <= tmin <= tmax:
        cd = 0
    elif 0 <= tmin <= tc < tmax:
        cd = -((tavg - tmin) - (tmax - tc) ** 2 / (2 * (tmax - tmin)))
    elif 0 <= tmin <= tmax <= tc:
        cd = -(tavg - tmin)
    elif tmin < 0 <= tmax <= tc:
        cd = -(tmax ** 2 / (2 * (tmax - tmin)))
    elif tmin < 0 < tc < tmax:
        cd = -(tmax ** 2 / (2 * (tmax - tmin))) - ((tmax - tc) ** 2 / (2 * (tmax - tmin)))
    else:
        cd = 0
    return cd


# 가온량 계산 함수
def anti_chill_days(tmax, tmin, tavg):
    if 0 <= tc <= tmin <= tmax:
        hr = tavg - tc
    elif 0 <= tmin <= tc < tmax:
        hr = (tmax - tc) ** 2 / (2 * (tmax - tmin))
    elif 0 <= tmin <= tmax <= tc:
        hr = 0
    elif tmin < 0 <= tmax <= tc:
        hr = 0
    elif tmin < 0 < tc < tmax:
        hr = (tmax - tc) ** 2 / (2 * (tmax - tmin))
    else:
        hr = 0
    return hr


# mDVR_hourly_temp 코드와 동일한 방식으로 처리
def mDVR_cd_model():
    # 데이터 불러오기
    output_path = 'output'
    output_list = os.listdir(output_path)
    output_list = ['Ichen']  # 테스트를 위한 데이터 정리
    for output_folder in output_list:
        file_path = os.listdir(os.path.join(output_path, output_folder))
        for station_file in file_path:

            # 현재 데이터 없어서 처리 -> 데이터 생기면 삭제
            if not (
                    'wanju' in station_file or 'ulju' in station_file or 'sacheon' in station_file or 'naju' in station_file):
                if not (
                        'flowering_date' in station_file or 'DVS' in station_file or 'mDVR' in station_file):  # 기상데이터만 남기기
                    df = pd.read_csv(os.path.join(output_path, output_folder, station_file))

                    # tavg 계산 추가
                    df['tavg'] = (df['tmax'] + df['tmin']) / 2
                    df['cd'] = 0  # 냉각량 초기화
                    df['hr'] = 0  # 가온량 초기화

                    cumulative_cd = 0
                    cumulative_hr = 0
                    dormancy_released = False
                    flowering_date = None

                    for idx, row in df.iterrows():
                        tmax = row['tmax']
                        tmin = row['tmin']
                        tavg = row['tavg']

                        # 냉각량 계산
                        cd_value = chill_days(tmax, tmin, tavg)
                        df.at[idx, 'cd'] = cd_value
                        cumulative_cd += cd_value

                        # 저온 요구량에 도달했을 때 내생휴면 해재
                        if not dormancy_released and cumulative_cd <= cr:
                            dormancy_released = True
                            release_date = row['Date']
                            print(f"내생휴면 해재일: {release_date}")

                        # 내생휴면 해재 후 가온량 계산
                        if dormancy_released:
                            hr_value = anti_chill_days(tmax, tmin, tavg)
                            df.at[idx, 'hr'] = hr_value
                            cumulative_hr += hr_value

                            # 누적 가온량이 고온 요구량에 도달했을 때 만개일 예측
                            if cumulative_hr >= hr_threshold and flowering_date is None:
                                flowering_date = row['Date']
                                print(f"예상 만개일: {flowering_date}")

                    # 결과 DataFrame을 저장하거나 출력할 수 있음
                    # df.to_csv(f"{output_folder}_processed.csv", index=False)
                    print(df[['Date', 'tmax', 'tmin', 'tavg', 'cd', 'hr']])


# 함수 실행
mDVR_cd_model()
