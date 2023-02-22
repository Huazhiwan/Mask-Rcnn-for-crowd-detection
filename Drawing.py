import cv2
import numpy as np
import json
from global_read import video_name,img_flag 
from json import dumps
import os, sys
import tkinter as tk


#檔案開啟
path = './virtual fence'
if not os.path.isdir(path):
    os.mkdir(path)
path = './virtual fence/jsonfile'
if not os.path.isdir(path):
    os.mkdir(path)

#格式設定
picture_path = video_name
if img_flag == 2:#直接使用圖片
    for filename in os.listdir(picture_path):
        img = cv2.imread(picture_path+"\\"+filename)
        if cv2.waitKey(1):
            cv2.imwrite('./virtual fence/first_output.png', img)
            break
    #quit()
else :
    cap = cv2.VideoCapture(video_name) 
    retval = cv2.VideoCapture.isOpened(cap)
    if retval == False:
        messagebox.showerror('Error', 'not exist monitor')
        quit()   
    while True:
        ret, frame = cap.read()
        if cv2.waitKey(1):
            cv2.imwrite('./virtual fence/first_output.png', frame)
            break
    cap.release()
    cv2.destroyAllWindows()





#'D:\\virtual fence\\first_output.png'
# draw picture and get row and col
img = cv2.imread("./virtual fence/first_output.png")
sp = img.shape
x = sp[0]  # 480
y = sp[1]  # 640
cor = []


#規劃虛擬圍籬
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        global cor
        cor.append(x)
        cor.append(y)
        cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=-1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 255), thickness=1)
        cv2.imshow("image", img)


cv2.namedWindow("image")
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
cv2.imshow("image", img)

while(True):
    if cv2.waitKey(0) == ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()

# create the white picture
white_pic = np.zeros((x, y, 3), dtype=np.uint8)
white_pic.fill(255)
cv2.imwrite('./virtual fence/output.png', white_pic)


img = cv2.imread('./virtual fence/output.png')
for i in range(0, len(cor)-2, 2):
    cv2.line(img, (cor[i], cor[i+1]), (cor[i+2], cor[i+3]), (0, 0, 255), 6)
cv2.line(img, (cor[0], cor[1]), (cor[-2], cor[-1]), (0, 0, 255), 6)

'''
#to transparent white color
img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)         # 轉換顏色為 BGRA
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)        # 新增 gray 變數為轉換成灰階的圖片

h = img.shape[0]     # 取得圖片高度
w = img.shape[1]     # 取得圖片寬度

# 依序取出圖片中每個像素
for x in range(w):
    for y in range(h):
        if gray[y, x] > 200:
            img[y, x, 3] = 255 - gray[y, x]
            # 如果該像素的灰階度大於 200，調整該像素的透明度
            # 使用 255 - gray[y, x] 可以將一些邊緣的像素變成半透明，避免太過鋸齒的邊緣
'''
   
cv2.imwrite('./virtual fence/overlapping.png', img)     # 存檔儲存為 png
overlapping = cv2.imread('./virtual fence/overlapping.png')

# GUI to enter name
root = tk.Tk()
root.title('JSON FILE NAME')
root.geometry('300x50')
# name fuc


def get_name():
    global n
    flag = 1
    n = entry_1.get()
    if n == '':  # entry not space
        flag = 0

    if flag == 1:
        root.destroy()


# comform
button_1 = tk.Button(root, text='確定', relief="ridge", command=get_name)
# name
label_1 = tk.Label(root, text="名稱：")
# enter entry
entry_1 = tk.Entry(root, bd='3')
# show on GUI
label_1.pack(side='left', padx='10')
entry_1.pack(side='left', padx='5')
button_1.pack(side='right', padx='20')

root.mainloop()


#建立Json、txt檔
JSON_NAME_n = n
txtname = JSON_NAME_n
IMAGE_NAME = 'overlapping.png'
img_list = overlapping.tolist()
img_dict = {}
img_dict['name'] = IMAGE_NAME
img_dict['content'] = img_list


json_data = dumps(img_dict, indent=2)
with open(path+'/'+JSON_NAME_n+'.json', 'w') as json_file:
    json_file.write(json_data)
    
with open(path+'/'+txtname+'.txt', 'w') as f:
    for i in range(0, len(cor), 1):
        f.write(str(cor[i]))
        f.write('\n')