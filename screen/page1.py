# 동작 설명 페이지 (page1)
import streamlit as st
import os

def show():
    st.title("동작 설명 페이지")
    st.write("여기는 동작 설명 페이지입니다.")

    # 동영상 절대 경로 설정
    video_path = os.path.join(os.path.dirname(__file__), '../src/mp4/video2.mp4')

    # 동영상 경로 확인
    if os.path.exists(video_path):
        # 파일을 바이너리로 읽어서 스트림릿에서 재생
        with open(video_path, 'rb') as video_file:
            video_bytes = video_file.read()
            st.video(video_bytes, format="video/mp4")
    else:
        st.error(f"동영상을 찾을 수 없습니다: {video_path}")