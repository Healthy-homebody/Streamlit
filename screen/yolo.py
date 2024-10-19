from ultralytics.utils.plotting import Annotator
from ultralytics import YOLO
import cv2

# pip install ultralytics
# pip install opencv-python
# pip install torch torchvision torchaudio
# pip install numpy


# YOLO 모델 초기화
model = YOLO("../models/yolov8m-pose.pt")  # yolov8m 모델 경로에 맞게 수정

def process_frame(frame):
    """
    비디오 프레임에 YOLO 모델 적용
    """
    # 모델을 사용하여 추론
    results = model(frame)
    result = results[0]

    # 경계 상자와 키 포인트 그리기
    frame = draw_boxes(result, frame)
    frame = draw_keypoints(result, frame)
    return frame

def draw_boxes(result, frame):
    """
    경계 상자 그리기 함수
    """
    for boxes in result.boxes:
        x1, y1, x2, y2, score, cls = boxes.data.squeeze().cpu().numpy()
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    return frame

def draw_keypoints(result, frame):
    """
    키 포인트 그리기 함수
    """
    for kps in result.keypoints:
        kps = kps.data.squeeze().cpu().numpy()
        for idx, (x, y, score) in enumerate(kps):
            if score > 0.5:  # 신뢰도 0.5 이상일 때만 표시
                cv2.circle(frame, (int(x), int(y)), 3, (0, 0, 255), cv2.FILLED)
    return frame