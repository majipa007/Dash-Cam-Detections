# Importing all the required libraries
import cv2 as cv
import time
from dash import Dash


def play_video(video_path):
    dash = Dash(video_path)  # calling class Dash from dash.py
    cap = cv.VideoCapture(video_path)
    pTime = 0
    if not cap.isOpened():
        print("Error: Unable to open the video file.")
        return

    while True:
        cTime = time.time()
        ret, frame = cap.read()
        if not ret:
            break

        frame, level = dash.dash_detect(frame)  # dash_detect method from Dash class

        if level == 2:
            cv.putText(frame, "far", (10, 170), cv.FONT_HERSHEY_PLAIN, 3,
                       (0, 0, 0), 3)
        elif level == 1:
            cv.putText(frame, "moderate", (10, 170), cv.FONT_HERSHEY_PLAIN, 3,
                       (0, 0, 0), 3)
        elif level == 0:
            cv.putText(frame, "close", (10, 170), cv.FONT_HERSHEY_PLAIN, 3,
                       (0, 0, 0), 3)
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv.putText(frame, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3,
                   (255, 0, 255), 3)

        resized_frame = cv.resize(frame, (1920, 1080))
        cv.imshow('win', resized_frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


play_video("vid1.mp4")
