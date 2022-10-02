from distutils.log import error
from gc import collect
import csv
import time
from googlemaps import Client as GoogleMaps

#1. use your api key
api_key='AIzaSyAjVYl_ou5Q27gANjD3iuR6U5mFfM_g8ow'
googleMap = GoogleMaps(api_key)

#2. import your address file
with open('Bridge_information_address.csv',encoding="utf-8") as addressFile:
    addressList = csv.reader(addressFile)

    #3. create new file to write latitude and longitude
    convertAddress_file = open('Bridge_information_gps.csv', 'w')
    writer = csv.writer(convertAddress_file)

    #4. convert your address to latitude and longitude
    for row in addressList:
        convertAddressStore=[]
        addressInfo = googleMap.geocode(str(row[0]))

        #5. find latitude and longtitude 
        try:
            print(addressInfo)
            lat=str(addressInfo[0]['geometry']['location']['lat'])
            lon=str(addressInfo[0]['geometry']['location']['lng'])
            
            convertAddressStore.append(str(row))
            convertAddressStore.append(lat)
            convertAddressStore.append(lon)
            writer.writerow(convertAddressStore)
            print(convertAddressStore)
            
        except:
            print("not find")
        time.sleep(1)

#6. close file
convertAddress_file.close()
addressFile.close()
