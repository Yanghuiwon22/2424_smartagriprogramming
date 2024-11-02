import requests
import concurrent.futures
import os
import pytz
import pandas as pd
import urllib.request as urllib2
from datetime import datetime, timedelta, timezone
#
# # 필드 이름
# field_names = {
#     1: '온도',
#     2: '습도',
#     3: '일사량',
#     4: '풍향',
#     5: '풍속',
#     6: '강우',
#     7: '베터리 전압'
# }
#
# # 데이터를 가져오는 함수
# def fetch_data(i):
#     url = f'https://thingspeak.mathworks.com/channels/2328695/field/{i}.json'
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # 상태 코드가 200이 아닐 때 예외 발생
#         data = response.json()
#         if 'feeds' in data and data['feeds']:
#             # 24시간 이내 데이터 필터링 (현재 시각 - 24시간)
#             latest_data = []
#             now = datetime.now(timezone(timedelta(hours=9)))
#             time_24_hours_ago = now - timedelta(hours=24)
#
#             for feed in data['feeds']:
#                 utc_time_str = feed['created_at']
#
#                 utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
#                 kst_time = utc_time.astimezone(timezone(timedelta(hours=9)))
#
#                 # KST 시간 형식으로 변환 (문자열)
#                 kst_time_str = kst_time.strftime("%Y-%m-%d %H:%M")
#
#                 if kst_time >= time_24_hours_ago:
#                     latest_data.append({
#                         'Date': kst_time_str,
#                         field_names[i]: feed[f'field{i}']
#                     })
#             return latest_data if latest_data else None
#         else:
#             return None
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching data for field {i}: {e}")
#         return None
#
# # 데이터를 가져와서 데이터프레임으로 변환하는 함수
def jbnu_aws_data():
    result = []
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = [executor.submit(fetch_data, i) for i in range(1, 8)]
    #     for future in concurrent.futures.as_completed(futures):
    #         data = future.result()
    #         if data:
    #             result.extend(data)


    if result:
        df = pd.DataFrame(result)
        df = df.groupby('Date', as_index=False).first()
        # 칼럼 순서 정렬
        df = df[['Date'] + [field_names[i] for i in range(1, 8)]]

        df.to_csv('output_data.csv', index=False, encoding='utf-8-sig')

        return df

    else:
        print("No data available.")
        return pd.DataFrame()

# aws 실시간 데이터 가져오기


desired_timezone = pytz.timezone('Asia/Seoul')

def get_date_list(start_date_str, end_date_str):
    try:
        start_date = datetime.strptime(start_date_str, "%Y%m%d")
        end_date = datetime.strptime(end_date_str, "%Y%m%d")
    except:
        start_date = start_date_str
        end_date = end_date_str

    date_list = []

    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)

    return date_list

def get_aws(date):
    Site = 85
    Dev = 1
    Year = date.year
    Mon = f"{date.month:02d}"
    Day = f"{date.day:02d}"

    aws_url =f'http://203.239.47.148:8080/dspnet.aspx?Site={Site}&Dev={Dev}&Year={Year}&Mon={Mon}&Day={Day}'
    data = urllib2.urlopen(aws_url)
    print(aws_url)

    df = pd.read_csv(data, header=None)
    df.columns = ['datetime', 'temp', 'hum', 'X', 'X', 'X', 'rad', 'wd', 'X', 'X', 'X', 'X', 'X', 'ws', 'rain', 'maxws', 'bv', 'X']
    drop_cols = [col for col in df.columns if 'X' in col]
    df = df.drop(columns=drop_cols)
    return df



def save_aws(start_date, end_date):
    save_dir = 'hw08/output/AWS'
    date_list = get_date_list(start_date, end_date)

    for date in date_list:
        os.makedirs(os.path.join(save_dir, f'{date.year}'), exist_ok=True)  # 경로가 없으면 만들기, 있으면 넘어감.

        filename = os.path.join(save_dir, f'{date.year}_{date.month}.csv')
        if os.path.exists(filename):
            print('exist')
            df = pd.read_csv(filename)
            each_data = get_aws(date)

            each_data = pd.concat([df, each_data], axis=0)
        else:
            each_data = get_aws(date)

        each_data = each_data.drop_duplicates()
        each_data.to_csv(f'{filename}', index=False)


def main():
    start_date_str = datetime.now().date() - timedelta(days=1)
    end_date_str = datetime.now().date()

    save_aws(start_date_str, end_date_str)

if __name__ == '__main__':
    main()
