# 스트레칭 영상 업로드 페이지 (page2)
import streamlit as st

def show():
    st.title("스트레칭 영상 업로드 페이지")
    st.write("여기는 스트레칭 영상 업로드 페이지입니다.")

    # 파일 업로드 기능 추가
    uploaded_file = st.file_uploader("파일 선택(mp4)", type=["mp4"])

    if uploaded_file is not None:
        # 업로드된 파일 처리 (여기서는 파일 이름과 타입을 출력)
        st.write("업로드된 파일:", uploaded_file.name)
        st.write("파일 타입:", uploaded_file.type)

        # 동영상 재생
        st.video(uploaded_file)