import os
import pandas as pd
import numpy as np
import math

import requests
def xls2csv():
    data_dir = 'data'
    for dir in os.listdir(data_dir):
        df_year = pd.DataFrame()

        dir_path = os.path.join(data_dir, dir)
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            df = pd.read_table(file_path, encoding='euc-kr', skiprows=6)
            df.columns = ['date', 'tavg', '-', 'tmax', 'tmin', 'hum', 'rain', 'sun', '-', 'windavg', 'windmax']
            df = df[['date', 'tavg', 'tmax', 'tmin']]
            df_year = pd.concat([df_year, df])

        df_year.sort_values(by='date', inplace=True)
        df_year = df_year.drop_duplicates()

        df_year['year'] = df_year['date'].apply(lambda x: x[:4])
        grouped = df_year.groupby('year')
        for year, group in grouped:
            group.to_csv(f'output/{dir}_{year}.csv', index=False)

def get_data(sy, ey):
    # station_dic = {'Pocheon': 98, 'Hwaseong':119, 'Geochang': 946, 'Gunwi':278, 'Cheongsong':276, 'Chungju':127}
    station_dic = {'Pocheon': 98, 'Hwaseong': 119, 'Gunwi': 278, 'Chungju': 127}
    for station, station_code in station_dic.items():
        print(station, station_code)

        if not os.path.exists(f'output/{station}/weather_data/{station}_{sy+1}.csv'):
            for i in range(ey+1-sy):
                url = f'https://api.taegon.kr/stations/{station_code}/'

                params = {
                    'sy' : sy+i,
                    'ey' : sy+i,
                    format : 'csv'
                }

                response = requests.get(url, params=params, verify=False)
                if response.status_code == 200:
                    content = response.json()
                    df = pd.DataFrame(content)

                    if not os.path.exists(f'output/{station}'):
                        os.makedirs(f'output/{station}')

                    if not os.path.exists(f'output/{station}/weather_data'):
                        os.makedirs(f'output/{station}/weather_data')

                    df.to_csv(f'output/{station}/weather_data/{station}_{sy+i}.csv')
                    print(f'{sy+i}년도 데이터 저장 완료.')
                else:
                    print(response.status_code)
def dvr1():
    a = 95.6
    b = -4.5

    station_list = os.listdir('output')
    for station in station_list:
        csv_flies = os.listdir(f'output/{station}/weather_data')
        dvr1_df = pd.DataFrame()

        for csv_file in csv_flies:
            df = pd.read_csv(f'output/{station}/weather_data/{csv_file}')

            df['tavg_above_5'] = df['tavg'] > 5  # tavg 값이 5도 이상인 경우 True
            df['3_day_streak'] = df['tavg_above_5'].rolling(window=3).sum() == 3  # 3일 연속 True

            first_valid_index = df[df['3_day_streak']].index.min() - 2
            # print(first_valid_index)

            df['tavg'] = df['tavg'].clip(upper=20)
            df['dvr'] = np.where(df['tavg'] < 5, 0, (1 / (a + b * df['tavg'])) * 100)

            # 3일 연속 5도 이상인 첫 번째 행부터 데이터프레임 반환
            df = df.iloc[first_valid_index:]

            df['dvr_cumsum'] = df['dvr'].cumsum()
            first_day_over_100 = df[df['dvr_cumsum'] >= 100].iloc[0]

            df_dic = {'station': station, 'dvr1': first_day_over_100['date']}
            dvr1_df = pd.concat([dvr1_df, pd.DataFrame([df_dic])])

        dvr1_df['year'] = dvr1_df['dvr1'].astype(str).apply(lambda x: x[:4])
        dvr1_df = dvr1_df[['station', 'year', 'dvr1']].sort_values('year')

        # print(dvr1_df)

        dvr1_df.to_csv(f'output/{station}/{station}_dvr1.csv', index=False)

def dvr2():
    a = 0.2584

    station_list = os.listdir('output')
    for station in station_list:
        csv_flies = os.listdir(f'output/{station}/weather_data')
        dvr2_df = pd.DataFrame()

        for csv_file in csv_flies:
            df = pd.read_csv(f'output/{station}/weather_data/{csv_file}')

            first_tavg_over_5 = df[df['tavg'] > 5].iloc[0]
            df = df.iloc[first_tavg_over_5.name:]

            df['dvr'] = a * df['tavg']
            df['dvr_cumsum'] = df['dvr'].cumsum()
            first_day_over_100 = df[df['dvr_cumsum'] >= 100].iloc[0]

            df_dic = {'station': station, 'dvr2': first_day_over_100['date']}
            dvr2_df = pd.concat([dvr2_df, pd.DataFrame([df_dic])])

        dvr2_df['year'] = dvr2_df['dvr2'].astype(str).apply(lambda x: x[:4])
        dvr2_df = dvr2_df[['station', 'year', 'dvr2']].sort_values('year')

        dvr2_df.to_csv(f'output/{station}/{station}_dvr2.csv', index=False)

