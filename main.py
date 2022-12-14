import cv2 as cv
from windowcapture import Screencap
import easyocr
import win32gui, win32ui, win32con
import time
import torch


reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())

screen = Screencap()
screen.update_res_and_window_points()

hwnd = win32gui.FindWindow(None, 'War  ')
win = win32ui.CreateWindowFromHandle(hwnd)

##TODO: Monitor your CURRENT position in queue. Maybe just parse 'result'?


in_queue = True
while in_queue:
    queue_position, travel_position = screen.get_two_cropped_img()

    result = reader.readtext(queue_position, detail=0, paragraph=True)
    result2 = reader.readtext(travel_position, detail=0, paragraph=True)
    print(f"Queue Position: {result}")
    print(f"Travel Position: {result2}")

    if result2: #Avoid exception handling. Only check the text, if text is detected.
        if result2[0] == 'Press E to travel to adjacent region':
            win.SendMessage(win32con.WM_KEYDOWN, 0x45, 0)
            time.sleep(.01)
            win.SendMessage(win32con.WM_KEYUP, 0x45, 0)
            in_queue = False

    cv.imshow('Queue Position', queue_position)
    cv.imshow('Travel Position', travel_position)

    waitkey = cv.waitKey(1)

    if waitkey == ord('q'):
        cv.destroyAllWindows()



##TODO: Test at as many borders as possible.