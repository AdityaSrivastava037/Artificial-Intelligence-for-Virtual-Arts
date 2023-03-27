#from email.mime import image
import HandTrackingModule as htm
import cv2
import numpy as np
import os
folder = "Header"
video = cv2.VideoCapture(0)
list = os.listdir("Header")
overlayList = []
video.set(3,1280)
video.set(4,720)
drawColor = (255,0,255)
for i in list:
    image = cv2.imread(f'{folder}/{i}')
    overlayList.append(image)
header = overlayList[0]
xp,yp = 0,0
eraserThickness = 50
shape = 'freestyle'
detector = htm.handDetector(detectionCon=0.85,maxHands=1)
imgcanvas = np.zeros((720,1280,3),np.uint8)



while True:
    success, img = video.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    pos = detector.findPosition(img)
    print(pos)
    if len(pos)!=0:
     xi,yi = pos[8][1:]
     xm, ym = pos[12][1:]
     xt,yt = pos[4][1:]
     dist = int((((yt-y1)**2)+((xt-x1)**2))**0.5)
     up = detector.fingersUp()
     if up[1] and up[2]:
         if y1 < 120:
             if 250 < x1 < 450:
                 header = overlayList[0]
                 drawColor = (255, 0, 255)
             elif 550 < x1 < 750:
                 header = overlayList[1]
                 drawColor = (255, 0, 0)
             elif 800 < x1 < 950:
                 header = overlayList[10]
                 drawColor = (0, 255, 0)
             elif 1050 < x1 < 1200:
                 header = overlayList[5]
                 drawColor = (0, 0, 0)
         if y1 > 120 and y1 < 210:
             if x1 < 250:
                 header = overlayList[9]

             elif 250 < x1 < 450 and drawColor == (255, 0, 255):
                 header = overlayList[0]
                 shape = 'freestyle'
             elif 550 < x1 < 750 and drawColor == (255, 0, 255):
                 header = overlayList[6]
                 shape = 'circle'
             elif 800 < x1 < 950 and drawColor == (255, 0, 255):
                 header = overlayList[7]
                 shape = 'rectangle'
             elif 1050 < x1 < 1200 and drawColor == (255, 0, 255):
                 header = overlayList[8]
                 shape = 'elipse'
             elif 250 < x1 < 450 and drawColor == (255, 0, 0):
                 header = overlayList[10]
                 shape = 'freestyle'
             elif 550 < x1 < 750 and drawColor == (255, 0, 0):
                 header = overlayList[11]
                 shape = 'circle'
             elif 800 < x1 < 950 and drawColor == (255, 0, 0):
                 header = overlayList[12]
                 shape = 'rectangle'
             elif 1050 < x1 < 1200 and drawColor == (255, 0, 0):
                 header = overlayList[13]
                 shape = 'elipse'
             if 250 < x1 < 450 and drawColor == (0, 255, 0):
                 header = overlayList[1]
                 shape = 'freestyle'
             elif 550 < x1 < 750 and drawColor == (0, 255, 0):
                 header = overlayList[2]
                 shape = 'circle'
             elif 800 < x1 < 950 and drawColor == (0, 255, 0):
                 header = overlayList[3]
                 shape = 'rectangle'
             elif 1050 < x1 < 1200 and drawColor == (0, 255, 0):
                 header = overlayList[4]
                 shape = 'elipse'
                cv2.circle(img,(x1,y1),25,drawColor,cv2.FILLED)
         if up[1] and up[2] == False:
            #print("Drawing Node")
            if xp==0 and yp==0:
                xp,yp = x1,y1
                if drawColor== (0,0,0):
                    if up[1] and up[4]:
                        eraserThickness = dist
                        #cv2.line(imgcanvas,(xp,yp),(x1,y1),drawColor,eraserThickness)
                        cv2.circle(img,(x1,y1),eraserThickness,drawColor,cv2.FILLED)
                        cv2.circle(imgcanvas,(x1,y1), eraserThickness, drawColor, cv2.FILLED)
                    #cv2.line(imgcanvas,(xp, yp),(x1, y1),drawColor,50)
                    else:
                        if shape == 'freestyle':
                            if dist<30:
                            cv2.line(imgcanvas, (xp, yp), (x1, y1), drawColor, 10)
                            #circle
                            if shape == 'circle':
                               
                                #print(dist)
                                cv2.circle(img,(x1,y1),dist,drawColor)
                                
                                #rectangle
                                if shape == 'rectangle':
                                    cv2.rectangle(img,(xt,yt),(x1,y1),drawColor)
                                    if up[4]:
                                        cv2.rectangle(imgcanvas, (xt, yt), (x1, y1), drawColor)
                            
            #cv2.linie(img,(xp,yp),(x1,y1),drawColor,10)
            #cv2.linie(imgcanvas,(xp,yp),(x1,y1),drawColor,10)
            xp,yp = x1,y1

    img[0:210,0:1280]=header

    img_gray = cv2.cvtColor(imgcanvas,cv2.COLOUR_BGR2GRAY)
    _,imginv = cv2.threshold(img_gray,50,255,cv2.THRESH_BINARY_INV)
     imginv = cv2.cvtColor(imginv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imginv)
        img = cv2.bitwise_or(img, imgcanvas)
    imginv = cv2.cvtColor(imginv,cv2.color)
    cv2.imshow("video",img)
    cv2.imshow("Canvas",imgcanvas)
    cv2.waitKey(1)
