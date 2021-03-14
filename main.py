import cv2
import math
import os
from os import listdir
from os.path import isfile, join
import glob

path_for_video = 'video.mp4'

def frames(path_for_video):
    cap = cv2.VideoCapture(path_for_video)
    count = 0
    try: 
        
        # creating a folder named data 
        if not os.path.exists('data'): 
	        os.makedirs('data') 

    # if not created then raise error 
    except OSError: 
        print ('Error: Creating directory of data') 

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            cv2.imwrite('./data/' + '{:d}.jpg'.format(count%30 + count//30), frame)
            count += 30 # i.e. at 30 fps, this advances one second
            cap.set(1, count)
        else:
            cap.release()
            break
def mousepoints(event,x,y,flags,params):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(img,(x,y),5,(0,255,0),cv2.FILLED)
            pointlist.append([x,y])
def gradient(pts1,pts2):
    return ((pts2[1]-pts1[1])/(pts2[0]-pts1[0]))

def getAngle(pointlist):
    pts1,pts2,pts3 = pointlist[-3:]
    m1 = gradient(pts1,pts2)
    m2 = gradient(pts1,pts3)
    x = (m1-m2)/(1+(m2*m1))
    angr = math.atan(x)
    angd = round(math.degrees(angr),2)
    #if angd < 0 or angd > 90:angd = 180 - abs(angd)
    cv2.putText(img,f"Angle  = {angd}",(30,50),cv2.FONT_HERSHEY_TRIPLEX,2,(0,0,0),2)


frames(path_for_video)
files = sorted(glob.glob('data\*.jpg'),key= os.path.getmtime)
for path in files:
    img = cv2.imread(path)
    pointlist =[]
    while True:
        if len(pointlist) % 3 == 0 and len(pointlist) != 0:
            getAngle(pointlist)
        else:pass
        cv2.namedWindow("image",cv2.WINDOW_NORMAL)
        cv2.imshow('image',img)
             
        cv2.setMouseCallback("image",mousepoints)
        if cv2.waitKey(1) & 0xFF == ord('c'):  #c stands for clear
            pointlist = []
            img = cv2.imread(path)
        elif cv2.waitKey(1) & 0xFF == ord('n'):  #n stands for next
            break
cv2.destroyAllWindows()
        
