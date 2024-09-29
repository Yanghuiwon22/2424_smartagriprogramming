import os

import numpy as np
import requests
import pandas as pd

import csv

def get_data(sy, ey):  # -> api를 통해서 데이터 받아오기
    station_dic = {'Ichen':203, 'Cheonan':232, 'Sangju':137, 'Yeongcheon':281}

    for station, station_code in station_dic.items():

        print(station, station_code)
        for i in range(ey+1-sy):
            url = f'https://api.taegon.kr/stations/{station_code}/'

            params = {
                'sy' : sy+i,
                'ey' : sy+i,
                format : 'csv'
            }

            response = requests.get(url, params=params)
            if response.status_code == 200:
                content = response.json()
                df = pd.DataFrame(content)

                if not os.path.exists(f'output/{station}'):
                    os.makedirs(f'output/{station}')

                df.to_csv(f'output/{station}/{station}_{sy+i}')
                print(f'{sy+i}년도 데이터 저장 완.')
            else:
                print(response.status_code)

def DVR_model(): # --> DVR모델
    output_path = 'output'
    output_list = os.listdir(output_path)

    for output_folder in output_list:
        file_list = os.listdir(os.path.join(output_path, output_folder))
        print(file_list)
        file_list.sort()
        flowering_df = pd.DataFrame()

        if not f'DVS_{output_folder}_model' in file_list:

            for i in file_list: #하나의 파일 ex.Icheon_2004

                if i != f'flowering_date_{output_folder}.csv':
                    df = pd.read_csv(os.path.join(output_path, output_folder, i))

                    print(df)
                    # DVR모델 계산
                    pear_a = 107.94
                    pear_b = 0.9

                    DVS = 0
                    for i in range(len(df)):
                        if df.iloc[i]['tavg'] >= 5:

                            DVRi = (1 / (pear_a * (pear_b ** df.iloc[i]['tavg']))) * 100
                            DVS += DVRi

                            if DVS >= 100:

                                dic = {'Station':output_folder, 'Date': df.iloc[i]['Date'], 'DVS':DVS}
                                df_save = pd.DataFrame([dic])

                                flowering_df = pd.concat([flowering_df, df_save])
                                break
                        flowering_df.to_csv(f'output/{output_folder}/DVS_{output_folder}_model')

                    else:
                        pass

def get_flowering_date():
    input_file = 'obs_date.txt'
    output_file = 'flowering_date.csv'

    # txt 파일에서 데이터를 읽어와 csv로 변환
    with open(input_file, 'r', encoding='utf-8') as txt_file, open(output_file, 'w', newline='',
                                                                   encoding='utf-8') as csv_file:

        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['생육일조사지역', '만개기'])

        # 각 줄을 읽어 필요한 부분만 추출
        for line in txt_file:
            columns = line.strip().split()  # 공백으로 분리
            if len(columns) >= 3 and columns[0] != '생육일조사지역':  # 유효한 데이터인 경우만 처리
                # 생육일조사지역과 만개기 추출
                region = columns[0]
                flowering_date = columns[2]
                csv_writer.writerow([region, flowering_date])

    df = pd.read_csv('flowering_date.csv')

    df_naju = pd.DataFrame()
    df_icheon = pd.DataFrame()
    df_cheonan = pd.DataFrame()
    df_sangju = pd.DataFrame()
    df_yoengcheon = pd.DataFrame()
    df_wanju = pd.DataFrame()
    df_ulju = pd.DataFrame()
    df_sacheon = pd.DataFrame()

    for i in range(len(df)):
        print(df.iloc[i])
        if df.iloc[i]['생육일조사지역'] == '나주':
            dic_naju = {'station':'naju', 'year':df.iloc[i]['만개기'].split('-')[0], 'Date':df.iloc[i]['만개기']}
            df_dic = pd.DataFrame([dic_naju])
            df_naju = pd.concat([df_naju, df_dic])

        elif df.iloc[i]['생육일조사지역'] == '이천':
            dic_icheon = {'station':'icheon', 'year':df.iloc[i]['만개기'].split('-')[0], 'Date':df.iloc[i]['만개기']}
            df_dic = pd.DataFrame([dic_icheon])
            df_icheon = pd.concat([df_icheon, df_dic])

        elif df.iloc[i]['생육일조사지역'] == '천안':
            dic_cheonan = {'station':'cheonan', 'year':df.iloc[i]['만개기'].split('-')[0], 'Date':df.iloc[i]['만개기']}
            df_dic = pd.DataFrame([dic_cheonan])
            df_cheonan = pd.concat([df_cheonan, df_dic])

        elif df.iloc[i]['생육일조사지역'] == '상주':
            dic_sangju = {'station':'sangju', 'year':df.iloc[i]['만개기'].split('-')[0], 'Date':df.iloc[i]['만개기']}
            df_dic = pd.DataFrame([dic_sangju])
            df_sangju = pd.concat([df_sangju, df_dic])

        elif df.iloc[i]['생육일조사지역'] == '영천':
            dic_yoengcheon = {'station':'yoengcheon', 'year':df.iloc[i]['만개기'].split('-')[0], 'Date':df.iloc[i]['만개기']}
            df_dic = pd.DataFrame([dic_yoengcheon])
            df_yoengcheon = pd.concat([df_yoengcheon, df_dic])

        elif df.iloc[i]['생육일조사지역'] == '완주':
            dic_wanju = {'station':'wanju', 'year':df.iloc[i]['만개기'].split('-')[0], 'Date':df.iloc[i]['만개기']}
            df_dic = pd.DataFrame([dic_wanju])
            df_wanju = pd.concat([df_wanju, df_dic])

        elif df.iloc[i]['생육일조사지역'] == '울주':
            dic_ulju = {'station':'ulju', 'year':df.iloc[i]['만개기'].split('-')[0], 'Date':df.iloc[i]['만개기']}
            df_dic = pd.DataFrame([dic_ulju])
            df_ulju = pd.concat([df_ulju, df_dic])

        elif df.iloc[i]['생육일조사지역'] == '사천':
            dic_sacheon = {'station':'sacheon', 'year':df.iloc[i]['만개기'].split('-')[0], 'Date':df.iloc[i]['만개기']}
            df_dic = pd.DataFrame([dic_sacheon])
            df_sacheon = pd.concat([df_sacheon, df_dic])

    df_naju.to_csv('output/naju/flowering_date_naju.csv')
    df_icheon.to_csv('output/Ichen/flowering_date_Ichen.csv')
    df_cheonan.to_csv('output/Cheonan/flowering_date_Cheonan.csv')
    df_sangju.to_csv('output/Sangju/flowering_date_Sangju.csv')
    df_yoengcheon.to_csv('output/Yeongcheon/flowering_date_Yeongcheon.csv')
    df_wanju.to_csv('output/wanju/flowering_date_wanju.csv')
    df_ulju.to_csv('output/ulju/flowering_date_ulju.csv')
    df_sacheon.to_csv('output/sacheon/flowering_date_sacheon.csv')

