import pandas as pd
import cv2
import urllib.request
import numpy as np
import os
from datetime import datetime
import face_recognition
from IPython.display import display
import time
from openpyxl import workbook
import datetime
import pytz

path = r'D:\#miniproject\images'
#url='http://192.168.192.225/cam-hi.jpg'
##'''cam.bmp / cam-lo.jpg /cam-hi.jpg / cam.mjpeg '''
 
'''if 'Attendance.csv' in os.listdir(os.path.join(os.getcwd(),'D:\#miniproject\images')):
    print("there iss..")
    os.remove("Attendance.csv")
else:
    df=pd.DataFrame(list())
    df.to_csv("Attendance.csv")'''
    
 
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)
 
 
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
 
 
def markAttendance(name):
    with open("Attendance.csv", 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')
 
 
encodeListKnown = findEncodings(images)
print('Encoding Complete')

# capturing the image
filename= cv2.VideoCapture(0)

ret, img= filename.read()
imgS= cv2.resize(img,(0,0),fx=0.25,fy=0.25)
imgS= cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

facesCurrFrame= face_recognition.face_locations(imgS)
encodesCurrFrame= face_recognition.face_encodings(imgS, facesCurrFrame)

for encodeFace, faceLoc in zip(encodesCurrFrame, facesCurrFrame):
    matches= face_recognition.compare_faces(encodeListKnown, encodeFace)
    faceDis= face_recognition.face_distance(encodeListKnown, encodeFace)

matchIndex= np.argmin(faceDis)

book= workbook()
now= datetime.datetime.now()

today= now.day()
month= now.month()
year= now.strftime("%x")
t_start= time.time()
t_end= t_start+ 60*8
x=0
while time.time()< t_end:
    curr_time= time.time()
    try:
        filename= take_photo()
        print("Saved to {}".format(filename))

        # show the image just taken
        display(Image(filename))
    except Exception as err:
            # errors will be thrown if user does not have a webcam or if
            # they don't give permission to access it
        print(str(err))

if matches[matchIndex]:
    name= className[matchIndex].upper()
    print(name)
    y1,x2,y2,x1= faceLoc
    y1,x2,y2,x1= y1*4,x2*4,y2*4,x1*4
    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
    cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
    cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_DUPLEX,1.0,(255,255,255),1)

    markAttendance(name,book)
    time.sleep(150)

 
