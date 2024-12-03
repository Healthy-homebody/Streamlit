# 동작 비교 페이지 (page3)
import streamlit as st
import sys
import os
import cv2
import tempfile  # 임시 파일을 저장하기 위해 사용
import mimetypes
from ultralytics import YOLO
from models.DTWEX import compare_videos
from dtaidistance import dtw
from models.gpt import get_advice_based_on_similarity

# 시스템 경로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def process_and_save_video(input_video_path, output_video_path, model):
    """
    YOLO 모델을 사용하여 입력 비디오를 처리하고 결과를 저장합니다.
    """
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        st.error("비디오를 열 수 없습니다.")
        return None

    # 비디오 저장 설정
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # H.264 코덱 사용 (더 안정적인 비디오 형식)
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height), isColor=True)

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_count == 0:
        st.error("비디오에 프레임이 없습니다.")
        return None

    progress_bar = st.progress(0)

    processed_frames = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # YOLO 포즈 추정
            results = model(frame, verbose=False)
            
            # 결과 시각화
            processed_frame = results[0].plot() if results else frame

            # 프레임 저장
            out.write(processed_frame)
            processed_frames += 1

            # 진행 상태 업데이트
            progress_bar.progress(processed_frames / frame_count)

    except Exception as e:
        st.error(f"비디오 처리 중 오류 발생: {e}")
    finally:
        cap.release()
        out.release()
        progress_bar.empty()

    # 처리된 비디오 파일 존재 확인
    if os.path.exists(output_video_path) and os.path.getsize(output_video_path) > 0:
        st.success(f"총 {processed_frames}개 프레임 처리 완료")
        return output_video_path
    else:
        st.error("비디오 처리에 실패했습니다.")
        return None

def save_uploaded_file(uploaded_file):
    """
    업로드된 비디오 파일을 임시 파일로 저장합니다.
    """
    if not uploaded_file:
        st.warning("업로드된 파일이 없습니다.")
        return None

    mime_type, _ = mimetypes.guess_type(uploaded_file.name)
    if mime_type and mime_type.startswith('video'):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(uploaded_file.read())
            return temp_file.name
    else:
        st.error("비디오 파일만 업로드 가능합니다.")
        return None

def show():
    # 세션 상태 초기화
    if 'similarity_measured' not in st.session_state:
        st.session_state.similarity_measured = False

    st.title("동작 비교 페이지")
    st.write("여기는 동작 비교 페이지입니다.")

    # YOLO 모델 로드
    try:
        model = YOLO('yolov8m-pose.pt')
    except Exception as e:
        st.error(f"YOLO 모델을 로드할 수 없습니다: {e}")
        return

    # 사용자 업로드 비디오 처리
    uploaded_video = st.file_uploader("비디오를 업로드하세요", type=["mp4", "avi", "mov"])
    if uploaded_video is not None:
        uploaded_video_path = save_uploaded_file(uploaded_video)
        if uploaded_video_path:
            st.video(uploaded_video_path)  # 업로드된 비디오 재생

            # YOLO 처리된 비디오 저장 경로
            processed_video_path = os.path.join(tempfile.gettempdir(), "processed_video.mp4")

            # YOLO 처리 및 저장
            st.info("YOLO 모델을 사용하여 비디오를 처리 중입니다...")
            processed_video_path = process_and_save_video(uploaded_video_path, processed_video_path, model)

            if processed_video_path:
                st.success("YOLO 처리 완료! 아래에서 확인하세요.")
                st.video(processed_video_path)  # 처리된 비디오 재생
            
                with st.spinner('동작에 대한 피드백 생성 중...'):
                    # GPT-4 모델을 통해 피드백 제공
                    advice = get_advice_based_on_similarity(dtw_distance, st.session_state.selected_action)
                    st.write(f"GPT-4 조언: {advice}")  # GPT-4 조언 출력
                    
            else:
                st.error("YOLO 처리가 실패했습니다.")
                
            # 동작 유사도 측정이 완료된 경우에만 다음 버튼 활성화
            if st.session_state.similarity_measured and st.button("다음", key="next"):
                st.session_state.selected_page = "recommendation"
    else:
        st.warning("비디오를 업로드해 주세요.")

        
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
    """
    업로드된 비디오 파일을 임시 파일로 저장하고, 그 파일 경로를 반환.
    """
    # 파일이 업로드되지 않은 경우 처리
    if uploaded_file is None:
        st.warning("업로드된 파일이 없습니다.")
        return None

    # 파일의 MIME 타입 확인
    mime_type, _ = mimetypes.guess_type(uploaded_file.name)
    if mime_type and mime_type.startswith('video'):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                temp_file.write(uploaded_file.read())  # 업로드된 파일을 임시 파일에 저장
                return temp_file.name  # 임시 파일 경로 반환
        except Exception as e:
            st.error(f"파일 저장 중 오류 발생: {e}")
            return None
    else:
        st.error("업로드된 파일은 비디오 파일이어야 합니다.")
        return None