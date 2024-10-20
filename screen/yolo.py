from ultralytics.utils.plotting import Annotator
from ultralytics import YOLO
import cv2

# pip install ultralytics
# pip install opencv-python
# pip install torch torchvision torchaudio
# pip install numpy


# # YOLO 모델 초기화
# model = YOLO("../models/yolov8m-pose.pt")  # yolov8m 모델 경로에 맞게 수정

def process_frame(frame):
    """
    비디오 프레임에 YOLO 모델 적용
    """
    # # 모델을 사용하여 추론
    # results = model(frame)
    # result = results[0]

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