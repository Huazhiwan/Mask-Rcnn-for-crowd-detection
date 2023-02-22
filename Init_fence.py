import numpy as np
import json
import tkinter as tk
from json import dumps
from tkinter import filedialog
from global_read import g_read
def control_section(window,step_from,step):#決定UI可以切換的下一個步驟(從哪一步到哪一步)	
    global check_flag,check_point
    check_flag = var.get()
    window.destroy()                       #破壞目前子視窗	
    if(step == 0):
        decision_window.destroy()          #最後一步時，破壞主視窗
    elif(step == 1):
        first()
    elif(step == 2):
        if(step_from == 1): #第一步結束後將check_flag保存給point，以便之後給global_read以及主程式參考             
            check_point = check_flag     
        if(step_from == 3):#若從第三步返回第二步，則將原本暫存第一步的變數給第二步參考 
            check_flag = c_flag            
        second()
    else:
        third()
def file_select(text,C,n):#用於檔案選取
    global JSON_NAME,TXT_NAME, video_name
    if(n == 0):
        JSON_NAME = filedialog.askopenfilename()#得到JSON檔案路徑
        if(JSON_NAME != ''):
            text.config(text=str(JSON_NAME),bg = "#FAFAFA")
        else:
            text.config(text='尚未選擇檔案',bg = "#FAFAFA")
        if(JSON_NAME != '' and TXT_NAME != ''):#若兩者都不為空則可下一步
            C.configure(state = tk.ACTIVE)
        else:
            C.configure(state = tk.DISABLED)
    elif(n == 1):
        TXT_NAME = filedialog.askopenfilename()#得到TXT檔案路徑
        if(TXT_NAME != ''):
            text.config(text=str(TXT_NAME),bg = "#FAFAFA")
        else:
            text.config(text='尚未選擇檔案',bg = "#FAFAFA")
        if(JSON_NAME != '' and TXT_NAME != ''):#若兩者都不為空則可下一步
            C.configure(state = tk.ACTIVE)
        else:
            C.configure(state = tk.DISABLED)
    elif(n == 2):
        video_name = filedialog.askopenfilename()#得到影片檔路徑
        #print(video_name)
        
        text.config(text=str(video_name),bg = "#FAFAFA")
        if(video_name != ''):
            C.configure(state = tk.ACTIVE)
        else:
            text.config(text='尚未選取影片',bg = "#FAFAFA")
            C.configure(state = tk.DISABLED)
    elif(n == 3):
        video_name = filedialog.askdirectory()#獲得圖片資料夾路徑
        #print(video_name)
        text.config(text=str(video_name),bg = "#FAFAFA")#在UI上顯示路徑
        if(video_name != ''):#若不為空，則可按下一步
            C.configure(state = tk.ACTIVE)
        else:
            text.config(text='尚未選取資料夾',bg = "#FAFAFA")
            C.configure(state = tk.DISABLED)

JSON_NAME = ''  #虛擬圍籬
TXT_NAME = ''   #虛擬圍籬座標
video_name = '' #圖片資料夾或影片的檔案名稱
check_flag = 0  #0鏡頭 1影片 2圖片資料夾用來傳給check_point以及下一個步驟參考
check_point = 0 #傳值給主程式與global參考
c_flag = 0      #用來保存first section所選擇的值
#UI        
decision_window =tk.Tk()#建立主視窗
decision_window.title('校園人流監控:初始化設定')
decision_window.geometry('650x300')#主視窗尺寸
var = tk.IntVar()#按鈕變數存取
var.set(0)
def first():#選擇鏡頭、影片或圖片資料夾
    global var
    first_window = tk.Frame(decision_window,width = 600,height = 250)#建立第一步驟的子視窗
    first_window.pack()
    R1=tk.Radiobutton(first_window,text='讀取鏡頭',font=(10),variable=var,value=0)
    R2=tk.Radiobutton(first_window,text='讀取影片檔',font=(10),variable=var,value=1)
    R3=tk.Radiobutton(first_window,text='讀取圖片',font=(10),variable=var,value=2)
    C1=tk.Button(first_window,text='下一步',font=(10),command = lambda:control_section(first_window,1,2))
    R1.place(x = 20,y = 50)
    R2.place(x = 20,y = 100)
    R3.place(x = 20,y = 150)
    C1.place(x = 400,y = 200)    
