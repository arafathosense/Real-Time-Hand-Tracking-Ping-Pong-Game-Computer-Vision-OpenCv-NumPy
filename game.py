import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cvzone
import random

# ---------------- CONFIG ----------------
width, height = 640, 480
paddleY = 440        # Paddle Y position
ballSize = 40
paddleWidth, paddleHeight = 120, 30
borderTop = 50

# ------------- INITIALIZE ---------------
cap = cv.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

hd = HandDetector(detectionCon=0.7, maxHands=1)

ball = cv.resize(cv.imread("ball.png", cv.IMREAD_UNCHANGED), (ballSize, ballSize))
paddle = cv.resize(cv.imread("speech.png", cv.IMREAD_UNCHANGED), (paddleWidth, paddleHeight))
gameoverImg = cv.resize(cv.imread("gameover.png", cv.IMREAD_UNCHANGED), (width, height))

# Ball default
position = [random.randint(60, 580), 120]
speedx = 8
speedy = 8
score = 0

# ----------------------------------------
while True:
    ret, img = cap.read()
    img = cv.flip(img, 1)

    # Border lines
    cv.rectangle(img, (0, height), (width, 0), (0, 0, 255), 8)
    cv.rectangle(img, (0, paddleY), (width, height), (0, 255, 255), 6)

    # Detect hand
    hands, img = hd.findHands(img, flipType=False)
    paddleX = 260  # default

    if hands:
        x, y, w, h = hands[0]['bbox']
        paddleX = np.clip(x - paddleWidth // 2, 5, width - paddleWidth - 5)
        img = cvzone.overlayPNG(img, paddle, [paddleX, paddleY])

    # ----------- TOP Bounce -----------
    if position[1] <= borderTop:
        speedy = -speedy
        position[0] += random.randint(-15, 15)

    # ----------- Paddle Bounce ----------
    if paddleX - 10 < position[0] < paddleX + paddleWidth + 10 and (paddleY - 20) < position[1] < paddleY + 10:
        speedy = -speedy
        position[0] += random.randint(-20, 20)
        score += 1

        # Increase difficulty gradually
        speedx += 0.2 if speedx > 0 else -0.2
        speedy += 0.2 if speedy > 0 else -0.2

    # ---------- Game Over -------------
    if position[1] > 430:
        img = gameoverImg.copy()
        cvzone.putTextRect(img, f'Final Score: {score}', [220, 180], scale=2, thickness=3, colorR=(0, 0, 0))
        cvzone.putTextRect(img, 'Press R to Restart', [210, 260], scale=1.8, thickness=2, colorR=(0, 0, 0))
        cvzone.putTextRect(img, 'Press ESC to Quit', [225, 300], scale=1.8, thickness=2, colorR=(0, 0, 0))
        cv.imshow("Arafat Game", img)

        key = cv.waitKey(1)
        if key in [ord('r'), ord('R')]:
            position = [random.randint(80, 560), 120]
            speedx = 8
            speedy = 8
            score = 0
        elif key == 27:
            break
        continue

    # ---------- Side Bounce ----------
    if position[0] <= 20 or position[0] >= width - 20:
        speedx = -speedx

    # ---------- Update Ball ----------
    position[0] += int(speedx)
    position[1] += int(speedy)

    img = cvzone.overlayPNG(img, ball, position)

    # Score display
    cvzone.putTextRect(img, f"Score: {score}", [260, 20], scale=1.6, thickness=2)

    cv.imshow("Arafat Game", img)

    key = cv.waitKey(1)
    if key == 27:
        break
    if key in [ord('r'), ord('R')]:
        position = [random.randint(80, 560), 120]
        speedx = 8
        speedy = 8
        score = 0
