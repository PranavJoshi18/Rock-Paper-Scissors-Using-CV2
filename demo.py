import cv2
import mediapipe as mp
import time
import random

#using cv2 utilities

cap = cv2.VideoCapture(0)
cap.set(3,268)
cap.set(4,220)

#using mediapipe utilities

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

#creating a timer

timer=0
stateResult=False
startGame=False
scores = [0,0] #[Computer,You]

#hand movement

def handMovement(hand_landmarks):
    landmarks = hand_landmarks.landmark
    if all([landmarks[i].y<landmarks[i+3].y for i in range(9,20,4)]): return "rock"
    elif landmarks[13].y<landmarks[16].y and landmarks[17].y<landmarks[20].y: return "scissors"
    else: return "paper"

#creating mp object and running hand gestures tracking on the palette

with mp_hands.Hands(
    model_complexity=0,
    min_tracking_confidence=0.5,
    min_detection_confidence=0.5) as hands:
    while True:
        imgBG = cv2.imread("resources/bg2.png")
        success,img = cap.read()
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results = hands.process(img)
        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

        if startGame:

            if not stateResult:
                timer=time.time() - initialTime
                cv2.putText(imgBG,str(int(timer)),(471,366),cv2.FONT_HERSHEY_PLAIN,6,(0,0,0),4)

            if timer>3:
                stateResult=True
                timer=0

                # this is for displaying hand tracking!
                # if results.multi_hand_landmarks:
                #     for hand_landmarks in results.multi_hand_landmarks:
                #         mp_drawing.draw_landmarks(img,
                #                                 hand_landmarks,
                #                                 mp_hands.HAND_CONNECTIONS,
                #                                 mp_drawing_styles.get_default_hand_landmarks_style(),
                #                                 mp_drawing_styles.get_default_hand_connections_style())

                playerResult = handMovement((results.multi_hand_landmarks)[0])  #for one hand

                l = ['rock','paper','scissors']
                AIResult = random.choice(l)
                imgAI = cv2.imread('resources/'+AIResult+'.png')
                # imgBG[252:452,174:424] = imgAI
                # cv2.imshow("AI",imgAI)

                if (playerResult=="scissors" and AIResult=="paper"): scores[1]+=1
                elif (playerResult=="scissors" and AIResult=="rock"): scores[0]+=1
                elif (playerResult=="paper" and AIResult=="rock"): scores[1]+=1
                elif (playerResult=="paper" and AIResult=="scissors"): scores[0]+=1
                elif (playerResult=="rock" and AIResult=="scissors"): scores[1]+=1
                elif (playerResult=="rock" and AIResult=="paper"): scores[0]+=1


        if stateResult:
            imgBG[252:452,134:384] = imgAI
            # cv2.imshow("AI",imgAI)

        cv2.putText(imgBG,str(scores[0]),(393,470),cv2.FONT_HERSHEY_PLAIN,4,(0,0,0),4)
        cv2.putText(imgBG,str(scores[1]),(570,470),cv2.FONT_HERSHEY_PLAIN,4,(0,0,0),4)

        img = cv2.flip(img,1)
        img = img[1:219,5:263]
        imgBG[243:461,617:875] = img
        # cv2.imshow("Image",img)
        cv2.imshow("BG",imgBG)
        key=cv2.waitKey(1)
        if key==ord('s'):
            startGame=True
            initialTime=time.time()
            stateResult=False