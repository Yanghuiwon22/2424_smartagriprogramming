import requests
import concurrent.futures
import pandas as pd
from datetime import datetime, timedelta, timezone

# 필드 이름
field_names = {
    1: '온도',
    2: '습도',
    3: '일사량',
    4: '풍향',
    5: '풍속',
    6: '강우',
    7: '베터리 전압'
}

# 데이터를 가져오는 함수
def fetch_data(i):
    url = f'https://thingspeak.mathworks.com/channels/2328695/field/{i}.json'
    try:
        response = requests.get(url)
        response.raise_for_status()  # 상태 코드가 200이 아닐 때 예외 발생
        data = response.json()
        if 'feeds' in data and data['feeds']:
            # 24시간 이내 데이터 필터링 (현재 시각 - 24시간)
            latest_data = []
            now = datetime.now(timezone(timedelta(hours=9)))
            time_24_hours_ago = now - timedelta(hours=24)

            for feed in data['feeds']:
                utc_time_str = feed['created_at']

                utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                kst_time = utc_time.astimezone(timezone(timedelta(hours=9)))

                # KST 시간 형식으로 변환 (문자열)
                kst_time_str = kst_time.strftime("%Y-%m-%d %H:%M")

                if kst_time >= time_24_hours_ago:
                    latest_data.append({
                        'Date': kst_time_str,
                        field_names[i]: feed[f'field{i}']
                    })
            return latest_data if latest_data else None
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for field {i}: {e}")
        return None

# 데이터를 가져와서 데이터프레임으로 변환하는 함수
def jbnu_aws_data():
    result = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_data, i) for i in range(1, 8)]
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            if data:
                result.extend(data)

    if result:
        df = pd.DataFrame(result)
        df = df.groupby('Date', as_index=False).first()
        # 칼럼 순서 정렬
        df = df[['Date'] + [field_names[i] for i in range(1, 8)]]
        print(df)

        # CSV 파일로 저장 (덮어쓰기 모드)
        # hw08 디렉토리가 없다고 나옴,,? -> 다시 해보기..ㅠㅜ
        df.to_csv('/hw08/output_data.csv', index=False, encoding='utf-8-sig')

        print("Data saved to hw08/output_data.csv")
        return df

    else:
        print("No data available.")
        return pd.DataFrame()


if __name__ == "__main__":
    df = jbnu_aws_data()
