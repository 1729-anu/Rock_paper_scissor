import random
import cv2
import cvzone
import mediapipe as mp
import time

# Initialize Mediapipe hand detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [Player, AI]
playerMove = None
imgAI = None  # Placeholder for AI's move image
rounds_played = 0
max_rounds = 5  # Number of rounds to play

def display_winner(imgBG):
    global scores
    winner_text = "Match Draw!" if scores[0] == scores[1] else "You Win!" if scores[0] > scores[1] else "AI Wins!"
    cv2.putText(imgBG, winner_text, (450, 300), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 6)
    cv2.imshow("BG", imgBG)
    cv2.waitKey(5000)  # Display result for 5 seconds

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture frame")
        continue

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    cursors = []

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lmList = [(int(lm.x * img.shape[1]), int(lm.y * img.shape[0])) for lm in hand_landmarks.landmark]
            cursors.append(lmList[8])
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if len(lmList) != 0:
                if lmList[8][1] > lmList[6][1] and lmList[12][1] > lmList[10][1] and lmList[16][1] > lmList[14][1] and lmList[20][1] > lmList[18][1]:
                    playerMove = 1  # Rock
                elif lmList[8][1] < lmList[6][1] and lmList[12][1] < lmList[10][1] and lmList[16][1] < lmList[14][1] and lmList[20][1] < lmList[18][1]:
                    playerMove = 2  # Paper
                elif lmList[8][1] < lmList[6][1] and lmList[12][1] < lmList[10][1] and lmList[16][1] > lmList[14][1] and lmList[20][1] > lmList[18][1]:
                    playerMove = 3  # Scissors

    imgBG = cv2.imread("BG.png")
    img_resized = cv2.resize(img, (400, 420))

    if startGame:
        if not stateResult:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                stateResult = True
                timer = 0
                if cursors:
                    if playerMove is not None:
                        randomNumber = random.randint(1, 3)
                        imgAI = cv2.imread(f'{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                        if (playerMove == 1 and randomNumber == 3) or (playerMove == 2 and randomNumber == 1) or (playerMove == 3 and randomNumber == 2):
                            scores[0] += 1  # Player wins
                        elif (playerMove == 3 and randomNumber == 1) or (playerMove == 1 and randomNumber == 2) or (playerMove == 2 and randomNumber == 3):
                            scores[1] += 1  # AI wins
                        
                        rounds_played += 1
                        if rounds_played >= max_rounds:
                            display_winner(imgBG)
                            break  # Exit loop after 5 rounds

    imgBG[234:654, 795:1195] = img_resized
    cv2.putText(imgBG, str(scores[1]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[0]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    if imgAI is not None:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.imshow("BG", imgBG)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
        playerMove = None
        imgAI = None
        print(f"Round {rounds_played + 1} started!")

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()