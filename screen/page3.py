# 동작 비교 페이지 (page3)
import streamlit as st
import sys
import os
import cv2
import tempfile  # 임시 파일을 저장하기 위해 사용
import mimetypes

# 시스템 경로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ultralytics import YOLO
from models.DTWEX import compare_videos
from dtaidistance import dtw
from models.gpt import get_advice_based_on_similarity


# def apply_yolo_to_video(video_path, model):
#     """YOLO 모델을 사용하여 비디오에 keypoints 적용 후 비디오 파일로 저장"""
#     cap = cv2.VideoCapture(video_path)
    
#     if not cap.isOpened():
#         st.error("비디오 파일을 열 수 없습니다.")
#         return None

#     output_dir = os.path.join(os.path.dirname(__file__), '../src/mp4')
#     output_path = os.path.join(output_dir, 'yolo_result.mp4')
    
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = None
    
#     try:
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break
            
#             # YOLO 모델로 프레임 처리
#             results = model(frame, verbose=False)
            
#             # 결과 이미지 렌더링
#             rendered_frame = results[0].plot()
            
#             if out is None:
#                 height, width, _ = rendered_frame.shape
#                 out = cv2.VideoWriter(output_path, fourcc, 30, (width, height))
            
#             # 프레임 저장
#             out.write(rendered_frame)
            
#     finally:
#         cap.release()
#         if out is not None:
#             out.release()
    
#     return output_path

def extract_keypoints_from_video(video_path, model):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        st.error("비디오를 열 수 없습니다.")
        return None

    keypoints_list = []
    frames = []

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

        # YOLO 결과 렌더링
        rendered_frame = results[0].plot()

        # OpenCV 창에 표시
        cv2.imshow("동작 유사도 비교", rendered_frame)

        # 'q'를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    return keypoints_list, frames

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
                dtw_distance = compare_videos(description_video_path, uploaded_video_path, model=model)  # DTW 거리 측정
                
                # # YOLO 모델로 업로드된 비디오에서 keypoints 추출
                # keypoints_list, frames = extract_keypoints_from_video(uploaded_video_path, model)
                
                # # 가장 유사한 동작 이미지 및 가장 비유사한 동작 이미지 추출
                # similar_frame = frames[0]  # 가장 유사한 동작 프레임 (예시로 첫 번째 프레임을 사용)
                # dissimilar_frame = frames[-1]  # 가장 비유사한 동작 프레임 (예시로 마지막 프레임을 사용)

                # # 프레임을 이미지로 저장
                # similar_action_image_path = 'similar_action_image.jpg'
                # dissimilar_action_image_path = 'dissimilar_action_image.jpg'
                # cv2.imwrite(similar_action_image_path, similar_frame)
                # cv2.imwrite(dissimilar_action_image_path, dissimilar_frame)

                # processed_video_path = apply_yolo_to_video(uploaded_video_path, model)

                # st.video(processed_video_path)  # YOLO 처리된 비디오 출력
                
                st.success('유사도 측정 완료!')
                st.write(f"동작 유사도 측정 결과 : {dtw_distance}")  # DTW 거리 출력
                
                # # 이미지 출력
                # st.image(similar_action_image_path, caption="가장 유사한 동작", use_container_width=True)
                # st.image(dissimilar_action_image_path, caption="가장 비유사한 동작", use_container_width=True)


                with st.spinner('동작에 대한 피드백 생성 중...'):
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
    
    # 업로드된 파일의 MIME 타입 확인
    mime_type, _ = mimetypes.guess_type(uploaded_file.name)
    
    if mime_type and mime_type.startswith('video'):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(uploaded_file.read())  # 업로드된 파일을 임시 파일에 저장
            return temp_file.name  # 임시 파일 경로 반환
    else:
        st.error("업로드된 파일은 비디오 파일이어야 합니다.")
        return None