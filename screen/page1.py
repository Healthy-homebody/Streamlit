# 동작 설명 페이지 (page1)
import streamlit as st
import os

def show():
    st.title("동작 설명 페이지")
    
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
    
    # 동작 설명 및 동영상 정보 딕셔너리
    action_info = {
        "기본 필라테스": {
            "title" : "기본 필라테스",
            "description": "기본 필라테스 동작입니다. 기초를 다지는 데 도움을 줍니다.",
            "video_path": os.path.join(os.path.dirname(__file__), '../src/mp4/video2.mp4')  # 기본 필라테스 동영상 경로
        },
        "상체 필라테스": {
            "title" : "상체 필라테스",
            "description": "상체를 강화하는 동작입니다.",
            "video_path": os.path.join(os.path.dirname(__file__), '../src/mp4/video2.mp4')  # 상체 필라테스 동영상 경로
        },
        "하체 필라테스": {
            "title" : "하체 필라테스",
            "description": "하체를 강화하는 동작입니다.",
            "video_path": os.path.join(os.path.dirname(__file__), '../src/mp4/video2.mp4'),  # 하체 필라테스 동영상 경로
        },
        "전신 필라테스": {
            "title" : "전신 필라테스",
            "description": "전신을 아우르는 동작입니다.",
            "video_path": os.path.join(os.path.dirname(__file__), '../src/mp4/video2.mp4')  # 전신 필라테스 동영상 경로
        }
    }
    
    selected_action = st.session_state.selected_action
    st.write(action_info[selected_action]["title"])  

    
    # 동영상 경로 확인
    video_path = action_info[selected_action]["video_path"]
    if os.path.exists(video_path):
        # 파일을 바이너리로 읽어서 스트림릿에서 재생
        with open(video_path, 'rb') as video_file:
            video_bytes = video_file.read()
            st.video(video_bytes, format="video/mp4")
    else:
        st.error(f"동영상을 찾을 수 없습니다: {video_path}")

    col1, col2 = st.columns([1, 1])  
    with col1:
        if st.button("이전", key="previous"):
            st.session_state.selected_page = "main"  # 이전 버튼 클릭 시 main 페이지로 이동

    with col2:
        if st.button("다음", key="next"):
            st.session_state.selected_page = "page2"  # 다음 버튼 클릭 시 page2로 이동

    st.write(action_info[selected_action]["description"])  