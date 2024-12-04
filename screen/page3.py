# 동작 비교 페이지 (page3)
import streamlit as st
import sys
import os
import cv2
import tempfile
import mimetypes
import warnings
import torch
import concurrent.futures

# 시스템 경로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ultralytics import YOLO, settings
from models.DTWEX import compare_videos
from dtaidistance import dtw
from models.gpt import get_advice_based_on_similarity

# 환경 변수 및 경고 설정
os.environ["QT_QPA_PLATFORM"] = "offscreen"
warnings.filterwarnings("ignore")

# Ultralytics 로깅 설정
try:
    from ultralytics.yolo.utils import LOGGER
    LOGGER.setLevel("WARNING")
    settings.reset()
except Exception as e:
    print(f"Ultralytics 설정 초기화 중 오류: {e}")

# 모델 캐싱
@st.cache_resource
def load_yolo_model():
    return YOLO('yolov8m-pose.pt', verbose=False)

# 비디오 전처리 및 키포인트 추출 최적화
@st.cache_data
def extract_keypoints_from_video(_video_path, _model):
    cap = cv2.VideoCapture(_video_path)
    if not cap.isOpened():
        st.error("비디오를 열 수 없습니다.")
        return None, None, None

    keypoints_list = []
    frames = []
    processed_frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 프레임 크기 조정 (성능 최적화)
        frame = cv2.resize(frame, (640, 480))

        results = _model(frame, verbose=False)
        keypoints = results[0].keypoints.cpu().numpy() if results[0].keypoints is not None else None

        if keypoints is not None:
            keypoints_list.append(keypoints)
            frames.append(frame)
            rendered_frame = results[0].plot()
            processed_frames.append(rendered_frame)

    cap.release()
    return keypoints_list, frames, processed_frames

# 비동기 비디오 처리 함수
@st.cache_data
def process_video_async(description_video_path, uploaded_video_path, _model):
    def compute_similarity():
        # 키포인트 및 프레임 추출
        keypoints_list, original_frames, processed_frames = extract_keypoints_from_video(uploaded_video_path, _model)
        
        # DTW 거리 측정
        dtw_distance = compare_videos(description_video_path, uploaded_video_path, model=_model)
        
        # 조언 생성
        advice = get_advice_based_on_similarity(dtw_distance, st.session_state.selected_action)
        
        return dtw_distance, advice, processed_frames

    try:
        dtw_distance, advice, processed_frames = compute_similarity()
        return dtw_distance, advice, processed_frames
    except Exception as e:
        st.error(f"분석 중 오류 발생: {e}")
        return None, None, None

def save_uploaded_file(uploaded_file):
    """업로드된 비디오 파일을 임시 파일로 저장하고, 그 파일 경로를 반환."""
    mime_type, _ = mimetypes.guess_type(uploaded_file.name)
    
    # 파일 크기 제한 (최대 10MB)
    if uploaded_file.size > 10 * 1024 * 1024:
        st.error("파일 크기가 너무 큽니다. 10MB 이하의 파일을 업로드해주세요.")
        return None
    
    if mime_type and mime_type.startswith('video'):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(uploaded_file.read())
            return temp_file.name
    else:
        st.error("업로드된 파일은 비디오 파일이어야 합니다.")
        return None

def show():
    # 세션 상태 초기화
    if 'similarity_measured' not in st.session_state:
        st.session_state.similarity_measured = False
    
    st.title("동작 비교 페이지")
    st.write("여기는 동작 비교 페이지입니다.")

    # YOLO 모델 로드
    model = load_yolo_model()

    # 동작 설명 비디오 처리
    description_video_path = None
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
            description_video_path = video_path
        else:
            st.write("비디오 파일을 찾을 수 없습니다.")
    else:
        st.subheader("동작 설명 비디오")
        st.write("비디오가 없습니다.")

    # 사용자 업로드 비디오 처리
    uploaded_video_path = None
    if 'uploaded_video' in st.session_state:
        st.subheader("사용자 업로드 비디오")
        st.video(st.session_state.uploaded_video)
        uploaded_video_path = save_uploaded_file(st.session_state.uploaded_video)
    else:
        st.subheader("사용자 업로드 비디오")
        st.write("업로드된 동영상이 없습니다.")

    # 동작 유사도 측정 버튼
    if description_video_path and uploaded_video_path:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("동작 유사도 측정"):
                # 진행 상태 프로그레스 바
                progress_bar = st.progress(0)
                
                try:
                    # 단계별 진행 상태 표시
                    progress_bar.progress(10)
                    result = process_video_async(description_video_path, uploaded_video_path, model)
                    
                    if result[0] is not None:
                        dtw_distance, advice, processed_frames = result
                        
                        progress_bar.progress(50)
                        
                        # 처리된 프레임 미리보기
                        if processed_frames:
                            preview_frames = processed_frames[:5]
                            preview_images = [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in preview_frames]
                            
                            cols = st.columns(len(preview_images))
                            for col, img in zip(cols, preview_images):
                                col.image(img, use_column_width=True)
                        
                        progress_bar.progress(80)
                        
                        # 세션 상태 업데이트
                        st.session_state.dtw_distance = dtw_distance
                        st.session_state.similarity_measured = True
                        st.session_state.advice = advice
                        
                        progress_bar.progress(100)
                        
                        st.success('유사도 측정 완료!')
                        st.write(f"동작 유사도 측정 결과 : {dtw_distance}")
                        st.write(f"GPT-4 조언: {advice}")
                    
                except Exception as e:
                    st.error(f"분석 중 오류 발생: {e}")
                
                finally:
                    # 진행 표시줄 제거
                    progress_bar.empty()

        with col2:
            # 동작 유사도 측정이 완료된 경우에만 다음 버튼 활성화
            if st.session_state.similarity_measured and st.button("다음", key="next"):
                st.session_state.selected_page = "recommendation"

    else:
        st.write("비디오를 선택하거나 업로드해 주세요.")

# CSS 로딩 함수
def load_css(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"CSS 파일을 찾을 수 없습니다: {file_path}")

# CSS 파일 경로
css_path = os.path.join(os.path.dirname(__file__), '../src/styles.css')

# CSS 로드 및 적용
st.markdown(f"<style>{load_css(css_path)}</style>", unsafe_allow_html=True)