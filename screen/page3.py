import streamlit as st
import sys
import os
import numpy as np
import tempfile  # 임시 파일을 저장하기 위해 사용
import mimetypes
from dotenv import load_dotenv
import openai
import logging

# 시스템 경로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ultralytics import YOLO
from models.DTWEX import compare_videos
from models.gpt import get_advice_based_on_similarity

# .env 파일 로드
load_dotenv()

# 로그 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# OpenAI API 키 설정
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    openai.api_key = api_key

def extract_keypoints_from_video(video_path, model):
    """
    비디오에서 키포인트를 안전하게 추출하는 함수
    """
    try:
        keypoints_list = []
        processed_frames = []

        # 모든 프레임을 한 번에 로드하는 대신 점진적으로 처리
        with st.spinner('키포인트 추출 중...'):
            cap = model.predictor(video_path, stream=True, verbose=False)
            
            for result in cap:
                if result.keypoints is not None:
                    keypoints = result.keypoints.cpu().numpy()
                    keypoints_list.append(keypoints)
                    
                    # 프레임 처리 결과를 numpy 배열로 변환
                    rendered_frame = result.plot()
                    processed_frames.append(rendered_frame)
                    
                    # 메모리 관리를 위해 5개의 프레임만 저장
                    if len(processed_frames) > 5:
                        processed_frames = processed_frames[-5:]

        return keypoints_list, processed_frames
    
    except Exception as e:
        st.error(f"키포인트 추출 중 오류 발생: {e}")
        logging.error(f"키포인트 추출 오류: {e}")
        return None, None

def show():
    st.title("동작 비교 페이지")

    # 세션 상태 초기화
    if 'similarity_measured' not in st.session_state:
        st.session_state.similarity_measured = False
    
    # YOLO 모델 로드 (캐싱)
    @st.cache_resource
    def load_yolo_model():
        return YOLO('yolov8m-pose.pt')
    
    model = load_yolo_model()

    # 동작 설명 비디오 처리
    if 'selected_action' in st.session_state:
        st.subheader("동작 설명 비디오")

        action_info = {
            "로우 런지(Low Lunge)": '../src/mp4/video1.mp4',
            "파르브리타 자누 시르사아사나(Revolved Head-to-Knee Pose)": '../src/mp4/video6.mp4',
            "선 활 자세(Standing Split)": '../src/mp4/video3.mp4',
            "런지 사이트 스트레칭(Lunging Side Stretch)": '../src/mp4/video4.mp4'
        }
        
        try:
            video_path = os.path.join(os.path.dirname(__file__), action_info[st.session_state.selected_action])
            if os.path.exists(video_path):
                st.video(video_path)
                description_video_path = video_path
            else:
                st.warning("비디오 파일을 찾을 수 없습니다.")
                description_video_path = None
        except Exception as e:
            st.error(f"비디오 처리 중 오류: {e}")
            description_video_path = None
    else:
        st.warning("비디오가 없습니다.")
        description_video_path = None

    # 사용자 업로드 비디오 처리
    if 'uploaded_video' in st.session_state:
        st.subheader("사용자 업로드 비디오")
        st.video(st.session_state.uploaded_video)
        uploaded_video_path = save_uploaded_file(st.session_state.uploaded_video)
    else:
        st.warning("업로드된 동영상이 없습니다.")
        uploaded_video_path = None

    # 동작 유사도 측정 버튼
    if description_video_path and uploaded_video_path:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("동작 유사도 측정"):
                try:
                    with st.spinner('동작 유사도 측정 중...'):
                        # 키포인트 및 프레임 추출
                        keypoints_list, processed_frames = extract_keypoints_from_video(uploaded_video_path, model)
                        
                        # 처리된 프레임 미리보기
                        st.subheader("처리된 프레임 미리보기")
                        if processed_frames:
                            preview_images = [frame for frame in processed_frames]
                            cols = st.columns(len(preview_images))
                            for col, img in zip(cols, preview_images):
                                col.image(img, channels='BGR', use_column_width=True)
                        
                        # DTW 거리 측정
                        dtw_distance = compare_videos(description_video_path, uploaded_video_path, model=model)
                        st.session_state.dtw_distance = dtw_distance
                        st.session_state.similarity_measured = True

                        st.success('유사도 측정 완료!')
                        st.write(f"동작 유사도 측정 결과: {dtw_distance}")
                        
                        with st.spinner('동작에 대한 피드백 생성 중...'):
                            advice = get_advice_based_on_similarity(dtw_distance, st.session_state.selected_action)
                            st.session_state.advice = advice
                            st.write(f"GPT-4 조언: {advice}")
                            
                except Exception as e:
                    st.error(f"유사도 측정 중 오류 발생: {e}")
                    logging.error(f"유사도 측정 오류: {e}")
        
        with col2:
            if st.session_state.similarity_measured and st.button("다음"):
                st.session_state.selected_page = "recommendation"
    
    else:
        st.warning("비디오를 선택하거나 업로드해 주세요.")

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
    """업로드된 비디오 파일을 안전하게 저장"""
    try:
        mime_type, _ = mimetypes.guess_type(uploaded_file.name)
        
        if mime_type and mime_type.startswith('video'):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                temp_file.write(uploaded_file.read())
                return temp_file.name
        else:
            st.error("업로드된 파일은 비디오 파일이어야 합니다.")
            return None
    except Exception as e:
        st.error(f"파일 저장 중 오류: {e}")
        return None