def second():#選擇虛擬圍籬檔案或繪製虛擬圍籬
    global var,c_flag
    c_flag = check_flag #保存first section所選擇的值
    var = tk.IntVar()
    second_window = tk.Frame(decision_window,width = 600,height = 200)#建立第二步驟的子視窗
    second_window.pack()
    if(check_flag == 2):#使用圖片資料夾
        R1_text = tk.Label(second_window,text='尚未選取資料夾',bg = "#FAFAFA")
        R2=tk.Radiobutton(second_window,text='選擇虛擬圍籬檔案',font=(10),variable=var,value=0)
        R3=tk.Radiobutton(second_window,text='繪製虛擬圍籬',font=(10),variable=var,value=1)
        C1=tk.Button(second_window,text='下一步',state = tk.DISABLED,font=(10),command = lambda:control_section(second_window,2,3))
        C2=tk.Button(second_window,text='上一步',font=(10),command = lambda:control_section(second_window,2,1))
        R1=tk.Button(second_window,text = '檔案總管',command = lambda:file_select(R1_text,C1,3))
        R1.place(x = 20,y = 20,width = 70)
        R1_text.place(x = 120,y = 20,width = 400)
        R2.place(x = 20,y = 50)
        R3.place(x = 20,y = 100) 
        C1.place(x = 400,y = 160)
        C2.place(x = 100,y = 160)
    if(check_flag == 1):#使用影片檔
        R1_text = tk.Label(second_window,text='尚未選取影片',bg = "#FAFAFA")
        R2=tk.Radiobutton(second_window,text='選擇虛擬圍籬檔案',font=(10),variable=var,value=0)
        R3=tk.Radiobutton(second_window,text='繪製虛擬圍籬',font=(10),variable=var,value=1)
        C1=tk.Button(second_window,text='下一步',state = tk.DISABLED,font=(10),command = lambda:control_section(second_window,2,3))
        #DISABLED若未選取影片檔，則鎖住下一步
        C2=tk.Button(second_window,text='上一步',font=(10),command = lambda:control_section(second_window,2,1))
        R1=tk.Button(second_window,text = '檔案總管',command = lambda:file_select(R1_text,C1,2))
        R1.place(x = 20,y = 20,width = 70)
        R1_text.place(x = 120,y = 20,width = 400)
        R2.place(x = 20,y = 50)
        R3.place(x = 20,y = 100) 
        C1.place(x = 400,y = 160)
        C2.place(x = 100,y = 160)
    elif(check_flag == 0):#使用鏡頭
        R1_text = tk.Label(second_window,text='已選擇使用鏡頭',bg = "#F9F900")
        R2=tk.Radiobutton(second_window,text='選擇虛擬圍籬檔案',font=(10),variable=var,value=0)
        R3=tk.Radiobutton(second_window,text='繪製虛擬圍籬',font=(10),variable=var,value=1)
        C1=tk.Button(second_window,text='下一步',font=(10),command = lambda:control_section(second_window,2,3))
        C2=tk.Button(second_window,text='上一步',font=(10),command = lambda:control_section(second_window,2,1))
        R1_text.place(x = 120,y = 20,width = 400)
        R2.place(x = 20,y = 50)
        R3.place(x = 20,y = 100) 
        C1.place(x = 400,y = 160)
        C2.place(x = 100,y = 160)        
def third():#選擇虛擬圍籬所需檔案(若上一步選取虛擬圍籬)
    global JSON_NAME,TXT_NAME
    third_window = tk.Frame(decision_window,width = 600,height = 200)#建立第三步驟的子視窗
    third_window.pack()
    if(check_flag == 0):#check_flag=0開啟現有檔案、=1直接畫虛擬圍籬
        R1_text = tk.Label(third_window,text=str('尚未選取檔案'),bg = "#FAFAFA")
        R2_text = tk.Label(third_window,text=str('尚未選取檔案'),bg = "#FAFAFA")
        C1=tk.Button(third_window,text='下一步',font=(10),state = tk.DISABLED,command = lambda:control_section(third_window,3,0))
        C2=tk.Button(third_window,text='上一步',font=(10),command = lambda:control_section(third_window,3,2))
        R1=tk.Button(third_window,text='JSON檔',command = lambda:file_select(R1_text,C1,0))
        R2=tk.Button(third_window,text='TXT檔',command = lambda:file_select(R2_text,C1,1))
        R1.place(x = 20,y = 50,width = 70)
        R1_text.place(x = 120,y = 50,width = 400)
        R2.place(x = 20,y = 100,width = 70)
        R2_text.place(x = 120,y = 100,width = 400)
        C1.place(x = 400,y = 160)
        C2.place(x = 100,y = 160)
    else:
        decision_window.destroy() #結束主視窗
        g_read(video_name,check_point)#之後用來給Drawing參考
        from Drawing import JSON_NAME_n,txtname,path
        JSON_NAME = path+'\\'+JSON_NAME_n+'.json'
        TXT_NAME = path+'\\'+txtname+'.txt'
first()#第一步
decision_window.mainloop()  

fence = []
with open(JSON_NAME,"rb") as json_file:
    img_dict = json.load(json_file)
img_list = img_dict['content']
zone = np.asarray(img_list)#虛擬圍籬
zone = zone.astype(np.uint8)
point = []
with open(TXT_NAME, 'r') as txt_file:
    for line in txt_file:
        point.append(int(line))
point = np.asarray(point)
fence = point.reshape((int(len(point)/2),2))#將point存成兩個為一組的陣列