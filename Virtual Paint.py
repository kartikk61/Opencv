import cv2
import numpy as np


def empty(a):
    pass


cap = cv2.VideoCapture(1)
cap.set(3, 50)
cap.set(4, 50)
#
cv2.namedWindow('TrackBars')
cv2.resizeWindow('TrackBars', 640, 240)
cv2.createTrackbar('Hue Min', 'TrackBars', 0, 179, empty)
cv2.createTrackbar('Hue Max', 'TrackBars', 0, 179, empty)
cv2.createTrackbar('sat Min', 'TrackBars', 0, 255, empty)
cv2.createTrackbar('sat Max', 'TrackBars', 255, 255, empty)
cv2.createTrackbar('Val Min', 'TrackBars', 0, 255, empty)
cv2.createTrackbar('Val Max', 'TrackBars', 255, 255, empty)

myColors = [[43, 44, 2, 90, 255, 255],
            [163, 0, 0, 179, 203, 255]]
myColorValues=[[204,204,0],[178,102,255]]   #BGR format
myPoints=[] #[x,y,colorId]

def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult,(point[0],point[1]), 10,myColorValues[point[2]], cv2.FILLED)



def findColor(img, myColors,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count=0
    newPoints=[]
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:])
        mask2 = cv2.inRange(imgHSV, lower, upper)
        # mask2=cv2.inRange(imgHSV, np.array([43,44,2]), np.array([90,255,255]))
        x,y=getContours(mask2)
        cv2.circle(imgResult,(x,y), 10,myColorValues[count], cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count+=1
        cv2.imshow(str(color[0]), mask2)
    return newPoints

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # print(len(contours))
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)
        if area > 500:
            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            # print(peri)
            approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
            # print(len(approx))
            # objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
    return x+(w//2),y
while True:
    # img = cv2.imread(path)
    # imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    success, img = cap.read()
    imgResult=img.copy()
    # getContours()
    newPoints= findColor(img, myColors,myColorValues)
    if len(newPoints)!=0:
        for newp in newPoints:
            myPoints.append(newp)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)

    cv2.imshow('Video Result', imgResult)


    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos('Hue Min', 'TrackBars')
    h_max = cv2.getTrackbarPos('Hue Max', 'TrackBars')
    s_min = cv2.getTrackbarPos('sat Min', 'TrackBars')
    s_max = cv2.getTrackbarPos('sat Max', 'TrackBars')
    v_min = cv2.getTrackbarPos('Val Min', 'TrackBars')
    v_max = cv2.getTrackbarPos('Val Max', 'TrackBars')
    # print(h_min,h_max)
    # print(s_min,s_max)
    # print(v_min,v_max)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask1 = cv2.inRange(imgHSV, lower, upper)

    imgResult = cv2.bitwise_and(img, img, mask=mask1)
    cv2.imshow('Skin image', imgResult)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
