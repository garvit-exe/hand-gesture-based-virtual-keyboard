import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
from pynput.keyboard import Controller, Key

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 520)

cv2.namedWindow("Virtual Keyboard", cv2.WINDOW_NORMAL)

detector = HandDetector(detectionCon=0.8, minTrackCon=0.2)

keyboard_keys = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
    ["SPACE", "ENTER", "BACKSPACE"]
]

keyboard = Controller()

class Button:
    def __init__(self, pos, text, size=(85, 85)):
        self.pos = pos
        self.size = size
        self.text = text

def draw_buttons(img, button_list):
    """
    Draws buttons on the given image.

    Args:
        img (numpy.ndarray): The image on which the buttons will be drawn.
        button_list (list): A list of Button objects representing the buttons to be drawn.

    Returns:
        numpy.ndarray: The image with the buttons drawn.
    """
    for button in button_list:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (x, y, w, h), 20, rt=0)
        cv2.rectangle(img, button.pos, (int(x + w), int(y + h)),
                      (37, 238, 250), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
    return img

button_list = []

for k in range(len(keyboard_keys)):
    for x, key in enumerate(keyboard_keys[k]):
        if key != "SPACE" and key != "ENTER" and key != "BACKSPACE":
            button_list.append(Button((100 * x + 25, 100 * k + 50), key))
        elif key == "ENTER":
            button_list.append(
                Button((100 * x - 30, 100 * k + 50), key, (220, 85)))
        elif key == "SPACE":
            button_list.append(
                Button((100 * x + 780, 100 * k + 50), key, (220, 85)))
        elif key == "BACKSPACE":
            button_list.append(
                Button((100 * x + 140, 100 * k + 50), key, (400, 85)))

while True:
    success, img = cap.read()
    allHands, img = detector.findHands(img)

    if len(allHands) == 0:
        lm_list, bbox_info = [], []
    else:
        lm_list, bbox_info = allHands[0]['lmList'], allHands[0]['bbox']

    img = draw_buttons(img, button_list)

    if lm_list:
        for button in button_list:
            x, y = button.pos
            w, h = button.size

            if x < lm_list[8][0] < x + w and y < lm_list[8][1] < y + h:
                cv2.rectangle(img, button.pos, (x + w, y + h),
                              (247, 45, 134), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)

                distance = np.sqrt(
                    (lm_list[8][0] - lm_list[4][0])**2 + (lm_list[8][1] - lm_list[4][1])**2)

                if distance < 30:
                    if button.text not in ['ENTER', "BACKSPACE", "SPACE"]:
                        keyboard.press(button.text)
                        sleep(0.2)
                    else:
                        if button.text == "SPACE":
                            keyboard.press(Key.space)
                            keyboard.release(Key.space)
                            sleep(0.2)

                        elif button.text == "ENTER":
                            keyboard.press(Key.enter)
                            keyboard.release(Key.enter)
                            sleep(0.2)

                        elif button.text == "BACKSPACE":
                            keyboard.press(Key.backspace)
                            keyboard.release(Key.backspace)
                            sleep(0.2)

                        else:
                            pass
                    cv2.rectangle(img, button.pos, (x + w, y + h),
                                  (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()