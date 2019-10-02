import cv2
import numpy as np
import sys
import win32api
import win32con
import time

                      #LOAD AND ASSIGN HAAR CASCADES. REMEMBER TO INSERT YOUR OWN PATH.
facePath = 'C:\Users\Nina\Downloads\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml'
mouthPath = 'C:\Users\Nina\Downloads\opencv\sources\data\haarcascades\haarcascade_mcs_mouth.xml'
faceCascade = cv2.CascadeClassifier(facePath)
mouthCascade = cv2.CascadeClassifier(mouthPath)


cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
sF = 1.05

while True:
    #ASSIGN AND CONVERT PICTURE VERSIONS
    ret, frame = cap.read() # Capture frame-by-frame
    img = frame #FRAME = ORDINARY COLOR IMAGE
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #CONVERT FROM COLOR TO BLACK AND WHITE
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  #CONVERT FROM COLOR TO HSV
    ret, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY) #CONVERT FROM BLACK AND WHITE TO MASK
    mask_inv = cv2.bitwise_not(mask) #INVERT MASK

     #DETECT FACE
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor= sF,
        minNeighbors=8,
        minSize=(55, 55),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
# ---- Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        y = int(y - 0.15 * h)
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        roi_gray = gray[y:y+h, x:x+w] #This ROI is found in Black and white version
        roi_color = frame[y:y+h, x:x+w] #This ROI is found in color version

# ------Dra
        mouth_rects = mouthCascade.detectMultiScale(gray, 1.7, 11)
        for (x, y, w, h) in mouth_rects:
            VK_CODE = {'spacebar': 0x20}
            y = int(y - 0.15 * h)
            cv2.rectangle(frame, (x - 20, y - 10), ((x + 5) + (w + 5), (y + 5) + (h + 5)), (0, 255, 0), 3)
            roi_mask_inv = mask_inv[y:y + h, x:x + w]  #Angir ROI for munnen i Mask Inverted
            #print roi_mask_inv
            netflix = sum(roi_mask_inv, )               #Summerer opp forste nivaa av array og leser inn i navnet netflix
            #print netflix
            youtube = sum(netflix)                      #Summerer opp neste nivaa av array og leser inn i navnet youtube
            #youtube = 800
           # bryter = 5
            print youtube                               #Printer ut youtube, som er totalverdi av pixler i ROI
            if youtube > 1 :                             #IF-setning som forteller om verdien av ROI er over eller under 1.
                print 'Open mouth'
                #cv.PutText(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.rectangle(frame, (x - 20, y - 10), ((x + 5) + (w + 5), (y + 5) + (h + 5)), (255, 255, 255), 3)
                win32api.keybd_event(VK_CODE['spacebar'], 0, 0, 0)
                time.sleep(1.05)
                win32api.keybd_event(VK_CODE['spacebar'], 0, win32con.KEYEVENTF_KEYUP, 0)
                    #bryter = 0
            else:
                print 'Mouth closed'
                cv2.rectangle(frame, (x - 20, y - 10), ((x + 5) + (w + 5), (y + 5) + (h + 5)), (0, 0, 0), 3)
                #bryter + 5
            break

    cv2.imshow('Detectoring 1', frame)                  #Printer ut vanlig fargebilde, med illustrasjoner

    c = cv2.cv.WaitKey(7) % 0x100 #Funksjonen som lukker vinduet
    if c == 27:

        break

cap.release()
cv2.destroyAllWindows()