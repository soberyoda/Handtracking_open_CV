"""
    Rock-Paper-Scissor

    simple game using computer vision
    1)press "s" button to start the game
    2)press "q" button to stop the game

    Python 3.10
    08.2022

"""

# Libraries
import random

import cvzone
from cvzone.HandTrackingModule import HandDetector
import cv2
# import numpy as np
import mediapipe as mp
import time

# web camera
cap = cv2.VideoCapture(0)
# camera settings
cap.set(3, 640)  # width
cap.set(4, 480)  # height

# create Hand Detector
detector = HandDetector(maxHands=1)

# timer
# initial states
timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # AI, Player

# main loop
while True:
    # images-background
    imgBG = cv2.imread("Resources\BG.png")  # background img

    # camera image
    success, img = cap.read()

    # scale img
    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)  # change height
    imgScaled = imgScaled[:, 80:480]  # change width

    # Find Hands
    hands, img = detector.findHands(imgScaled)  # with draw
    # Start the game
    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:  # rock
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:  # pepper
                        playerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:  # scissor
                        playerMove = 3
                    # AI part

                    randomNumber = random.randint(1, 3)
                    imgAI = cv2.imread(f"Resources/{randomNumber}.png", cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    # Player wins

                    if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1
                    # AI wins
                    if (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1

                    # print(playerMove)
                else:
                    startGame = False
                    stateResult = False  # reset game
                    timer = 0
                    scores = [0, 0]

    # join BG and camera img
    imgBG[234:654, 795:1195] = imgScaled
    cv2.putText(imgBG, str("'s'- start the game, 'q'- quit the game, 'r'- reset score"), (73, 694),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)  # basics information about game rules
    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 6)
    # cv2.imshow ("Output", img)
    cv2.imshow("BG", imgBG)

    # press key to start a game
    key = cv2.waitKey(1)
    if key == ord("s"):
        startGame = True
        initialTime = time.time()
        stateResult = False  # reset game
    elif key == ord("r"):
        scores = [0, 0]
    elif key == ord("q"):  # press "q" to stop the game
        break
