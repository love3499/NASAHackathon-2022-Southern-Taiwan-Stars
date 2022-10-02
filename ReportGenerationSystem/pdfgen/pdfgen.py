from reportlab.lib.pagesizes import letter ,landscape
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont 

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph, SimpleDocTemplate, PageBreak, CondPageBreak,Table, TableStyle,Image
import os

###
from reportlab.lib.styles import StyleSheet1, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors

import numpy as np

stylesheet = StyleSheet1()

pdfmetrics.registerFont(TTFont('Chinese', 'TaipeiSansTCBeta-Regular.ttf')) 
pdfmetrics.registerFont(TTFont('Bold', 'TaipeiSansTCBeta-Bold.ttf')) 
pdfmetrics.registerFont(TTFont('Light', 'TaipeiSansTCBeta-Light.ttf')) 

stylesheet.add(ParagraphStyle(name='Normal',
                                fontName='Chinese',
                                fontSize=16,
                                leading=12,
                                spaceBefore=6)
                )

stylesheet.add(ParagraphStyle(name='Comment',
                                fontName='Chinese')
                )

stylesheet.add(ParagraphStyle(name='Indent0',
                                leftIndent=18,
                                fontName='Chinese')
                )

stylesheet.add(ParagraphStyle(name='Indent1',
                                leftIndent=36,
                                firstLineIndent=0,
                                spaceBefore=1,
                                spaceAfter=7,
                                fontName='Chinese')
                )

stylesheet.add(ParagraphStyle(name='Indent2',
                                leftIndent=50,
                                firstLineIndent=0,
                                spaceAfter=100,
                                fontName='Chinese')
                )

stylesheet.add(ParagraphStyle(name='BodyText',
                                parent=stylesheet['Normal'],
                                spaceBefore=6,
                                fontName='Chinese')
                )
stylesheet.add(ParagraphStyle(name='Italic',
                                parent=stylesheet['BodyText'],
                                fontName = 'Chinese')
                )

stylesheet.add(ParagraphStyle(name='Heading1',
                                parent=stylesheet['Normal'],
                                fontName = 'Chinese',
                                alignment=1,
                                fontSize=24,
                                leading=22,
                                spaceAfter=6),
                alias='h1')

stylesheet.add(ParagraphStyle(name='Heading2',
                                parent=stylesheet['Normal'],
                                fontName='Chinese',
                                fontSize=20,
                                leading=17,
                                spaceBefore=12,
                                spaceAfter=6),
                alias='h2')

stylesheet.add(ParagraphStyle(name='Heading3',
                                parent=stylesheet['Normal'],
                                fontName='Chinese',
                                fontSize=18,
                                leading=14,
                                spaceBefore=12,
                                spaceAfter=6),
                alias='h3')

stylesheet.add(ParagraphStyle(name='Heading4',
                                parent=stylesheet['Normal'],
                                fontName='Chinese',
                                spaceBefore=10,
                                spaceAfter=4),
                alias='h4')
                

stylesheet.add(ParagraphStyle(name='Title',
                                parent=stylesheet['Normal'],
                                fontName='Bold',
                                fontSize=38,
                                leading=40,
                                spaceAfter=36,
                                alignment=TA_CENTER
                                ),
                alias='t')

stylesheet.add(ParagraphStyle(name='Subtitle',
                                parent=stylesheet['Normal'],
                                fontSize=20,
                                alignment=TA_CENTER,
                                fontName='Light'
                                ))

stylesheet.add(ParagraphStyle(name='Bullet',
                                parent=stylesheet['Normal'],
                                firstLineIndent=0,
                                leftIndent=54,
                                bulletIndent=18,
                                spaceBefore=0,
                                fontName='Bold',
                                bulletFontName='Symbol'),
                alias='bu')

stylesheet.add(ParagraphStyle(name='Definition',
                                parent=stylesheet['Normal'],
                                firstLineIndent=0,
                                leftIndent=36,
                                bulletIndent=0,
                                spaceBefore=6,
                                fontName='Bold',
                                bulletFontName='Times-BoldItalic'),
                alias='df')

