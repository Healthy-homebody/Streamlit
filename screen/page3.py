# 동작 비교 페이지 (page3)
import streamlit as st
import sys
import os
import cv2
import tempfile  # 임시 파일을 저장하기 위해 사용
import mimetypes
import warnings
import torch

# 시스템 경로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ultralytics import YOLO, settings
from models.DTWEX import compare_videos
from dtaidistance import dtw
from models.gpt import get_advice_based_on_similarity

# 환경 변수 처리
os.environ["QT_QPA_PLATFORM"] = "offscreen"

if 'QT_QPA_PLATFORM' in os.environ: # Qt 설정 제거
    os.environ.pop('QT_QPA_PLATFORM')

# Torch 및 일반 경고 무시
warnings.filterwarnings("ignore")
    
try:
    delattr(torch.classes, '_path')
except AttributeError:
    pass

# 설정 초기화 코드 수정
try:
    settings.reset()
except Exception as e:
    print(f"Ultralytics 설정 초기화 중 오류: {e}")

def extract_keypoints_from_video(video_path, model):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        st.error("비디오를 열 수 없습니다.")
        return None

    keypoints_list = []
    frames = []
    processed_frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # YOLO 모델로 keypoints 추출
        results = model(frame, verbose=False)
        keypoints = results[0].keypoints.cpu().numpy() if results[0].keypoints is not None else None

        if keypoints is not None:
            keypoints_list.append(keypoints)
            frames.append(frame)  # 동작이 포함된 프레임 저장
            
            # YOLO 결과 렌더링된 프레임 저장
            rendered_frame = results[0].plot()
            processed_frames.append(rendered_frame)

    cap.release()
    return keypoints_list, frames, processed_frames

def show():
    # 세션 상태 초기화
    if 'similarity_measured' not in st.session_state:
        st.session_state.similarity_measured = False
    
    st.title("동작 비교 페이지")
    st.write("여기는 동작 비교 페이지입니다.")

    # YOLO 모델 로드
    model = YOLO('yolov8m-pose.pt', verbose=False)

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
        col1, col2 = st.columns(2)  # 두 개의 열 생성
        
        with col1:
            if st.button("동작 유사도 측정"):
                # 동작 유사도 측정 중이라는 메시지 표시
                with st.spinner('동작 유사도 측정 중...'):
                    # 키포인트 및 프레임 추출
                    keypoints_list, original_frames, processed_frames = extract_keypoints_from_video(uploaded_video_path, model)
                    
                    # 처리된 프레임 미리보기 (선택적)
                    st.subheader("처리된 프레임 미리보기")
                    if processed_frames:
                        # 처음 몇 프레임만 보여주기
                        preview_frames = processed_frames[:5]
                        preview_images = [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in preview_frames]
                        
                        # 프레임들을 가로로 나란히 표시
                        cols = st.columns(len(preview_images))
                        for col, img in zip(cols, preview_images):
                            col.image(img, use_column_width=True)
                    
                    # DTW 거리 측정
                    dtw_distance = compare_videos(description_video_path, uploaded_video_path, model=model)
                    st.session_state.dtw_distance = dtw_distance  # 측정 결과 저장
                    st.session_state.similarity_measured = True  # 유사도 측정 완료 표시

                st.success('유사도 측정 완료!')
                st.write(f"동작 유사도 측정 결과 : {dtw_distance}")  # DTW 거리 출력

                with st.spinner('동작에 대한 피드백 생성 중...'):
                    advice = get_advice_based_on_similarity(dtw_distance, st.session_state.selected_action)
                    st.session_state.advice = advice  # 조언 저장
                    st.write(f"GPT-4 조언: {advice}")  # GPT-4 조언 출력
                    
        with col2:
            # 동작 유사도 측정이 완료된 경우에만 다음 버튼 활성화
            if st.session_state.similarity_measured and st.button("다음", key="next"):
                st.session_state.selected_page = "recommendation"
                


        # else:
        #     st.write("동작 유사도 측정 결과를 가져오지 못했습니다.")
    
    else:
        st.write("비디오를 선택하거나 업로드해 주세요.")


        
        
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
    
    # 업로드된 파일의 MIME 타입 확인
    mime_type, _ = mimetypes.guess_type(uploaded_file.name)
    
    if mime_type and mime_type.startswith('video'):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(uploaded_file.read())  # 업로드된 파일을 임시 파일에 저장
            return temp_file.name  # 임시 파일 경로 반환
    else:
        st.error("업로드된 파일은 비디오 파일이어야 합니다.")
        return None