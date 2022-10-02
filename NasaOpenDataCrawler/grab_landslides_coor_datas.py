"""
This code is to grab all the landslides alarm datas in the past three years,
which is used to improve the QuakeHunter platform, too.

Output_Fikes:
landslide_datas.csv: all the landslides alarm datas in the past three years.

"""
import googlemaps
import os
import time
import pprint
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv
import pandas as pd



import requests
import pandas as pd
from bs4 import BeautifulSoup

b = []

name_list = ['108A', '108B', '108C', '108D', '109A', '109B', '109C', '109D', '110A', '110B', '110C', '110D', '111A', '111B', '111C', '111D']
for i in range(len(name_list)):
    url = 'https://ls.swcb.gov.tw/api/LandslideAlertHistoryOpenData/{}'.format(name_list[i])
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")
    
    #tb = soup.find_all('td', class_='text-center')
    
    time.sleep(0.1)
    for j in soup:
        b.append(j.string)


import numpy as np

result_list = []
col_list = ["AlertType", "DebrisNo", "LandslideID","LandslideName","County","Town","Vill","AlertLevel","LastUpdateDate","ReportID"]
 



for content in b:
    result = content.replace('"',"").replace("null","0").replace("[","").replace("]","").replace("}","")
    
    for col in col_list:
        result = result.replace(col+":", "")
    
    result = result.split("{")
    for i in range(2, len(result)):
        result_list.append(result[i].split(","))
    


for i in range(len(result_list)):
    
    try:
        if (len(result_list[i])!= 11):
            result_list.remove(result_list[i])
            
    except:
        continue

for i in range(len(result_list)):
    try:
        if (result_list[i][1] == '土石流編號'):
            result_list.remove(result_list[i])  
            
    except:
        continue

col_list2 = ["AlertType", "DebrisNo","None",  "LandslideID", "LandslideName","County","Town", "AlertLevel","LastUpdateDate","ReportID", "address"]
df = pd.DataFrame( columns=col_list2)

print(len(result_list))
for i in range(len(result_list)):
    try:
        df.loc[len(df)] = result_list[i]
    except:
        print(result_list[i])



df['address'] = df['LandslideName']+ df['County'] + df['Town']
df['test'] = df['LastUpdateDate']+ df['address']

df = df.drop_duplicates(subset=['test'])

print(df.info())


from googlemaps import Client as GoogleMaps
import pandas as pd 

gmaps = GoogleMaps('Your_API_KEY')


addresses =  pd.DataFrame(df['address'])
addresses['Date'] = df['LastUpdateDate']

addresses = addresses.reset_index()
del addresses['index']


addresses['long'] = ""
addresses['lat'] = ""
addresses['shift'] = addresses['address'].shift(1)
print(addresses)


# In[29]:


for x in range(len(addresses)):
    try:
        print("address = ", addresses['address'][x])
        time.sleep(1) #to add delay in case of large DFs
        geocode_result = gmaps.geocode(addresses['address'][x])
        addresses['lat'][x] = geocode_result[0]['geometry']['location'] ['lat']
        addresses['long'][x] = geocode_result[0]['geometry']['location']['lng']
    except IndexError:
        print("Address was wrong...")
    except Exception as e:
    
        if(addresses['lat'][x] == addresses['shift'][x]):
            addresses['lat'][x]  = tmp_lat
            addresses['long'][x] = tmp_long
        else:
            addresses['lat'][x]  = 0.0
            addresses['long'][x] = 0.0  
            print("Unexpected error occurred.", e )
    
    tmp_lat = addresses['lat'][x]
    tmp_long = addresses['long'][x]
    if (x%20==0):
        addresses[:x].to_csv("landslide_datas.csv", index=False, sep = ',')

addresses.head()
addresses.to_csv("landslide_datas.csv", index=False, sep = ',')




data = pd.read_csv('landslide_datas.csv')
df = pd.read_csv('address_datas.csv')
# drop function which is used in removing or deleting rows or columns from the CSV files
data.drop('shift', inplace=True, axis=1)
data['AlertLevel'] = df['AlertLevel']
data.to_csv("landslide_datas.csv", index=False, sep = ',')





