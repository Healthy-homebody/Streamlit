# 동작 비교 페이지 (page3)
import streamlit as st
import sys
import os
import tempfile

# 시스템 경로 추가 (Windows 경로 형식 사용)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from ultralytics import YOLO
from models.DTWEX import compare_videos
from dtaidistance import dtw
from models.gpt import get_advice_based_on_similarity  # gpt 모듈 임포트

# OpenCV import with error handling
try:
    import cv2
except ImportError:
    st.error("OpenCV를 불러올 수 없습니다. 시스템 관리자에게 문의하세요.")
    cv2 = None

def show():
    st.title("동작 비교 페이지")
    st.write("여기는 동작 비교 페이지입니다.")

    # YOLO 모델 로드
    model = YOLO('yolov8n-pose.pt')

    # 동작 설명 비디오 처리
    if 'selected_action' in st.session_state:
        st.subheader("동작 설명 비디오")

        action_info = {
            "로우 런지(Low Lunge)": '../src/mp4/video1.mp4',
            "파르브리타 자누 시르사아사나(Revolved Head-to-Knee Pose)": '../src/mp4/video6.mp4',
            "선 활 자세(Standing Split)": '../src/mp4/video3.mp4',
            "런지 사이트 스트레칭(Lunging Side Stretch)": '../src/mp4/video4.mp4'
        }
        video_path = os.path.join(os.path.dirname(__file__), action_info[st.session_state.selected_action])
        if os.path.exists(video_path):
            st.video(video_path)
            description_video_path = video_path  # 설명 비디오 경로 저장
        else:
            st.write("비디오 파일을 찾을 수 없습니다.")
            description_video_path = None  # 비디오 경로가 없으면 None으로 설정
    else:
        st.subheader("동작 설명 비디오")
        st.write("비디오가 없습니다.")
        description_video_path = None

    # 사용자 업로드 비디오 처리
    if 'uploaded_video' in st.session_state:
        st.subheader("사용자 업로드 비디오")
        st.video(st.session_state.uploaded_video)
        uploaded_video_path = save_uploaded_file(st.session_state.uploaded_video)
    else:
        st.subheader("사용자 업로드 비디오")
        st.write("업로드된 동영상이 없습니다.")
        uploaded_video_path = None

    # 동작 유사도 측정 버튼
    if description_video_path and uploaded_video_path:
        if st.button("동작 유사도 측정"):
            # 동작 유사도 측정 중이라는 메시지 표시
            with st.spinner('동작 유사도 측정 중...'):
                # 유사도 측정을 위해 DTW 모델 적용
                dtw_distance = compare_videos(description_video_path, uploaded_video_path, model=model)  # DTW 거리 반환
                
            st.success('유사도 측정 완료!')
            if dtw_distance is not None:
                st.write(f"동작 유사도 측정 결과 : {dtw_distance}")  # DTW 거리 출력

                with st.spinner('동작에 대한 피드백 생성 중...'):
                    # GPT-4 모델을 통해 피드백 제공
                    advice = get_advice_based_on_similarity(dtw_distance, st.session_state.selected_action)
                    st.write(f"GPT-4 조언: {advice}")  # GPT-4 조언 출력
            else:
                st.write("동작 유사도 측정 결과를 가져오지 못했습니다.")
    else:
        st.write("비디오를 선택하거나 업로드해 주세요.")

    if st.button("완료", key="finish"):
        st.session_state.selected_page = "main"  # 완료 버튼 클릭 시 main 페이지로 이동
        
        
        
def load_css(file_path):
    """CSS 파일 내용을 읽어 반환"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"CSS 파일을 찾을 수 없습니다: {file_path}")
    
# CSS 파일 경로
css_path = os.path.join(os.path.dirname(__file__), '../src/styles.css')

# CSS 로드 및 적용
st.markdown(f"<style>{load_css(css_path)}</style>", unsafe_allow_html=True)

def save_uploaded_file(uploaded_file):
    """업로드된 비디오 파일을 임시 파일로 저장하고, 그 파일 경로를 반환."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(uploaded_file.read())  # 업로드된 파일을 임시 파일에 저장
        return temp_file.name  # 임시 파일 경로 반환
