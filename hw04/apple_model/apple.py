import os
import pandas as pd
import numpy as np
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

def dvr1():
    a = 95.6
    b = -4.5

    dvr1_df = pd.DataFrame()
    station_list = os.listdir('output')
    for station in station_list:
        csv_flies = os.listdir(f'output/{station}/weather_data')
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

        dvr1_df.to_csv(f'output/{station}/{station}_dvr1.csv', index=False)

def dvr2():
    a = 0.2584

    dvr2_df = pd.DataFrame()
    station_list = os.listdir('output')
    for station in station_list:
        csv_flies = os.listdir(f'output/{station}/weather_data')
        for csv_file in csv_flies:
            df = pd.read_csv(f'output/{station}/weather_data/{csv_file}')

            first_tavg_over_5 = df[df['tavg'] > 5].iloc[0]
            df = df.iloc[first_tavg_over_5.name:]

            df['dvr'] = a * df['tavg']
            df['dvr_cumsum'] = df['dvr'].cumsum()
            first_day_over_100 = df[df['dvr_cumsum'] >= 100].iloc[0]

            df_dic = {'station': station, 'dvr2': first_day_over_100['date']}
            dvr2_df = pd.concat([dvr2_df, pd.DataFrame([df_dic])])

        dvr2_df.to_csv(f'output/{station}/{station}_dvr2.csv', index=False)

def cd_model():
    Tc = 6.1
    Cr = -100.5
    Hr = 271.5

    cd_df = pd.DataFrame()
    station_list = os.listdir('output')
    for station in station_list:
        csv_flies = os.listdir(f'output/{station}/weather_data')
        for csv_file in csv_flies:
            df = pd.read_csv(f'output/{station}/weather_data/{csv_file}')
            print(df)

            for idx, row in df.iterrows():
                Tx = row['tmax']
                Tn = row['tmin']
                Tm = row['tavg']

                if 0 <= Tc <= Tn <= Tx:
                    cd = 0
                    df.loc[idx, 'type'] = 'case 1'
                    df.loc[idx, 'cd'] = cd

                elif 0 <= Tn <= Tc < Tx:
                    cd = -((Tm - Tn)-((Tx-Tc)/2))
                    df.loc[idx, 'type'] = 'case 2'
                    df.loc[idx, 'cd'] = cd

                elif 0 <= Tn <= Tx <= Tc:
                    cd = -(Tm -Tn)
                    df.loc[idx, 'type'] = 'case 3'
                    df.loc[idx, 'cd'] = cd

                elif Tn < 0 < Tx <= Tc:
                    cd = -(Tx/(Tx-Tn))*(Tx/2)
                    df.loc[idx, 'type'] = 'case 4'
                    df.loc[idx, 'cd'] = cd

                elif Tn < 0 < Tc < Tx:
                    cd = -((Tx/(Tx-Tn))*(Tx/2)*((Tx-Tc)/2))
                    df.loc[idx, 'type'] = 'case 5'
                    df.loc[idx, 'cd'] = cd

            print(df)





def main():
    if not os.path.exists('output'):
        os.makedirs('output')

    # 엑셀 형태의 데이터 -> csv파일의 형태로 변경하기 ( 처음에만 하면 됌 )
    # xls2csv()

    # 첫번째 모델 돌리기 : DVR1 ==> 파일에 정리 완.
    dvr1()

    # 두번째 모델 돌리기 : DVR2 ==> 파일에 정리 완.
    dvr2()

    # 세번째 모델 돌리기 : CD모델
    cd_model()


if __name__ == '__main__':
   main()