stylesheet.add(ParagraphStyle(name='Code',
                                parent=stylesheet['Normal'],
                                fontName='Chinese',
                                fontSize=14,
                                leading=8.8,
                                leftIndent=36,
                                firstLineIndent=0,
                                hyphenationLang=''))

stylesheet.add(ParagraphStyle(name='Link',
                                parent=stylesheet['Code'],
                                spaceAfter=7,
                                spaceBefore=0,
                                fontName='Bold',
                                leftIndent=55))

stylesheet.add(ParagraphStyle(name='FunctionHeader',
                                parent=stylesheet['Normal'],
                                fontName='Chinese',
                                fontSize=14,
                                leading=8.8))

stylesheet.add(ParagraphStyle(name='DocString',
                                parent=stylesheet['Normal'],
                                fontName='Chinese',
                                fontSize=14,
                                leftIndent=18,
                                leading=8.8))

stylesheet.add(ParagraphStyle(name='DocStringIndent',
                                parent=stylesheet['Normal'],
                                fontName='Chinese',
                                fontSize=14,
                                leftIndent=36,
                                leading=8.8))

stylesheet.add(ParagraphStyle(name='URL',
                                parent=stylesheet['Normal'],
                                fontName='Chinese',
                                textColor=colors.navy,
                                alignment=TA_CENTER),
                alias='u')

stylesheet.add(ParagraphStyle(name='Centred',
                                parent=stylesheet['Normal'],
                                alignment=TA_CENTER,
                                fontName='Chinese'
                                ))

stylesheet.add(ParagraphStyle(name='Caption',
                                parent=stylesheet['Centred'],
                                fontName='Chinese'
                                ))
stylesheet.add(ParagraphStyle(name='Subtitle_yi',
                                parent=stylesheet['Normal'],
                                fontSize=20,
                                alignment=TA_CENTER,
                                fontName='Light'
                                ))
H1 = stylesheet['Heading1']
H2 = stylesheet['Heading2']
H3 = stylesheet['Heading3']
H4 = stylesheet['Heading4']
Subtitle_yi = stylesheet['Subtitle_yi']

B = stylesheet['BodyText']
BU = stylesheet['Bullet']
Comment = stylesheet['Comment']
Centred = stylesheet['Centred']
Caption = stylesheet['Caption']


pdfmetrics.registerFont(TTFont('Sans', 'TaipeiSansTCBeta-Regular.ttf')) 

text=[]
text.append(Paragraph("橋梁檢測報表",stylesheet['Title']))
text.append(Paragraph("臺灣希望創新團隊",stylesheet['Subtitle']))



text.append(PageBreak())
text.append(Paragraph("<br/>",stylesheet['Title']))
text.append(Paragraph("<br/>",stylesheet['Title']))
text.append(Paragraph("<br/>",stylesheet['Title']))
text.append(Paragraph("<br/>",stylesheet['Title']))
text.append(Paragraph("<br/>",stylesheet['Title']))
text.append(Paragraph("<br/>",stylesheet['Title']))
text.append(Paragraph("<br/>",stylesheet['Title']))
text.append(Paragraph("<br/>",stylesheet['Title']))
text.append(Paragraph("<br/>",stylesheet['Title']))
text.append(Paragraph("<br/>",stylesheet['Title']))
text.append(Paragraph("<br/>",stylesheet['Title']))
text.append(Paragraph("<br/>",stylesheet['Title']))
text.append(Paragraph("橋樑指定部位影像拍攝",stylesheet['Heading1']))
text.append(PageBreak())

# text.append(PageBreak())
# reason="剪力"

# test_object="橋墩墩體"
# position="P4"
# serial_num="P4"
# PD="3"
# PE="2"
# PR="3"
# PU="3"
# broken_pos="墩體"
# kind="混凝土裂縫"
# reason="剪力"

# solution="裂縫修補"
# num=20
# num_unit="公尺"
# others="0.4MM*1M"
# date="2010/10/10"


test_object=""
position=""
serial_num=""
PD=""
PE=""
PR=""
PU=""
broken_pos=""
kind=""
reason=""

solution=""
num=0
num_unit=""
others=""
date="2010/10/10"


resizeMultiple=5.5
resizeMultiple_1=5

