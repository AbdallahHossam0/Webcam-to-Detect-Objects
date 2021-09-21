import cv2, os, pandas
from datetime import datetime

os.system("cls")

df = pandas.DataFrame(columns= ["Start", "End"])

firstFrame = None

statusList = [None, None]
times = []

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    check, frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # to increase the accuracy of the calculations 
    gray = cv2.GaussianBlur(gray, (21, 21), 0)



    if firstFrame is None:
        firstFrame = gray
        continue
    
    deltaFrame = cv2.absdiff(firstFrame, gray)

    th_frame = cv2.threshold(deltaFrame, 30, 255, cv2.THRESH_BINARY)[1]
    th_frame = cv2.dilate(th_frame, None, iterations= 2)

    # to find contours
    (cnts,_) = cv2.findContours(th_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in cnts:
        if cv2.contourArea(cnt) < 10000:
            continue
        
        status = 1
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(frame , (x, y), (x + w, y + h), (0, 255, 0), 3)

    statusList.append(status)

    if statusList[-1] == 1  and statusList[-2]  == 0:
        times.append(datetime.now())
    if statusList[-1] == 0  and statusList[-2]  == 1:
        times.append(datetime.now())

    cv2.imshow("Capturing gray..", gray)
    cv2.imshow("Capturing delta..", deltaFrame)
    cv2.imshow("Capturing threshold..", th_frame)
    cv2.imshow("Capturing colored ..", frame)

    key = cv2.waitKey(1)
    
    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break


print(statusList)
print(times)

for i in range(0 , len(times), 2):
    df = df.append({"Start": times[i], "End" : times[i + 1]}, ignore_index= True)

df.to_csv("times.csv")
video.release()
cv2.destroyAllWindows()
