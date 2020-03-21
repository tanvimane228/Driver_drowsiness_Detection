import cv2
from functools import wraps
from pygame import mixer
import time

lastsave = 0


def counter(func):
    @wraps(func)
    def tmp(*args, **kwargs):
        tmp.count += 1
        global lastsave
        if time.time() - lastsave > 1:
            # this is in seconds, so 5 minutes = 300 seconds
            lastsave = time.time()
            tmp.count = 0
        return func(*args, **kwargs)
    tmp.count = 0
    return tmp


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0)


@counter
def closed():
  print ("Eye Closed")


def openeye():
  print ("Eye is Open")



def sound():
    mixer.init()
    mixer.music.load('alarm.mp3')
    mixer.music.play()

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray)

        if eyes is not ():
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                openeye()
        else:
           closed()
           if closed.count == 1:
               print ("driver is sleeping")
               sound()





    cv2.imshow('img', img)
    k = cv2.waitKey(1) & 0xff
    if k==27:
        break


cap.release()
cv2.destroyAllWindows()
