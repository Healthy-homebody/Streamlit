# 스트레칭 영상 업로드 페이지 (page2)
import streamlit as st

def show():
    st.title("스트레칭 영상 업로드 페이지")
    st.write("여기는 스트레칭 영상 업로드 페이지입니다.")
    
    # 버튼 스타일 적용
    button_style = """
        <style>
        .stButton button {
            width: 80%;
            height: 50px;
            font-size: 18px;
        }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)

    # 파일 업로드 기능 추가
    uploaded_file = st.file_uploader("파일 선택(mp4)", type=["mp4"])

    if uploaded_file is not None:
        # 업로드된 파일 처리 (여기서는 파일 이름과 타입을 출력)
        st.write("업로드된 파일:", uploaded_file.name)
        st.write("파일 타입:", uploaded_file.type)

        # 업로드된 파일을 세션 상태에 저장
        st.session_state.uploaded_video = uploaded_file  # 업로드한 비디오를 세션 상태에 저장

        # 동영상 재생
        st.video(uploaded_file)
        
    col1, col2 = st.columns([1, 1])  
    
    # 이전 버튼 (CSS를 통해 스타일 적용)
    with col1:
        if st.button("이전", key="previous"):
            st.session_state.selected_page = "page1"  # 이전 버튼 클릭 시 page1 페이지로 이동

    # 다음 버튼 (CSS를 통해 스타일 적용)
    with col2:
        if st.button("다음", key="next"):
            st.session_state.selected_page = "page3"  # 다음 버튼 클릭 시 page3로 이동
