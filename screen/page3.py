# 동작 비교 페이지 (page3)
import streamlit as st

def show():
    st.title("동작 비교 페이지")
    st.write("여기는 동작 비교 페이지입니다.")

    col1, col2 = st.columns(2)  # 두 개의 열로 나누기

    # page1에서 저장한 동영상 가져오기
    if 'page1_video' in st.session_state:
        with col1:
            st.subheader("동작 설명 비디오")
            st.video(st.session_state.page1_video)  # page1에서 비디오 재생
    else:
        with col1:
            st.subheader("동작 설명 비디오")
            st.write("비디오가 없습니다.")

    # 세션 상태에서 업로드한 동영상 가져오기
    if 'uploaded_video' in st.session_state:
        with col2:
            st.subheader("사용자 업로드 비디오")
            st.video(st.session_state.uploaded_video)  # 업로드된 비디오 재생
    else:
        with col2:
            st.subheader("사용자 업로드 비디오")
            st.write("업로드된 동영상이 없습니다.")

    if st.button("완료", key="finish"):
        st.session_state.selected_page = "main"  # 완료 버튼 클릭 시 main 페이지로 이동
