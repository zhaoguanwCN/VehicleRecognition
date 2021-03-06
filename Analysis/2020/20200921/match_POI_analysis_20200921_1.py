import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import sys
import datetime
import math
pi = 3.1415926535897932384626  # π
ee = 0.00669342162296594323
'''@Author Hou Jue
   20200910'''


def dataPrePorcess(flag,data_byDay):


    if flag==1:
        pcev_list = os.listdir("D:\\data\\私家车\\纯电\\")
        pcphev_list= os.listdir("D:\\data\\私家车\\混动\\")
        didi_list = os.listdir("D:\\data\\网约车\\")
        taxi_list = os.listdir("D:\\data\\出租车\\")

        ''' didi-EV'''
        for didi_id in didi_list:
            data_didi_HEV = pd.read_csv('D:\\data\\网约车\\' + didi_list)
            data_didi_HEV['time'] = pd.to_datetime(data_didi_HEV['time']).apply(lambda x: x.date())

    data_didi_HEV=data_byDay
    data_didi_HEV['lng_new'] = 0.000000
    data_didi_HEV['lat_new'] = 0.000000


    for i in range(data_didi_HEV.index.tolist()[0],data_didi_HEV.index.tolist()[-1]):
        data_didi_HEV['lng_new'][i] = transfer(data_didi_HEV['longitude'][i], data_didi_HEV['latitude'][i])[0]
        data_didi_HEV['lat_new'][i] = transfer(data_didi_HEV['longitude'][i], data_didi_HEV['latitude'][i])[1]

    # return  data_didi_HEV
    return  data_didi_HEV



def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret

def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def transfer(lng, lat):   #NO
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]



def divideDay(day):
    # data_didi_HEV = pd.read_csv('D:\\data\\出租车\\SHEVDC_1A5H2N7C.csv')
    '''didi'''
    # data_didi_HEV = pd.read_csv('D:\\2020.09.10\\HJ\\pick_vehicle\\didi\\SHEVDC_546B660B.csv')
    '''pc_ev'''
    # data_didi_HEV = pd.read_csv('D:\\2020.09.10\\HJ\\pick_vehicle\\pc_ev\\SHEVDC_3M4S302G.csv')
    '''pc_hev'''
    # data_didi_HEV = pd.read_csv('D:\\2020.09.10\\HJ\\pick_vehicle\\pc_hev\\SHEVDC_4L10316B.csv')
    '''taxi'''
    data_didi_HEV = pd.read_csv('D:\\2020.09.10\\HJ\\pick_vehicle\\taxi\\SHEVDC_341O5511.csv') #输入车辆名称的文件名
    data_didi_HEV['time'] = pd.to_datetime(data_didi_HEV['time']).apply(lambda x: x.date())
    data_byDay_index=data_didi_HEV[data_didi_HEV.loc[:, 'time']== pd.to_datetime(day)].index.tolist()
    data_byDay=data_didi_HEV.loc[data_byDay_index,:]
    '''to Dataframe'''
    return data_byDay


def POIPorcess():

    df_airport=pd.read_excel('C:\\Users\\admin\\PycharmProjects\\pythonProject\\20200910\\match_POI\\data\\airport.xlsx')
    df_railway=pd.read_excel('C:\\Users\\admin\\PycharmProjects\\pythonProject\\20200910\\match_POI\\data\\railway_station.xlsx')

    '''airport'''
    df_airport_location=df_airport.loc[:,'location']
    airport_location=list(df_airport_location)

    pd_airport_location=pd.DataFrame(df_airport_location)
    pd_airport_location.loc[0,'location'].split(',')

    '''railway station'''
    df_railway_location = df_railway.loc[:, 'location']
    railway_location = list(df_railway_location)

    pd_railway_location = pd.DataFrame(df_railway_location)
    pd_railway_location.loc[0, 'location'].split(',')

    airport_location_volume=pd_airport_location.shape[0]
    railway_location_volume=pd_railway_location.shape[0]

    '''airport'''
    airport_location_2_column=[]
    airport_location_2_column=[pd_airport_location.loc[i,'location'].split(',') for i in range(airport_location_volume)]

    '''railway station'''
    railway_location_2_column = []
    railway_location_2_column = [pd_railway_location.loc[i, 'location'].split(',') for i in range(railway_location_volume)]

    '''20200909
       需要将list中的str元素转为float,可以了'''
    # data= [[]]
    airport_location_done=list()

    '''airport'''
    for i in range(airport_location_volume):
        # data = list(map(eval, [airport_location_2_column[i] for i in range(100)]))
        # data[i] = list(map(eval, airport_location_2_column[i]))
        '''还是用append好些，用list的索引添加很多问题'''
        airport_location_done.append(list(map(eval, airport_location_2_column[i])))

    '''二维数组再转为DataFrame格式，可以了'''
    airport_location_done=pd.DataFrame(airport_location_done,columns=['longitude','latitude'])

    '''railway station'''
    railway_location_done = list()
    for i in range(railway_location_volume):
        railway_location_done.append(list(map(eval, railway_location_2_column[i])))
    railway_location_done = pd.DataFrame(railway_location_done, columns=['longitude', 'latitude'])

    # airport_location.split(",") #字符串转为列表有split(",")
    s1 = ','.join(str(n) for n in airport_location)
    a=1
    return airport_location_done,railway_location_done


def matchPOI(data_byDay):

    airport_location, railway_location=POIPorcess()
    flag=0
    data_didi_HEV = dataPrePorcess(flag,data_byDay)
    data_didi_HEV_location=pd.concat([data_didi_HEV['lat_new'],data_didi_HEV['lng_new']],axis=1)

    '''airport'''
    match_points_airport=0
    for i in range(airport_location.shape[0]):
        for j in range(data_didi_HEV_location.index[0],data_didi_HEV_location.index[-1]):
            if (data_didi_HEV_location.loc[j,'lat_new'].round(decimals=3)==airport_location.loc[i,'latitude'].round(decimals=3))\
                    and (data_didi_HEV_location.loc[j,'lng_new'].round(decimals=3)==airport_location.loc[i,'longitude'].round(decimals=3)):
                match_points_airport+=1

    '''railway station'''
    match_points_railway = 0
    for i in range(railway_location.shape[0]):
        for j in range(data_didi_HEV_location.index[0],data_didi_HEV_location.index[-1]):
            if (data_didi_HEV_location.loc[j,'lat_new'].round(decimals=3)==railway_location.loc[i,'latitude'].round(decimals=3))\
                    and (data_didi_HEV_location.loc[j,'lng_new'].round(decimals=3)==railway_location.loc[i,'longitude'].round(decimals=3)):
                match_points_railway+=1

    return match_points_airport,match_points_railway


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    days=['2019-09-01','2019-09-02','2019-09-03','2019-09-04','2019-09-05','2019-09-06','2019-09-07','2019-09-08']
    for day in days:
        data_byDay=divideDay(day)
        # match_points_airport,match_points_railway=matchPOI()
        match_points_airport,match_points_railway=matchPOI(data_byDay)
        print('{}'.format(day))
        print('match_points_airport:{}\nmatch_points_railway_station:{}'.format(match_points_airport,match_points_railway))
        endtime = datetime.datetime.now()

        print('CPU time(s):',(endtime - starttime).seconds)
        print('---------------------------------')



