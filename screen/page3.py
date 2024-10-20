# 동작 비교 페이지 (page3)
import streamlit as st
import os
import cv2
import tempfile  # 임시 파일을 저장하기 위해 사용
from yolo import process_frame

def process_video_to_file(video_path, output_path):
    """YOLO로 처리한 비디오를 파일로 저장."""
    cap = cv2.VideoCapture(video_path)
    
    # 비디오 속성 가져오기
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # YOLO 처리된 비디오 저장을 위한 VideoWriter 객체 생성
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # YOLO 모델로 프레임 처리
        frame = process_frame(frame)

        # YOLO로 처리된 프레임을 저장
        out.write(frame)

    cap.release()
    out.release()

def save_uploaded_file(uploaded_file):
    """업로드된 비디오 파일을 임시 파일로 저장하고, 그 파일 경로를 반환."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(uploaded_file.read())  # 업로드된 파일을 임시 파일에 저장
        return temp_file.name  # 임시 파일 경로 반환

def show():
    st.title("동작 비교 페이지")
    st.write("여기는 동작 비교 페이지입니다.")

    # 동작 설명 비디오 처리
    if 'selected_action' in st.session_state:
        st.subheader("동작 설명 비디오")
        # video_path = save_uploaded_file(st.session_state.page1_video)

        # # YOLO 처리된 비디오 파일을 임시로 저장
        # with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
        #     yolo_output_path = temp_video_file.name
        #     process_video_to_file(video_path, yolo_output_path)  # YOLO 처리된 비디오 저장
            
        #     # YOLO 처리된 비디오 재생
        #     st.video(yolo_output_path)
        action_info = {
            "로우 런지(Low Lunge)": '../src/mp4/video1.mp4',
            "파르브리타 자누 시르사아사나(Revolved Head-to-Knee Pose)": '../src/mp4/video6.mp4',
            "선 활 자세(Standing Split)": '../src/mp4/video3.mp4',
            "런지 사이트 스트레칭(Lunging Side Stretch)": '../src/mp4/video4.mp4'
        }
        video_path = os.path.join(os.path.dirname(__file__), action_info[st.session_state.selected_action])
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.write("비디오 파일을 찾을 수 없습니다.")
    else:
        st.subheader("동작 설명 비디오")
        st.write("비디오가 없습니다.")

    # 사용자 업로드 비디오 처리
    if 'uploaded_video' in st.session_state:
        st.subheader("사용자 업로드 비디오")
        st.video(st.session_state.uploaded_video)
        # uploaded_video_path = save_uploaded_file(st.session_state.uploaded_video)

        # # YOLO 처리된 비디오 파일을 임시로 저장
        # with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
        #     yolo_output_path = temp_video_file.name
        #     process_video_to_file(uploaded_video_path, yolo_output_path)  # YOLO 처리된 비디오 저장
            
        #     # YOLO 처리된 비디오 재생
        #     st.video(yolo_output_path)
    else:
        st.subheader("사용자 업로드 비디오")
        st.write("업로드된 동영상이 없습니다.")

    if st.button("완료", key="finish"):
        st.session_state.selected_page = "main"  # 완료 버튼 클릭 시 main 페이지로 이동