image_screen_place_str_list=['蝴蝶橋全貌','梁下螺栓','橋墩帽樑下方','同一個支承2個面(之一)','同一個支承2個面(之二)','P21記號','梁下細部構件(之一)','梁下細部構件(之二)','梁下細部構件(之三)','P22記號']
image_detect_place_str_list=['梁下螺栓','橋墩墩柱','支承','P21記號','梁下細部構件','鋼骨結構鏽蝕污漬','橋墩柱鏽蝕污漬','兩條大樑、小梁']
########################################### 讀取感測器資料 ####################################################################
file=open('1.txt')    
readRate=2
readCnt=0
sensorDataList=[]  
for line in file.readlines():    
	if(readCnt%readRate==0):
		curLine=line.strip().split(",")    
		sensorDataList.append(curLine)
	readCnt+=1
print("sensorDataList=%d",len(sensorDataList))    
############################################################################################################################

image_load_path_0='./指定影像拍攝/'
# 讀取指定拍攝影像  0-9 資料夾 每個資料夾 4 張  
for _,img_dirs_0,_ in os.walk(image_load_path_0):
    break
img_dirs_0.sort()
print(img_dirs_0)

img_total_list_0 = []

sensorDataList_empty=['0','0','0','0','0','0','0','0','0']
for img_dir in img_dirs_0 :
    img_item_path = image_load_path_0 + ("%s/" % img_dir)
    print(img_item_path)
    for _,_,files in os.walk(img_item_path):
        break
    files.sort()
    # print(files)
    image_list=[]
    for file in files:
        if 'jpg' in file or 'png' in file or 'JPG' in file:
            data_dict = {}
            # print("%s%s" % (img_item_path,file))
            img_path=("%s%s" % (img_item_path,file))
            data_dict['img_path']=img_path
            sensorData_index=int(file.split('.')[0])
            # print(sensorData_index)
            if(len(sensorDataList)>=sensorData_index):
               data_dict['sensor_data']=sensorDataList[sensorData_index]
            else:
               data_dict['sensor_data']=sensorDataList_empty
		       
            #data_dict['sensor_data']=sensorDataList[sensorData_index]
           
            # print(data_dict['img_path'])
            # print(data_dict['sensor_data'])
            # print(data_dict)
            image_list.append(data_dict)
            # print(image_list)
    # print("\r\n")             
    img_total_list_0.append(image_list)



# sensor_data  0 時間戳   1,2 飛機GPS 3  飛機拍攝高度 4 航向角 5 深度 6 7 目標位置(經緯度) 8 UNIX時間
for i in range(10):
    # 生成表格 每張圖片生成一個表格
    table_num=len(img_total_list_0[i])
    text.append(Paragraph(image_screen_place_str_list[i],stylesheet['Subtitle_yi']))
    if(i==6):
        resizeMultiple=2
    else:
        resizeMultiple=5.5

    if(table_num==0):
        text.append(PageBreak())
    else:
        text.append(Paragraph("<br/>",stylesheet['Title']))

    for table_index in range(0,table_num):
        image_data=img_total_list_0[i][table_index]['img_path']
        sensor_data=img_total_list_0[i][table_index]['sensor_data']
        # print(image_data)
        # print(sensor_data)

        image1 = Image(image_data)
        image1.drawHeight = resizeMultiple*inch*image1.drawHeight / image1.drawWidth
        image1.drawWidth = resizeMultiple*inch
        data=[
            ['檢測項目','位置描述','無人機GPS座標','D','E','R','U','損壞位置','','劣質類型','損壞原因'],
            [image_screen_place_str_list[i],sensor_data[1]+','+sensor_data[2],sensor_data[6]+','+sensor_data[7],PD,PE,PR,PU,broken_pos,'',kind,reason],
            ['建議維修工法','','','','','','','損耗''/單位','面積','備註'],
            [solution,'','','','','','',num,num_unit,others],
            ['檢測照片',image1],
            # ['檢測照片',image1,'','',image2,'','',image3,'','',''],
            ['拍攝日期','','','','','','','','','',''],
            [sensor_data[0],'','','','','','','','','','']
        ]
        t = Table(data, style=[('GRID', (0, 0), (-1, -1), 1, colors.black),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                       ('FONTNAME', (0,0), (-1,0), 'Bold'),
                       ('FONTNAME', (0,1), (-1,1), 'Chinese'),
                       ('BACKGROUND', (0, 2), (-1, 2), colors.lightgrey),
                       ('FONTNAME', (0,2), (-1,2), 'Bold'),
                       ('FONTNAME', (0,3), (-1,3), 'Chinese'),
                       ('BACKGROUND', (0, 4), (0, 5), colors.lightgrey),
                       ('FONTNAME', (0,4), (0,5), 'Bold'),
                       ('FONTNAME', (1,4), (-1,-1), 'Chinese'),
                       ('FONTNAME', (0,-1), (0,-1), 'Chinese'),
                        ('SPAN',(0,2),(6,2)),
                        ('SPAN',(7,0),(8,0)),
                        ('SPAN',(7,1),(8,1)),
                        ('SPAN',(9,2),(10,2)),
                        ('SPAN',(9,3),(10,3)),
                        ('SPAN',(0,3),(6,3)),
                        ('SPAN',(1,4),(-1,-1)),
                        # ('SPAN',(4,4),(-1,-1)),
                        # ('SPAN',(7,4),(-1,-1))
                       ])
        text.append(t)
        text.append(PageBreak())

