# 필라테스 동작 선택 페이지 (main)
import streamlit as st
import page1
import page2
import page3

# streamlit run screen/main.py

# 사이드바에서 페이지 선택
page = st.sidebar.selectbox("페이지를 선택하세요", ["main", "page1", "page2", "page3"])

# 조건부 렌더링을 통해 각 페이지 파일을 불러옴
if page == "main":
    st.title("집순이 집돌이의 건강 지킴이 서비스")
    st.write("필라테스 동작을 선택해주세요")

elif page == "page1":
    page1.show()

elif page == "page2":
    page2.show()

elif page == "page3":
    page3.show()
