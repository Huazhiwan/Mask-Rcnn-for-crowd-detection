# Mask-Rcnn-for-crowd-detection
# People counting、People detection、Simple virtual fence application
建議python 使用 3.6版本  
此為學生時期寫出的程式，因此可能有許多漏洞及優化問題
### step1:
此程式為基於Mask-Rcnn運作，因此建議先透過 <https://github.com/matterport/Mask_RCNN>，將Mask-Rcnn安裝完成，或
使用requirements.txt 安裝所需套件。套件安裝完成後，執行setup.py。  
### step2:
上述設定完成後，即可執行people_detection.py進行人物辨識  
(1)先選取輸入來源類型  

![image](https://user-images.githubusercontent.com/71805770/220571005-753f38bf-1696-4685-bf32-04234c706a91.png)  

(2)選取來源與虛擬圍籬檔案(第一次使用時必須繪製虛擬圍籬)  
![image](https://user-images.githubusercontent.com/71805770/220571258-29ad4294-4b1a-4f13-9db3-a80928725fc1.png)  
(3)依順時針方向繪製虛擬圍籬，並按下Q鍵(一次不行就兩次)結束繪製  
![image](https://user-images.githubusercontent.com/71805770/220571965-12d3d61d-433d-4351-8e3a-0c1c72664743.png)  
(4)輸入虛擬圍籬檔名  
![image](https://user-images.githubusercontent.com/71805770/220572252-db19acb6-0443-4e1a-93f2-483055eba32b.png)  
### step3:  
得到結果，最後使用Ctrl-C結束執行  
![image](https://user-images.githubusercontent.com/71805770/220572623-a5242adc-031b-4194-b1e9-67035fb36fc1.png)  
![image](https://user-images.githubusercontent.com/71805770/220572561-2698383e-1b0c-4c15-8908-862a7809bc4c.png)  