text.append(Paragraph("橋樑指定部位影像辨識",stylesheet['Heading1']))
text.append(PageBreak())

image_load_path_1='./指定部位辨識/'
# 讀取指定拍攝影像  0-9 資料夾 每個資料夾 4 張  
for _,img_dirs_1,_ in os.walk(image_load_path_1):
    break
img_dirs_1.sort()
img_total_list_1 = []
print(img_dirs_1)


for img_dir in img_dirs_1 :
    img_item_path = image_load_path_1 + ("%s/" % img_dir)
    # print(img_item_path)
    for _,_,files in os.walk(img_item_path):
        break
    files.sort()
    # print(files)
    image_list=[]
    for file in files:
        if 'jpg' in file or 'png' in file or 'JPG' in file:
            data_dict = {}
            # print("%s%s" % (img_item_path,file))
            img_path=("%s%s" % (img_item_path,file))
            data_dict['img_path']=img_path
            sensorData_index=int(file.split('_')[0])
            # print(sensorData_index)
            if(len(sensorDataList)>=sensorData_index):
               data_dict['sensor_data']=sensorDataList[sensorData_index]
            else:
               data_dict['sensor_data']=sensorDataList_empty
            #data_dict['sensor_data']=sensorDataList[sensorData_index]
            # print(data_dict['img_path'])
            # print(data_dict['sensor_data'])
            # print(data_dict)
            image_list.append(data_dict)
            # print(image_list)
    # print(image_list)   
    # print("\r\n")             
    img_total_list_1.append(image_list)

for i in range(8):
    solution=''
    if(i==5 or i==6):
        reason="風吹日曬雨淋"
        solution='建議清潔'
        if(i==5):
            broken_pos="橋梁鋼骨"
        else:
            broken_pos="橋墩"

    # 生成表格 每張圖片生成一個表格
    table_num=len(img_total_list_1[i])
    text.append(Paragraph(image_detect_place_str_list[i],stylesheet['Subtitle_yi']))
    if(table_num==0):
        text.append(PageBreak())
    else:
        text.append(Paragraph("<br/>",stylesheet['Title']))
    
    for table_index in range(0,table_num):
        image_data=img_total_list_1[i][table_index]['img_path']
        sensor_data=img_total_list_1[i][table_index]['sensor_data']
        # print(image_data)
        # print(sensor_data)

        image1 = Image(image_data)
        image1.drawHeight = resizeMultiple_1*inch*image1.drawHeight / image1.drawWidth
        image1.drawWidth = resizeMultiple_1*inch
        data=[
            ['檢測項目','位置描述','無人機GPS座標','D','E','R','U','損壞位置','','劣質類型','損壞原因'],
            [image_detect_place_str_list[i],sensor_data[1]+','+sensor_data[2],sensor_data[6]+','+sensor_data[7],PD,PE,PR,PU,broken_pos,'',kind,reason],
            ['建議維修工法','','','','','','','數量''單位','單價','備註'],
            [solution,'','','','','','',num,num_unit,others],
            ['檢測照片',image1],
            # ['檢測照片',image1,'','',image2,'','',image3,'','',''],
            ['拍攝日期','','','','','','','','','',''],
            [sensor_data[0],'','','','','','','','','','']
        ]
        t = Table(data, style=[('GRID', (0, 0), (-1, -1), 1, colors.black),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                       ('FONTNAME', (0,0), (-1,0), 'Bold'),
                       ('FONTNAME', (0,1), (-1,1), 'Chinese'),
                       ('BACKGROUND', (0, 2), (-1, 2), colors.lightgrey),
                       ('FONTNAME', (0,2), (-1,2), 'Bold'),
                       ('FONTNAME', (0,3), (-1,3), 'Chinese'),
                       ('BACKGROUND', (0, 4), (0, 5), colors.lightgrey),
                       ('FONTNAME', (0,4), (0,5), 'Bold'),
                       ('FONTNAME', (1,4), (-1,-1), 'Chinese'),
                       ('FONTNAME', (0,-1), (0,-1), 'Chinese'),
                        ('SPAN',(0,2),(6,2)),
                        ('SPAN',(7,0),(8,0)),
                        ('SPAN',(7,1),(8,1)),
                        ('SPAN',(9,2),(10,2)),
                        ('SPAN',(9,3),(10,3)),
                        ('SPAN',(0,3),(6,3)),
                        ('SPAN',(1,4),(-1,-1)),
                        # ('SPAN',(4,4),(-1,-1)),
                        # ('SPAN',(7,4),(-1,-1))
                       ])
        text.append(t)
        text.append(PageBreak())

