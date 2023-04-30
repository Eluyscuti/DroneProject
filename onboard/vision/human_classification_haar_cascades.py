import cv2 
import pandas as pd
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480) #hi


while True:
    success, img = cap.read()
    cv2.imshow("Video", img)
    grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Person", grayscale_img)

    haar_cascade = cv2.CascadeClassifier("haar_human.xml")

    human_rect = haar_cascade.detectMultiScale(grayscale_img, scaleFactor = 1.03, minNeighbors= 3)

    for (x,y,w,h) in human_rect:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0))

    cv2.imshow("Detect", img)

    print("num human found: " +str(len(human_rect)))


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break