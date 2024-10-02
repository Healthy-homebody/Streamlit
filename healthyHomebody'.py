import streamlit as st

# 사이드바에서 페이지 선택
page = st.sidebar.selectbox("페이지를 선택하세요", ["main", "page2", "page3", "page4"])

# 제목과 설명 추가
st.title("Healthy homebody")
st.write("집순이 집돌이의 건강 지킴이 서비스")

# 선택한 페이지에 따른 조건부 렌더링
if page == "main":
    st.title("동작 선택 페이지")
    st.write("여기는 동작 선택 페이지입니다.")
    
elif page == "page2":
    st.title("동작 설명 페이지")
    st.write("여기는 동작 설명 페이지입니다.")
    name = st.text_input("이름을 입력하세요")
    age = st.number_input("나이를 입력하세요", min_value=1, max_value=100)
    if st.button("프로필 저장"):
        st.write(f"이름: {name}, 나이: {age}")
    
elif page == "page3":
    st.title("스트레칭 영상 업로드 페이지")
    st.write("여기는 스트레칭 영상 업로드 페이지입니다.")
    option = st.selectbox("설정 옵션을 선택하세요", ["옵션 1", "옵션 2", "옵션 3"])
    st.write(f"선택한 설정: {option}")
    
elif page == "page4":
    st.title("동작 비교 페이지")
    st.write("여기는 동작 비교 페이지입니다.")
    option = st.selectbox("설정 옵션을 선택하세요", ["옵션 1", "옵션 2", "옵션 3"])
    st.write(f"선택한 설정: {option}")