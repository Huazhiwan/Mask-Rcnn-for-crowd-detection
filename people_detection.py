#影像處理
import cv2
import tkinter as tk
import numpy as np
from visualize  import model, display_instances, class_names#用於辨識
from Init_fence import zone,fence,video_name,check_point#虛擬圍籬、圍籬座標、檔案路徑、決定辨識目標
import os
import matplotlib.pyplot
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
import time

ROOT_DIR = os.getcwd()

def line_chart(y1,y2,flag):#即時折線圖(總人數、圍籬內人數)
    global people_max#最高人數
    global date,max_time#日期、最高人數的時間
    if(flag == True):#若是第一次繪製，則必須創建圖表
        plt.ion()
        fig = plt.figure(1) 
    if(len(x_list)>20):#若資料超過20筆，則刪除第一筆
        del x_list[0]
        del y1_list[0]
        del y2_list[0]
    local_time = time.localtime()
    current_time = time.strftime("%H:%M:%S",local_time)#獲得目前時間
    if(y1> people_max):#若當前人數超過目前最高人數，則取代
        people_max = y1
        max_time = current_time       
    x_list.append(current_time)
    y1_list.append(y1)
    y2_list.append(y2)
    
    output_time = time.strftime("%M:%S",local_time)#用於(全部時間)折線圖
    output_x.append(output_time)
    output_y1.append(y1)
    output_y2.append(y2)
    
    plt.xticks(rotation=45, ha="right", rotation_mode="anchor")#X軸文字往右選轉45度
    plt.ylim(0,50)#設定範圍
    plt.xlim(0,19)
    plt.title("Crowd monitoring")#標題名
    plt.title(date,loc = "right",color = 'green')#日期
    plt.text(0,48,'Max number of people:'+str(people_max),color = 'blue')
    plt.text(0,45,'Number of people'+str(y1),color = 'black')
    plt.text(0,42,'People in fence:'+str(y2),color = 'orange')
    plt.text(13,48,'——',color = 'c')
    plt.text(13,45,'——',color = 'r')
    plt.ylabel("Number of people")
    plt.plot(x_list, y1_list,c='c',ls='-')
    plt.plot(x_list, y2_list,c='r',ls='-')
    plt.show()
    plt.pause(1)
    plt.cla()   #清除目前座標

picture_path='' 
if(check_point != 2):#0鏡頭 1影片 2圖片資料夾
    capture = cv2.VideoCapture(video_name) #捕捉影片檔或鏡頭
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    size = (width,height) #得到寬與高用於錄製結果
    codec = cv2.VideoWriter_fourcc(*'XVID')#使用XVID編碼
    output = cv2.VideoWriter('./result/result.mp4', codec,30.0, size)#以FPS30錄製
else:
    picture_path = video_name
    first_img=cv2.imread('./virtual fence/first_output.png')
    #width = sp[0]  # 480
    #height = sp[1]  # 640
    size = first_img.shape
'''
D:\virtual fence
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (width,height) 
codec = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter('webcam.mp4', codec,30.0, size)
'''
#折線圖初始化
x_list = []         #時間
y1_list = []        #總人數
y2_list = []        #圍籬內人數

output_x = []       #用於結果輸出   
output_y1 = []
output_y2 = []

people_max = 0      #最高人數
date = time.localtime()#本地時間(秒)
date = time.strftime("%Y/%m/%d",date)#今天日期
start_time = time.localtime()
start_time = time.strftime("%H:%M:%S",start_time)#開始時間
max_time = start_time
line_flag =True #是否為第一次繪製折線圖


if check_point != 2:#影片或鏡頭
    try:      
        while(capture.isOpened()):
            ret, frame = capture.read()#ret表示是否有frame進來，frame則為當前獲取的影像
            people_count = 0#總人數
            people_fence = 0#圍籬內的人數
            if ret:
                # add mask to frame
                results = model.detect([frame], verbose=0)
                r = results[0]
                (people_count,people_fence,frame) = display_instances(
                    frame, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'],fence
                )#將frame、fence丟入進行判斷        
                line_chart(people_count,people_fence,line_flag)#判斷完繪製折線圖
                line_flag = False#繪製過折線圖，轉為flase
                frame = cv2.addWeighted(frame, 1, zone, 0.2, 0)#將虛擬圍籬與判斷完的畫面結合
                output.write(frame)#將frame寫入之後要儲存的影片檔
                
                cv2.imshow('frame', frame)#show出目前結果
                cv2.waitKey(3)
            else:
                break
    except KeyboardInterrupt:#ctrl-c 結束
        pass
    capture.release()
    output.release()
else:                       #使用圖片資料夾
    try: 
        for filename in os.listdir(picture_path):
            people_count = 0
            people_fence = 0
            # get pic info
            
            frame = cv2.imread(picture_path+"\\"+filename)
            if frame is not None:
                results = model.detect([frame], verbose=0)
                r = results[0]
                (people_count,people_fence,frame) = display_instances(
                    frame, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'],fence
                )        
                
                frame = cv2.addWeighted(frame, 1, zone, 0.2, 0)
                cv2.namedWindow("image")
                cv2.imshow("image", frame)
                line_chart(people_count,people_fence,line_flag)
                
                
                line_flag = False
                # late pic speed
                cv2.waitKey(3)
            else:
                break
    except KeyboardInterrupt:
        pass
    
    
    

cv2.destroyAllWindows() #結束視窗
plt.close()
#(全部時間)折線圖結果輸出
end_time = time.localtime()#結束時間
end_time = time.strftime("%H:%M:%S",end_time)
line_output = plt.figure(figsize=(10,10))#建立折線圖
plt.title("Crowd monitoring")#標題名
plt.title(date,loc = "right",color = 'green')#日期
plt.title("start:"+start_time+'\n'+"end:"+end_time,loc = "left")#開始時間
plt.xticks(rotation=45, ha="right", rotation_mode="anchor")
plt.ylim(0,50)#y軸最大50
plt.text(0,48,'Max people:'+str(people_max)+'('+max_time+')',color = 'blue')#紀錄最高人數
plt.plot(output_x,output_y1,c='c',ls='-',label = 'Number of people')#總人數
plt.plot(output_x,output_y2,c='red',ls='-',label = 'People in fence:')#圍籬內人數
plt.legend(loc='upper right', shadow=True)#標出折線用途
plt.gca().xaxis.set_ticklabels([])#隱藏X軸座標
line_output.savefig('./results/line_chart_result.png')#儲存折線圖
plt.close()


    