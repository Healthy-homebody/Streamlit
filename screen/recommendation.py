import streamlit as st
import os
import json
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.optimize import minimize

import streamlit as st
import os
import numpy as np

def show():
    st.title("🧘‍♀️ 맞춤형 요가 운동 계획 추천")
    st.write("""
    안녕하세요! 🧘‍♂️  
    저는 여러분께 딱 맞는 요가 계획을 추천해드릴 요가 전문가입니다.  
    지금부터 간단한 정보를 입력하시면, 나만의 요가 루틴을 만들어드릴게요!
    """)

    # 사용자 프로필 입력
    with st.form("user_profile"):
        st.subheader("✨ 사용자 프로필 입력")
        age = st.number_input("나이", min_value=10, max_value=100, value=25, help="정확한 추천을 위해 나이를 입력해주세요.")
        gender = st.selectbox("성별", options=["남성", "여성"], help="요가 동작의 강도나 추천을 맞춤화하기 위한 선택입니다.")
        weight = st.number_input("체중(kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
        height = st.number_input("키(cm)", min_value=100, max_value=250, value=170)
        activity_level = st.selectbox("활동 수준", options=["낮음", "중간", "높음"], help="평소 활동량을 선택해주세요.")
        purpose = st.selectbox("요가를 하는 목적", options=[
            "유연성 향상", "체력 및 근력 강화", "스트레스 해소", "균형 감각 향상"
        ])

        submitted = st.form_submit_button("✨ 추천 요가 플랜 받기")

    if submitted:
        user_data = {
            "age": age,
            "gender": gender,
            "weight": weight,
            "height": height,
            "activity_level": activity_level,
            "purpose": purpose
        }

        st.write("💡 입력한 프로필 데이터:")
        st.json(user_data)

        st.write(f"""
        🎉 {user_data["purpose"]}을(를) 목표로 하는 요가 플랜을 준비했습니다!  
        아래 추천 플랜을 확인하시고, 요가를 통해 목표를 성취해보세요!
        """)

        # 운동 계획 추천 생성
        recommended_plan = generate_recommendation(user_data)
        for week, plan in enumerate(recommended_plan, 1):
            st.markdown(f"## 🗓️ Week {week} 요가 플랜")
            for day, exercises in plan.items():
                st.markdown(f"### {day}")
                for exercise in exercises:
                    st.markdown(f"- **{exercise['동작']}**: {exercise['설명']}")

def generate_recommendation(user_data):
    """
    사용자 데이터와 목적에 기반한 요가 운동 계획 추천 시스템.
    """
    yoga_plans = {
        "유연성 향상": [
            {"동작": "로우 런지(Low Lunge)", "설명": "엉덩이와 허벅지를 늘려 유연성을 높입니다."},
            {"동작": "파르브리타 자누 시르사아사나(Revolved Head-to-Knee Pose)", "설명": "척추와 옆구리를 부드럽게 늘려줍니다."},
            {"동작": "런지 사이트 스트레칭(Lunging Side Stretch)", "설명": "허리를 이완시키고 복부를 자극합니다."},
            {"동작": "코브라 자세(Cobra Pose)", "설명": "척추를 강화하고 복부 근육을 스트레칭합니다."},
            {"동작": "차일드 포즈(Child's Pose)", "설명": "허리와 목을 부드럽게 풀어줍니다."}
        ],
        "체력 및 근력 강화": [
            {"동작": "플랭크(Plank)", "설명": "코어와 팔 근력을 강화하는 기본 자세입니다."},
            {"동작": "사이드 플랭크(Side Plank)", "설명": "옆구리와 복부 근육을 강화합니다."},
            {"동작": "전사 자세 1(Warrior Pose I)", "설명": "다리 근육과 균형 감각을 동시에 훈련합니다."},
            {"동작": "전사 자세 2(Warrior Pose II)", "설명": "상체와 하체를 연결하며 힘을 키웁니다."},
            {"동작": "의자 자세(Chair Pose)", "설명": "다리와 등 근육을 단련합니다."}
        ],
        "스트레스 해소": [
            {"동작": "나비 자세(Butterfly Pose)", "설명": "골반과 허벅지를 부드럽게 이완합니다."},
            {"동작": "스핑크스 자세(Sphinx Pose)", "설명": "가슴과 허리를 편안하게 열어줍니다."},
            {"동작": "비둘기 자세(Pigeon Pose)", "설명": "엉덩이와 허리를 깊게 스트레칭합니다."},
            {"동작": "시체 자세(Corpse Pose)", "설명": "몸과 마음을 완전히 휴식하게 만듭니다."},
            {"동작": "고양이-소 자세(Cat-Cow Pose)", "설명": "허리와 척추를 부드럽게 풀어줍니다."}
        ],
        "균형 감각 향상": [
            {"동작": "나무 자세(Tree Pose)", "설명": "균형 감각을 기르고 다리 근력을 강화합니다."},
            {"동작": "독수리 자세(Eagle Pose)", "설명": "집중력을 높이고 관절의 유연성을 키웁니다."},
            {"동작": "반달 자세(Half Moon Pose)", "설명": "몸의 안정성과 균형을 향상시킵니다."},
            {"동작": "바카사나(Crow Pose)", "설명": "팔과 코어 근육을 강화하며 집중력을 높입니다."},
            {"동작": "다리 들어 올리기(Leg Lift Pose)", "설명": "다리 힘과 균형을 동시에 훈련합니다."}
        ]
    }

    selected_plan = yoga_plans.get(user_data["purpose"], yoga_plans["유연성 향상"])
    weekly_plan = []
    for week in range(4):
        week_plan = {}
        for day in ["월요일", "수요일", "금요일"]:
            daily_exercises = np.random.choice(selected_plan, 3, replace=False)
            week_plan[day] = daily_exercises.tolist()
        weekly_plan.append(week_plan)

    return weekly_plan



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
