import math
import numpy
import cv2
import mediapipe as mp
from HAND_TRACKING import HandTrackingModule as htm
 
wCam = 900
hCam = 550
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(detectionConf=0.75)
tipIds = [4, 8, 12, 16, 20]
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    if not success:
        break
    else:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img, results = detector.findHands(img)
        Total_fingers = 0
        if results.multi_hand_landmarks:
            for handNo, handType in enumerate(results.multi_handedness):
                label = handType.classification[0].label
                lmlist = detector.find_position(img, handNo=handNo, draw=False)
                if len(lmlist) != 0:
                    fingers = []
                    # Thumb (image is mirrored, so left thumb opens the opposite way)
                    if label == "Right":
                        if lmlist[tipIds[0]][1] < lmlist[tipIds[0] - 1][1]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    else:
                        if lmlist[tipIds[0]][1] > lmlist[tipIds[0] - 1][1]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    # 4 Fingers
                    for id in range(1, 5):
                        if lmlist[tipIds[id]][2] < lmlist[tipIds[id] - 2][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    Total_fingers += fingers.count(1)
                    cv2.putText(
                        img,
                        f"{label}:{fingers.count(1)}",
                        (10, 130 + handNo * 50),
                        cv2.FONT_HERSHEY_COMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                    )
            cv2.putText(
                img,
                f"No of finger:{Total_fingers}",
                (10,70),
                cv2.FONT_HERSHEY_COMPLEX,
                1.5,
                (255,0,255),
                3,
            )
 
        cv2.imshow("FINGER_COUNTER", img)
 
        if cv2.waitKey(1) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()