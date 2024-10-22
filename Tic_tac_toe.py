# import required libraries and classes
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import time

video = cv2.VideoCapture(0)  # to capture the video
board = np.zeros((300, 300, 3), np.uint8)  # creating a board
detector = HandDetector(maxHands=1, detectionCon=0.8)  # declaring hand detector
x, y = 340, 50
moves = [["", "", ""], ["", "", ""], ["", "", ""]]  # to store move in array
coordinates = [[[], [], []], [[], [], []], [[], [], []]]  # to store coordinates 
curr_turn = "O"
total_moves = 0
winner = "-"
xwins = 0
owins = 0
color = (0, 255, 0)
notify = ""


# creating board for tic tac toe
def draw_board():
    board[:] = (0, 0, 0)
    for i in range(2):
        x = 98
        for j in range(2):
            if i == 0:
                cv2.line(board, (x, 0), (x, 300), (81, 218, 11), 2)
                x += 98
            else:
                cv2.line(board, (0, x), (300, x), (81, 218, 11), 2)
                x += 98


def print_moves(x1, y1):
    global moves, color, total_moves, coordinates, owins, xwins, winner, notify
    y = 0
    if winner == "-":
        for i in range(3):
            x = 0
            for j in range(3):
                if x < x1 < x + 98 and y < y1 < y + 98 and moves[i][j] == "":
                    cv2.putText(board, curr_turn, ((x + x + 70) // 2, (y + y + 110) // 2), cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                color)
                    print(x1, y1)
                    coordinates[i][j] = list(((x + x + 90) // 2, (y + y + 90) // 2))
                    moves[i][j] = curr_turn
                    time.sleep(0.3)
                    change_turn()
                    print(coordinates)
                    print(moves)
                    if total_moves > 4:
                        check_winner()
                        # print(winner)
                        if winner == "X":
                            xwins += 1
                        elif winner == "O":
                            owins += 1
                        elif total_moves == 9:
                            winner = "Draw"
                            # print(x, x1, x + 98)
                    # print(y, y1, y + 98)
                x += 100
            y += 100


def change_turn():
    global curr_turn, total_moves, color
    if curr_turn == "X":
        curr_turn = "O"
        color = (0, 255, 0)
    elif curr_turn == "O":
        curr_turn = "X"
        color = (0, 0, 255)
    total_moves += 1


def check_winner():
    global moves, winner, board, coordinates
    for i in range(3):
        if moves[i][0] == moves[i][1] and moves[i][1] == moves[i][2] and moves[i][0] != "":
            winner = moves[i][0]
            cv2.line(board, (coordinates[i][0]), (coordinates[i][2]), (0, 0, 255), 2)
            return
    for i in range(3):
        if moves[0][i] == moves[1][i] and moves[1][i] == moves[2][i] and moves[0][i] != "":
            winner = moves[i][0]
            cv2.line(board, (coordinates[0][i]), (coordinates[2][i]), (0, 0, 255), 2)
            return
    if moves[0][0] == moves[1][1] and moves[1][1] == moves[2][2] and moves[0][0] != "":
        winner = moves[0][0]
        cv2.line(board, (coordinates[0][0]), (coordinates[2][2]), (0, 0, 255), 2)
        return
    if moves[0][2] == moves[1][1] and moves[1][1] == moves[2][0] and moves[2][0] != "":
        winner = moves[1][1]
        cv2.line(board, (coordinates[2][0]), (coordinates[0][2]), (0, 0, 255), 2)


def reset():
    global owins, xwins, winner, total_moves, moves, x, y, coordinates, notify
    notify = ""
    winner = "-"
    total_moves = 0
    x, y = 340, 50
    moves = [["", "", ""], ["", "", ""], ["", "", ""]]
    coordinates = [[[], [], []], [[], [], []], [[], [], []]]
    draw_board()


draw_board()
while True:
    _, img = video.read()
    img = cv2.flip(img, 1)
    hand, img = detector.findHands(img)
    img[50:350, 340:640] = board
    if hand:
        list1 = hand[0]
        lmlist = list1['lmList']
        if lmlist:
            fing = detector.fingersUp(list1)
            if fing == [0, 1, 1, 0, 0]:
                x1, y1 = lmlist[8][0:2]
                x2, y2 = lmlist[12][0:2]
                # print(x1, y1)
                # print(x2, y2)
                nx, ny = (x1 + x2) // 2, (y1 + y2) // 2
                # print(nx-340, ny-50)
                dis, _, img = detector.findDistance(lmlist[8][0:2], lmlist[12][0:2], img)
                dis = int(dis)
                if dis < 42:
                    print_moves(nx - 340, ny - 50)
    cv2.putText(img, "Current Turn : " + curr_turn, (10, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 255))
    cv2.putText(img, "Winner : " + winner, (10, 80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255))
    cv2.putText(img, "Score", (10, 400), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 255))
    cv2.putText(img, "o wins : " + str(owins) + " x wins : " + str(xwins), (10, 440), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                (0, 255, 0))
    if winner != "-":
        notify = "Press R to reset"
        cv2.putText(img, notify, (340, 380), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))
    cv2.imshow("Tic Tac Toe", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('r'):
        reset()