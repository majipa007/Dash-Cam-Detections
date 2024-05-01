import cv2 as cv
from ultralytics import YOLO
import time

model = YOLO("yolov8s.pt")


def play_video(video_path):
    cap = cv.VideoCapture(video_path)
    cTime = 0
    pTime = 0
    if not cap.isOpened():
        print("Error: Unable to open the video file.")
        return

    while True:
        cTime = time.time()
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame, conf=0.4)
        print(len(results))
        x = 0
        for result in results:
            for i in result.boxes:
                x1, y1, x2, y2 = i.xyxy[0]
                cv.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 255), 2)
                cv.putText(frame, "Fish", (int(x1), int(y1)), cv.FONT_HERSHEY_PLAIN, 2,
                           (255, 0, 255), 2)
                x = x+len(results)
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv.putText(frame, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3,
                   (255, 0, 255), 3)
        # cv.putText(frame, str(x), (50,50), cv.FONT_HERSHEY_PLAIN, 5,
        #            (255, 255, 0), 5)

        resized_frame = cv.resize(frame, (1920, 1080))
        cv.imshow('win', resized_frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


play_video("mall.mp4")

# play_video(0)