def get_other_region_data():
    file_list = ['aws_data.csv', 'aws_data_2.csv', 'aws_data_3.csv']
    for file in file_list:
        df = pd.read_csv(file, encoding='cp949')
        station_dic = {'나주':'naju', '완주':'wanju', '두서':'ulju', '사천':'sacheon'}

        # 지역별 데이터프레임을 저장할 딕셔너리
        df_dict = {}

        # 각 지점명을 기준으로 데이터프레임 분리하여 딕셔너리에 저장
        for i in df['지점명'].unique():
            try:
                df_dict[station_dic[i]] = df[df['지점명'] == i]

                df_dict[station_dic[i]]['년도'] = pd.to_datetime(df_dict[station_dic[i]]['일시']).dt.year
                df_dict[station_dic[i]]['tavg'] = df_dict[station_dic[i]]['평균기온(°C)']
                df_dict[station_dic[i]]['Date'] = df_dict[station_dic[i]]['일시']

                # 연도별로 데이터를 저장할 딕셔너리
                yearly_data_dict = {}

                # 연도별로 데이터프레임을 분리하여 딕셔너리에 저장
                for year, group in df_dict[station_dic[i]].groupby('년도'):
                    yearly_data_dict[year] = group

                for year, data in yearly_data_dict.items():

                    if not os.path.exists(f'output/{station_dic[i]}'):
                        os.makedirs(f'output/{station_dic[i]}')
                    data.to_csv(f'output/{station_dic[i]}/{station_dic[i]}_{year}.csv', index=False, encoding='utf-8-sig')

            except:
                pass

# def main():
#
#
#     # DVR모델을 위한 데이터 수집
#     get_data(2004, 2024)
#     get_other_region_data()
#     DVR_model()
#     get_flowering_date()

def main():
    output_path = 'output'
    # output_list = os.listdir(output_path)

    output_list = ['Ichen'] # 테스트를 위한 데이터 정리
    for station in output_list:
        print(station)

        df = pd.DataFrame()

        obj_date = pd.read_csv(f'output/{station}/flowering_date_{station}.csv')
        dvs_date = pd.read_csv(f'output/{station}/DVS_{station}_model')

        df['station'] = [station for i in range(len(obj_date))]
        df['year'] = obj_date['Date'].apply(lambda x: x.split('-')[0])

        df['obj_date'] = obj_date['Date']
        df['DVS_date'] = dvs_date['Date']

        # 'obj_date'와 'DVS_date'를 datetime 형식으로 변환
        df['obj_date'] = pd.to_datetime(df['obj_date'])
        df['DVS_date'] = pd.to_datetime(df['DVS_date'])

        # 월-일만 추출해서 새로운 열에 저장
        df['obj_date'] = df['obj_date'].dt.strftime('%m-%d')
        df['DVS_date'] = df['DVS_date'].dt.strftime('%m-%d')

        print(df)




if __name__ == '__main__':
    main()