def cd_model():
    Tc = 6.1
    Cr = -100.5
    Hr = 271.5

    station_list = os.listdir('output')
    for station in station_list:
        csv_flies = os.listdir(f'output/{station}/weather_data')
        cd_df = pd.DataFrame()

        for csv_file in csv_flies:
            df = pd.read_csv(f'output/{station}/weather_data/{csv_file}')
            for idx, row in df.iterrows():
                Tx = row['tmax']
                Tn = row['tmin']
                Tm = row['tavg']

                if 0 <= Tc <= Tn <= Tx:
                    cd = 0
                    Ca = Tm -Tc
                    df.loc[idx, 'cd'] = cd
                    df.loc[idx, 'Ca'] = Ca

                elif 0 <= Tn <= Tc < Tx:
                    cd = -((Tm - Tn)-((Tx-Tc)/2))
                    Ca = (Tx-Tc)/2
                    df.loc[idx, 'cd'] = cd
                    df.loc[idx, 'Ca'] = Ca


                elif 0 <= Tn <= Tx <= Tc:
                    cd = -(Tm -Tn)
                    Ca = 0
                    df.loc[idx, 'cd'] = cd
                    df.loc[idx, 'Ca'] = Ca

                elif Tn < 0 < Tx <= Tc:
                    cd = -(Tx/(Tx-Tn))*(Tx/2)
                    Ca = 0
                    df.loc[idx, 'cd'] = cd
                    df.loc[idx, 'Ca'] = Ca

                elif Tn < 0 < Tc < Tx:
                    cd = -((Tx/(Tx-Tn))*(Tx/2)*((Tx-Tc)/2))
                    Ca = (Tx-Tc)/2
                    df.loc[idx, 'cd'] = cd
                    df.loc[idx, 'Ca'] = Ca

            df['cd_sum'] = df['cd'].cumsum()
            first_day_over_Cr = df[df['cd_sum'] <= -100.5].iloc[0]

            df['Ca_sum'] = df['Ca'].cumsum()
            first_day_over_Hr = df[df['Ca_sum'] >= 271.5].iloc[0]

            df_dic = {'station': station, 'first_day_over_Cr': first_day_over_Cr['date'], 'cd' : first_day_over_Hr['date']}
            cd_df = pd.concat([cd_df, pd.DataFrame([df_dic])])

        cd_df['year'] = cd_df['cd'].astype(str).apply(lambda x: x[:4])
        cd_df = cd_df[['station', 'year', 'cd']].sort_values('year')

        cd_df.to_csv(f'output/{station}/{station}_cd.csv', index=False)

def dm_gdh_model():

    # DM 모델 구현


    # GDH 모델 구현
    Tb = 4
    Tu =25
    Tc = 36

    if Tb < Th <= Tu:
        GDH = (Tu - Tb)/2 * (1+math.cos(math.pi + math.pi*(Th - Tb)/(Tu - Tb)))
    elif Tu < Th <= Tc:
        GDH = (Tu-Tb) * (1+math.cos(math.pi/2 + math.pi/2*(Th-Tu)/(Tc-Tu)))
    else:
        GDH = 0

def concat_result():
    station_list = os.listdir('output')
    for station in station_list:
        dvr1_df = pd.read_csv(f'output/{station}/{station}_dvr1.csv')
        dvr2_df = pd.read_csv(f'output/{station}/{station}_dvr2.csv')
        cd_df = pd.read_csv(f'output/{station}/{station}_cd.csv')
        flowering_df = pd.read_csv(f'output/{station}/{station}.csv')

        flowering_df['year'] = flowering_df['obj'].astype(str).apply(lambda x: x[:4]).astype(int)
        flowering_df = flowering_df[['station', 'year', 'obj']]
        flowering_df = flowering_df.sort_values('year')

        result_df = pd.merge(dvr1_df, dvr2_df, on=['year', 'station'], how='outer')
        result_df = pd.merge(result_df, cd_df, on=['year', 'station'], how='outer')
        result_df = pd.merge(result_df, flowering_df, on=['year', 'station'], how='outer')

        result_df['dvr1'] = result_df['dvr1'].astype(str).apply(lambda x: x[4:])
        result_df['dvr2'] = result_df['dvr2'].astype(str).apply(lambda x: x[4:])
        result_df['cd'] = result_df['cd'].astype(str).apply(lambda x: x[4:])
        result_df['obj'] = result_df['obj'].astype(str).apply(lambda x: x[5:])

        result_df['dvr1'] = result_df['dvr1'].apply(lambda x: f"{x[:2]}-{x[2:]}")
        result_df['dvr2'] = result_df['dvr2'].apply(lambda x: f"{x[:2]}-{x[2:]}")
        result_df['cd'] = result_df['cd'].apply(lambda x: f"{x[:2]}-{x[2:]}")

        result_df['dvr1'] = pd.to_datetime(result_df['dvr1'], format='%m-%d')
        result_df['dvr2'] = pd.to_datetime(result_df['dvr2'], format='%m-%d')
        result_df['cd'] = pd.to_datetime(result_df['cd'], format='%m-%d')
        result_df['obj'] = pd.to_datetime(result_df['obj'], format='%m-%d')

        result_df.to_csv(f'output/{station}/{station}_result.csv', index=False)

def main():
    if not os.path.exists('output'):
        os.makedirs('output')

    # 엑셀 형태의 데이터 -> csv파일의 형태로 변경하기 ( 처음에만 하면 됌 ) --> 논문 구현
    # xls2csv()

    # api.taegon.kr 데이터 가져오기  --> 최초 1회
    get_data(2021, 2024)

    # 첫번째 모델 돌리기 : DVR1 ==> 파일에 정리 완.
    # dvr1()

    # 두번째 모델 돌리기 : DVR2 ==> 파일에 정리 완.
    # dvr2()

    # 세번째 모델 돌리기 : CD모델
    # cd_model()

    # 네번째 모델 돌리기 : DM + GDH 모델
    # dm_gdh_model()

    # ( DVR1, DVR2, CD모델 결과 + 실제 만개일 ) 파일 합치기
    concat_result()


if __name__ == '__main__':
   main()

