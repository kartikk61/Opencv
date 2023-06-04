import cv2

widthImg = 640
heightImg = 480

numberPlateCascade = cv2.CascadeClassifier('Resources/haarcascade_russian_plate_number.xml')
minArea = 200
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
count=0
while True:
    success, img = cap.read()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    numberPlates = numberPlateCascade.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in numberPlates:
        area = w * h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, 'Number plate ', (x, y - 5),
                        cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
                        1, (255, 0, 255), 2)
            imgRoi = img[y: y + h, x:x + w]
            cv2.imshow('Roi ', imgRoi)
    cv2.imshow('Result', img)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite('Resources/Scanned/NoPlate'+str(count)+'.jpg',imgRoi)
        cv2.rectangle(img,(0,200),(640,300),(0,255,0),cv2.FILLED)
        cv2.putText(img,'Scan saved',(150,265), cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
                    2,(0,0,225),2)
        cv2.imshow('Result',img)
        cv2.waitKey(500)
        count+=1

