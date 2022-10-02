# import cv2
# import numpy as np
 

# def save_image(image,addr,num):
#     address = addr + str(num)+ '.jpg'
#     cv2.imwrite(address,image)
 
# videoCapture = cv2.VideoCapture("C0005.MP4")
# # videoCapture=cv2.VideoCapture(1)
 

# success, frame = videoCapture.read()
# i = 0
# while success:
#     i = i + 1
#     save_image(frame,'./output/image',i)
#     if success:
#         print('save image:',i)
#     success, frame = videoCapture.read()



# import cv2

# def save_image(image,addr,num):
#     address = addr + str(num)+ '.jpg'
#     cv2.imwrite(address,image)


# video_path = "./RX0.MP4"
# capture = cv2.VideoCapture(video_path)
# fps = capture.get(cv2.CAP_PROP_FPS)
# total_frame = capture.get(cv2.CAP_PROP_FRAME_COUNT)

# for i in range(int(total_frame)):
# 	ret = capture.grab()
# 	if not ret:
# 		print("Error grabbing frame from movie!")
# 		break
# 	if i % fps == 0:
# 	    ret, frame = capture.retrieve()
# 	    if ret:
#             address="fkopewkpoe"
#             address=("%s%s%s" % address,str(i),".JPG")
#             # address = addr + str(i)+ '.jpg'
#     #         cv2.imwrite(address,frame)
#     #         # save_image(frame,'./output/',i)
# 	# 	else:
# 	# 		print("Error retrieving frame from movie!")
# 	# 		break
# cv2.waitKey(-1)


# import cv2

# def save_image(image,addr,num):
#     address = addr + str(num)+ '.jpg'
#     print(address)
#     cv2.imwrite(address,image)


# video_path = "./RX0.MP4"
# capture = cv2.VideoCapture(video_path)
# fps = capture.get(cv2.CAP_PROP_FPS)
# total_frame = capture.get(cv2.CAP_PROP_FRAME_COUNT)
# print(fps)
# aaa
# for i in range(int(total_frame)):
#     ret = capture.grab()
#     if not ret:
#         print("Error grabbing frame from movie!")
#         break
#     if i % fps == 0:
#         ret, frame = capture.retrieve()
#         if ret:
#             save_image(frame,'./output/',i)
#         else:
#             print("Error retrieving frame from movie!")
#             break
# cv2.waitKey(-1)

# import cv2

# video_path = "./RX0.MP4"
# cap = cv2.VideoCapture(video_path)
# c = 1
# timeRate = 1 #間隔秒數
 

# image_index=0

# while(True):
# 	ret, frame = cap.read()
# 	FPS = cap.get(5)
# 	if ret:
# 		frameRate = int(FPS) * timeRate
# 		if(c % frameRate == 0):
# 			print("開始擷取：" + str(c) + "幀")
# 			cv2.imwrite("./output/" + str(image_index) + '.JPG', frame)
#             image_index+=1
# 		c += 1
# 		cv2.waitKey(0)
# 	else:
# 		print("success")
# 		break
# cap.release()


import cv2

# file=open('RX0.txt')    
# sensorDataList=[]  
# for line in file.readlines():    
#     curLine=line.strip().split(",")    
#     sensorDataList.append(curLine) 

video_path = "./RX0.MP4"
cap = cv2.VideoCapture(video_path)
c = 1
timeRate = 1 #間隔秒數

start_index=60

image_index=0
count=0

while(True):
    ret, frame = cap.read()
    FPS = cap.get(5)
    if ret:
        frameRate = int(FPS) * timeRate
        if(c % frameRate == 0):
            if(count>=start_index):
                print("開始擷取：" + str(c) + "幀")
                cv2.imwrite("./output/" + str(image_index) + '.jpg', frame)
                image_index+=1
            count+=1
        c += 1
        cv2.waitKey(0)
    else:
        print("success")
        break
cap.release()