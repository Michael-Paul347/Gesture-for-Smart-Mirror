import cv2
import mediapipe as mp
import pyautogui
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
##################################
tipIds = [4, 8, 12, 16, 20]
state = None
Gesture = None
wCam, hCam = 720, 640
############################ggg
def fingerPosition(image, handNo=0):
    lmList = []
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            # print(id,lm)
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
    return lmList
# For webcam input:
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
        continue
    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    lmList = fingerPosition(image)
    #print(lmList)
    if len(lmList) != 0:
        fingers = []
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                #state = "Play"
                fingers.append(1)
            if (lmList[tipIds[id]][2] > lmList[tipIds[id] - 2][2] ):
               # state = "Pause"
               # pyautogui.press('space')
               # print("Space")
                fingers.append(0)
        totalFingers = fingers.count(1)
        print(totalFingers)
        #print(lmList[9][2])

        if totalFingers == 3:
            cap.release()
            pyautogui.press('g')
            time.sleep(9)
            cap=cv2.VideoCapture(0)
           # fingers.append(1)
        if totalFingers == 0 and state == "Play":
            state = "Pause"
            pyautogui.press('space')
            print("Space") 
        if totalFingers == 1:
            if lmList[8][1]<300:
                print("left")  
                pyautogui.press('left')
                time.sleep(2)
            if lmList[8][1]>400:
                print("Right")
                pyautogui.press('Right')
                time.sleep(2)
        if totalFingers == 2:
            if lmList[9][2] < 210:
                print("Up")
                pyautogui.press('Up')
            if lmList[9][2] > 230:
                print("Down")
                pyautogui.press('Down')
                pyautogui.press('Down')
    #cv2.putText(image, str("Gesture"), (10,40), cv2.FONT_HERSHEY_SIMPLEX,
     #              1, (255, 0, 0), 2)
    cv2.imshow("Media Controller", image)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
  cv2.destroyAllWindows()               