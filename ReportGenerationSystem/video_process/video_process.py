import cv2

# file=open('RX0.txt')    
# sensorDataList=[]  
# for line in file.readlines():    
#     curLine=line.strip().split(",")    
#     sensorDataList.append(curLine) 

video_path = "./1.avi"
cap = cv2.VideoCapture(video_path)
c = 1
timeRate = 1 #間隔秒數

timeRate_cut = 2


start_index=780
start_index_1=0

image_index=0
count=0

error_retry_cnt=0
'''
while(True):
    ret, frame = cap.read()
    FPS = cap.get(5)
    if ret:
        frameRate = int(FPS) * timeRate
        frameRate=int(frameRate/2)
        #print(frameRate)
        if(c % frameRate == 0):
            if(count>=start_index and count%timeRate_cut==0):
                print("開始擷取：" + str(c) + "幀")
                frame=cv2.rotate(frame,cv2.ROTATE_180)
                cv2.imwrite("/home/mmdb/Desktop/bridge/bridge/output/" + str(image_index) + '.jpg', frame)
                image_index+=1
            count+=1
            print(count)
        c += 1
    else:
        print("success")
        break
       
cap.release()
'''

video_path = "./4.mp4"
cap = cv2.VideoCapture(video_path)

count=0
image_index=322
while(True):
    ret, frame = cap.read()
    FPS = cap.get(5)
    if ret:
        frameRate = int(FPS) * timeRate
        #print(c)
        if(c % frameRate == 0):
            if(count>=start_index_1 and count%timeRate_cut==0):
                print("開始擷取：" + str(c) + "幀")
                #frame=cv2.rotate(frame,cv2.ROTATE_180)
                cv2.imwrite("/home/mmdb/Desktop/bridge/bridge/output/" + str(image_index) + '.jpg', frame)
                image_index+=1
            count+=1
            print(count)
        c += 1
    else:
        print("success")
        break
cap.release()

import sys
import os
import random
data_base_dir = "/home/mmdb/Desktop/bridge/bridge/output/" 
file_list = []
write_file_name = '/home/mmdb/Desktop/bridge/bridge/output.txt' 
write_file = open(write_file_name, "w") 
for file in os.listdir(data_base_dir): 
    if file.endswith(".jpg"):
        write_name = file
        file_list.append('/home/mmdb/Desktop/bridge/bridge/output/'+write_name)
        sorted(file_list) 
        number_of_lines = len(file_list) 
    if file.endswith(".png"):
        write_name = file
        file_list.append('/home/mmdb/Desktop/bridge/bridge/output/'+write_name)
        sorted(file_list) 
        number_of_lines = len(file_list)
for current_line in range(number_of_lines): 
    write_file.write(file_list[current_line] + '\n') 
write_file.close()




'''
while(True):
    ret, frame = cap.read()
    print("read")
    FPS = cap.get(5)
    if ret:
        frameRate = int(FPS) * timeRate
        frameRate=int(frameRate)
        print(c)
        if(c % frameRate == 0):
            print("開始擷取：" + str(c) + "幀")
            cv2.imwrite("./output/" + str(image_index) + '.jpg', frame)
            image_index+=1
        else:
            print("not")    
        c += 1
        #cv2.waitKey(0)
    else:
        print("success")
        break
cap.release()
'''
