# 필라테스 동작 선택 페이지 (main)
import streamlit as st
import os

import page1
import page2
import page3

# streamlit run screen/main.py

icon_path = os.path.join(os.path.dirname(__file__), '../src/images/logo.jpg')

# 페이지 아이콘 설정
st.set_page_config(
    page_title="healthy_homebody",
    page_icon=icon_path
)

# 사이드바에서 페이지 선택
page = st.sidebar.selectbox("페이지를 선택하세요", ["main", "page1", "page2", "page3"])

# 조건부 렌더링을 통해 각 페이지 파일을 불러옴
if page == "main":
    st.title("집순이 집돌이의 건강 지킴이 서비스")
    st.write("필라테스 동작을 선택해주세요")

    # 필라테스 동작 버튼 리스트
    actions = ["기본 필라테스", "상체 필라테스", "하체 필라테스", "전신 필라테스"]

    # 각 동작에 대한 버튼 생성
    col1, col2 = st.columns(2)  # 버튼을 두 개의 열로 나눠서 보여주기
    with col1:
        if st.button("기본 필라테스"):
            st.session_state.selected_action = "기본 필라테스"

        if st.button("상체 필라테스"):
            st.session_state.selected_action = "상체 필라테스"

    with col2:
        if st.button("하체 필라테스"):
            st.session_state.selected_action = "하체 필라테스"

        if st.button("전신 필라테스"):
            st.session_state.selected_action = "전신 필라테스"


# 조건부 렌더링을 통해 각 페이지 파일을 불러옴
if page == "page1":
    page1.show()
elif page == "page2":
    page2.show()
elif page == "page3":
    page3.show()