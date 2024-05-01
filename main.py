import cv2 as cv
from ultralytics import YOLO
import time
import supervision as sv
import numpy as np
np.bool = np.bool_

y = 100
model = YOLO("yolov8s.pt")
polygon = np.array([
    [550, 350],
    [650, 350],
    [1000, 600],
    [200, 600]
])


# ------------------------------------------------------ZONE------------------------------------------------------------
x = [sv.Color(r=255, g=0, b=0), sv.Color(r=255, g=255, b=0), sv.Color(r=0, g=255, b=0)]
polygons = [
    np.array([
        [460, 450],
        [740, 450],
        [900, 550],
        [300, 550]
    ], np.int32),
    np.array([
        [530, 373],
        [670, 373],
        [740, 447],
        [460, 447]
    ], np.int32),
    np.array([
        [570, 330],
        [630, 330],
        [670, 370],
        [530, 370]
    ], np.int32)
]
video_info = sv.VideoInfo.from_video_path("dash.mp4")

zones = [
    sv.PolygonZone(
        polygon=polygon,
        frame_resolution_wh=video_info.resolution_wh
    )
    for polygon
    in polygons
]
zone_annotators = [
    sv.PolygonZoneAnnotator(
        zone=zone,
        color=x[index],
        thickness=1,
        text_thickness=1,
        text_scale=0.5,
        text_padding=0
    )
    for index, zone
    in enumerate(zones)
]
box_annotators = [
    sv.BoxAnnotator(
        color=x[index],
        thickness=1,
        text_thickness=1,
        text_scale=0.25,
        text_padding=0

    )
    for index
    in range(len(polygons))
]
# ----------------------------------------------------------------------------------------------------------------------

selected_classes = [0, 1, 2, 3, 5, 7]


def play_video(video_path):
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
        results = model(frame, imgsz=1280)[0]
        detections = sv.Detections.from_ultralytics(results)
        detections = detections[np.isin(detections.class_id, selected_classes)]
        detections = detections[detections.confidence > 0.5]

        for zone, zone_annotator, box_annotator in zip(zones, zone_annotators, box_annotators):
            mask = zone.trigger(detections=detections)
            detections_filtered = detections[mask]
            labels = []
            for detection in detections_filtered:
                _, _, confidence, class_id, _, _ = detection
                class_name = model.names[class_id]
                label = f"{class_name} {confidence:0.2f}"
                labels.append(label)
            frame = box_annotator.annotate(scene=frame, detections=detections_filtered,labels=labels)
            frame = zone_annotator.annotate(scene=frame)

        # zone.trigger(detections=detections)
        # # labels = [f"{model.names[class_id]} {confidence:0.2f}" for _, confidence, class_id, _ in detections]
        #
        # labels = []
        #
        # for detection in detections:
        #     _, _, confidence, class_id, _, _ = detection
        #     class_name = model.names[class_id]
        #     label = f"{class_name} {confidence:0.2f}"
        #     labels.append(label)
        # frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)
        # frame = zone_annotator.annotate(scene=frame)
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


play_video("dash.mp4")

# play_video(0)
