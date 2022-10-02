import requests
import pandas as pd
from bs4 import BeautifulSoup


"""
This code is to grab all the earthqukes datas and precipitation in Taiwan in the past decade.
The datas are from UGAS, China Earthquake Administration and Central Weather Bureau in Taiwan, which are used to improve the QuakeHunter platform.

df : 十年來的地震資料
station_list: 所有的氣象觀測站資料
result.csv : 三年來所有的氣象觀測資料

"""

#  抓所有的地震資料

import time
b = []
for i in range(1, 13):
    url = 'http://ditu.92cha.com/dizhen.php?page={}&dizhen_ly=china&dizhen_zjs=1&dizhen_zje=10&dizhen_riqis=2012-10-11&dizhen_riqie=2022-10-11&ckwz=台湾'.format(i)
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    tb = soup.find_all('td', class_='text-center')
    
    time.sleep(0.1)
    for j in tb:
        b.append(j.string)

    

times=[]
mag=[]
lon=[]
lat=[]
depth=[]

for i in range(0, len(b), 5):
    if(float(b[i+2])>120 and float(b[i+2])<122.5 and float(b[i+3])>22 and float(b[i+3])<25):
        times.append(b[i])
        mag.append(b[i+1])
        lon.append(b[i+2])
        lat.append(b[i+3])
        depth.append(b[i+4])
    
df = pd.DataFrame({'time':times, 'magnitude':mag, 'longitude':lon, 'Latitude':lat, 'depth':depth})

df.to_csv("earthquake_datas.csv", index=False, sep = ',')
print(len(df))


# In[16]:


df.head()



station_list = pd.read_excel("./測站資料.xlsx")
station_list.head()



import mpu

def geodistance(lng1,lat1,lng2,lat2):
    dist = mpu.haversine_distance((lat1, lng1), (lat2, lng2))
    return dist


def find_nearest_station(lng1, lat1):
    min_dis = -1
    station_id = ''
    for i in range (len(station_list)):
        dis = geodistance(lng1, lat1, station_list.loc[i, '經度'], station_list.loc[i, '緯度'])
        if min_dis > dis or min_dis == -1:
            min_dis = dis
            station_id = station_list.loc[i, '站號']
            altitude = station_list.loc[i, '海拔高度(m)']
    return station_id, altitude


#  找所有的地震資料最近的測站

nearest_station = []
date_list = []
altitude_list = []
for i in range(len(df)):
    #date = df.loc[i,'time'].split( )[0]
    lng = float( df.loc[i,'longitude'])
    lat = float( df.loc[i,'Latitude'])
    nearest_station.append(find_nearest_station(lng, lat)[0])
    altitude_list.append(find_nearest_station(lng, lat)[1])
    date_list.append(df.loc[i,'time'].split( )[0])

print(len(df)==len(nearest_station))
#  抓三年來所有地震最近測站的資料
import csv

csvfile="result.csv" #開個csv檔案準備寫入

with open(csvfile,"w+",newline="",encoding="utf-8") as fp:
    writer=csv.writer(fp)

    for i in range (len(df)):

        url="http://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station={}&stname=%25E8%258D%2589%25E5%25B6%25BA&datepicker={}&altitude={}m".format(nearest_station[i], date_list[i], altitude_list[i])  #網址
        #print(url)
        
        r=requests.get(url)
        r.encoding="utf-8"
        soup=BeautifulSoup(r.text,"html.parser")
        tag_table=soup.find(id="MyTable") #用BeautifulSoup找到table位置

        rows=tag_table.findAll("tr") #找到每個

        time.sleep(0.1)

        ct = 0
        for row in rows:
            if ct <3:
                ct= ct + 1 
                continue
            rowList=[]
            for cell in row.findAll(["td","th"]):
                rowList.append(cell.get_text().replace("\n","").replace("\r",""))
            writer.writerow(rowList)



import pandas as pd
#  找所有地震資料最近測站當日的降雨量

result = pd.read_csv('./result.csv')
total_list = []

for i in range (0, len(result), 24):
    total = 0
    for j in range (24):
        try:
            total = total + float(result.iloc[i+j, 10])
        except:
            total = total + 0
     
    total_list.append(total)
    
df['rainfall'] = total_list
df.to_csv("earthquake_datas.csv", index=False, sep = ',')