# print(img_total_list_0[5][3]['sensor_data'])

# def getImageData(image1_path,image2_path):
#     image1 = Image(image1_path)
#     image1.drawHeight = resizeMultiple*inch*image1.drawHeight / image1.drawWidth
#     image1.drawWidth = resizeMultiple*inch
#     if(image2_path != None):
#         image2 = Image(image2_path)
#         image2.drawHeight = resizeMultiple*inch*image2.drawHeight / image2.drawWidth
#         image2.drawWidth = resizeMultiple*inch
#         return image1,image2
#     else:
#         return image1

# def getSensorData(sensor_data_1,sensor_data_2):
#     if(sensor_data_2 != None):
#         return sensor_data_1,sensor_data_2
#     else:
#         return sensor_data_1

# for i in range(10):
#     is_odd=False
#     if(len(img_total_list_0[i])%2==0):
#         table_num=int(len(img_total_list_0[i])/2)
#     else:
#         is_odd=True
#         table_num=int(len(img_total_list_0[i])/2+1)
#     # print(table_num)
#     # 生成表格  次數為  圖片數量/2+1
#     table_num=len(img_total_list_0[i])
#     for table_index in range(0,table_num):
#         print("%d,%d",table_index*2+1,table_index*2+2)
#         if(table_index==table_num-1):
#             if(is_odd):
#                 image1,image2=getImageData(img_total_list_0[i][table_index*2+1]['img_path'],img_total_list_0[i][table_index*2+2]['img_path'])
#                 sensor_data_1,sensor_data_2=getSensorData
#             else:    
#                 image1=getImageData(img_total_list_0[i][table_index*2+1]['img_path'],None)
#         else:        
#             image1,image2=getImageData(img_total_list_0[i][table_index*2+1]['img_path'],img_total_list_0[i][table_index*2+2]['img_path'])



# aaaaaa





# for i in range(10):
#     # print(len(img_total_list_0[i]))
#     image_screen_place_dict = {}
#     image_total_screen_place_list=[]
#     for image_index in range(0,(len(img_total_list_0[i]))):
#         # print(img_total_list_0[i][image_index]['img_path'])
#         image_screen_place_dict['img_path']=img_total_list_0[i][image_index]['img_path']
#         image_screen_place_dict['sensor_data']=img_total_list_0[i][image_index]['sensor_data']

#         image_total_screen_place_list.append(image_screen_place_dict)
#         # image = Image(img_total_list_0[image_index]['img_path'])
#         # image.drawHeight = resizeMultiple*inch*image1.drawHeight / image1.drawWidth
#         # image.drawWidth = resizeMultiple*inch

        

# 每次讀取完顯示對應資料



# 讀取指定辨識部位  0-9 資料夾 每個資料夾 4 張  

# 每次讀取完顯示對應資料




# p = canvas.Canvas(response, pagesize=(landscape(letter)))



# image1 = Image('./n1.JPG')
# image1.drawHeight = resizeMultiple*inch*image1.drawHeight / image1.drawWidth
# image1.drawWidth = resizeMultiple*inch
# image2 = Image('./n1.JPG')
# image2.drawHeight = resizeMultiple*inch*image2.drawHeight / image2.drawWidth
# image2.drawWidth = resizeMultiple*inch
# image3 = Image('./n1.JPG')
# image3.drawHeight = resizeMultiple*inch*image3.drawHeight / image3.drawWidth
# image3.drawWidth = resizeMultiple*inch

# data=[
#     ['檢測項目','位置描述','無人機GPS座標','D','E','R','U','損壞位置','','劣質類型','損壞原因'],
#     [test_object,'無人機左前方(22.8915539,120.6393974)','22.8915539,120.6393974',PD,PE,PR,PU,broken_pos,'',kind,reason],
#     ['建議維修工法','','','','','','','數量''單位','單價','備註'],
#     [solution,'','','','','','',num,num_unit,others],
#     ['檢測照片',image1],
#     # ['檢測照片',image1,'','',image2,'','',image3,'','',''],
#     ['拍攝日期','','','','','','','','','',''],
#     [date,'','','','','','','','','','']
# ]
# t = Table(data, style=[('GRID', (0, 0), (-1, -1), 1, colors.black),
#                        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#                        ('FONTNAME', (0,0), (-1,0), 'Bold'),
#                        ('FONTNAME', (0,1), (-1,1), 'Chinese'),
#                        ('BACKGROUND', (0, 2), (-1, 2), colors.lightgrey),
#                        ('FONTNAME', (0,2), (-1,2), 'Bold'),
#                        ('FONTNAME', (0,3), (-1,3), 'Chinese'),
#                        ('BACKGROUND', (0, 4), (0, 5), colors.lightgrey),
#                        ('FONTNAME', (0,4), (0,5), 'Bold'),
#                        ('FONTNAME', (1,4), (-1,-1), 'Chinese'),
#                        ('FONTNAME', (0,-1), (0,-1), 'Chinese'),
#                         ('SPAN',(0,2),(6,2)),
#                         ('SPAN',(7,0),(8,0)),
#                         ('SPAN',(7,1),(8,1)),
#                         ('SPAN',(9,2),(10,2)),
#                         ('SPAN',(9,3),(10,3)),
#                         ('SPAN',(0,3),(6,3)),
#                         ('SPAN',(1,4),(-1,-1)),
#                         # ('SPAN',(4,4),(-1,-1)),
#                         # ('SPAN',(7,4),(-1,-1))
#                        ])
# text.append(Paragraph("<br/>",stylesheet['Title']))
# text.append(t)
# text.append(t)




# text.append(PageBreak())
# text.append(Paragraph("梁下螺栓",stylesheet['Heading1']))


# text.append(PageBreak())
# text.append(Paragraph("橋墩帽樑下方",stylesheet['Heading1']))

# text.append(PageBreak())
# text.append(Paragraph("同一支承2個面(之一)",stylesheet['Heading1']))

# text.append(PageBreak())
# text.append(Paragraph("同一支承2個面(之二)",stylesheet['Heading1']))

# text.append(PageBreak())
# text.append(Paragraph("P21記號",stylesheet['Heading1']))

# text.append(PageBreak())
# text.append(Paragraph("梁下細部構件(之一)",stylesheet['Heading1']))

# text.append(PageBreak())
# text.append(Paragraph("梁下細部構件(之二)",stylesheet['Heading1']))

# text.append(PageBreak())
# text.append(Paragraph("梁下細部構件(之三)",stylesheet['Heading1']))

# text.append(PageBreak())
# text.append(Paragraph("P22記號",stylesheet['Heading1']))

# text.append(PageBreak())
# text.append(Paragraph("橋樑指定部位影像辨識結果",stylesheet['Heading1']))

doc = SimpleDocTemplate('mydoc.pdf',pagesize=(15.7*inch,8.3*inch))
doc.build(text)



# 11*inch, 8.5*inch
