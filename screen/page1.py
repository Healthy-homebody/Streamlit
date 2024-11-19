import streamlit as st
import os

def show():
    st.title("동작 설명 페이지")
    
    # 동작 설명 및 동영상 정보 딕셔너리
    action_info = {
        "로우 런지(Low Lunge)": {
            "title": "로우 런지(Low Lunge)",
            "description": [
                ("자세 설명", [
                    "• 앞쪽 무릎을 직각으로 굽히고, 뒷다리는 뒤로 뻗습니다.",
                    "• 상체를 곧게 세운 상태로 양손을 합장하거나 허리에 둡니다."
                ]),
                ("효과", [
                    "• 고관절의 유연성 향상",
                    "• 하체 근육 강화",
                    "• 고관절과 허벅지 앞쪽 근육 스트레칭"
                ]),
                ("주의사항", [
                    "• 무릎에 무리가 가지 않도록 주의합니다.",
                    "• 균형을 잃지 않도록 천천히 동작을 수행합니다."
                ]),
                ("실행 방법", [
                    "1. 한 발을 앞으로 크게 내딛습니다.",
                    "2. 뒷발은 뒤꿈치를 들어 올립니다.",
                    "3. 앞무릎이 발목 위에 오도록 자세를 잡습니다.",
                    "4. 상체를 곧게 세우고 호흡을 깊게 유지합니다."
                ])
            ],
            "video_path": os.path.join(os.path.dirname(__file__), '../src/mp4/video1.mp4')
        },
        "파르브리타 자누 시르사아사나(Revolved Head-to-Knee Pose)": {
            "title": "파르브리타 자누 시르사아사나(Revolved Head-to-Knee Pose)",
            "description": [
                ("자세 설명", [
                    "• 한쪽 다리를 옆으로 뻗고, 다른 다리는 접어 몸통을 기울입니다.",
                    "• 상체를 뻗은 다리 쪽으로 숙이고, 반대쪽 팔을 위로 들어 올립니다."
                ]),
                ("효과", [
                    "• 옆구리와 허리 확장",
                    "• 햄스트링과 척추 유연성 향상",
                    "• 복부와 등 근육 강화"
                ]),
                ("주의사항", [
                    "• 무리하게 자세를 취하지 않도록 합니다.",
                    "• 허리에 통증이 있는 경우 주의가 필요합니다."
                ]),
                ("실행 방법", [
                    "1. 앉은 자세에서 한쪽 다리를 옆으로 뻗습니다.",
                    "2. 다른 다리는 접어 안쪽으로 당깁니다.",
                    "3. 상체를 뻗은 다리 쪽으로 천천히 숙입니다.",
                    "4. 반대쪽 팔을 위로 들어 스트레칭합니다."
                ])
            ],
            "video_path": os.path.join(os.path.dirname(__file__), '../src/mp4/video6.mp4')
        },
        "선 활 자세(Standing Split)": {
            "title": "선 활 자세(Standing Split)",
            "description": [
                ("자세 설명", [
                    "• 한 다리로 서서 균형을 잡습니다.",
                    "• 다른 다리를 뒤로 들어 올려 머리 위로 뻗습니다.",
                    "• 상체는 앞으로 숙여 들어 올린 다리와 일직선을 이룹니다."
                ]),
                ("효과", [
                    "• 균형감과 집중력 향상",
                    "• 다리, 엉덩이, 복부 근력 강화",
                    "• 햄스트링과 등 유연성 개선"
                ]),
                ("주의사항", [
                    "• 초보자는 벽을 활용하여 균형 잡기를 연습합니다.",
                    "• 무릎이나 허리에 문제가 있는 경우 주의가 필요합니다."
                ]),
                ("실행 방법", [
                    "1. Mountain Pose(산 자세)로 시작합니다.",
                    "2. 한쪽 다리에 체중을 실어 균형을 잡습니다.",
                    "3. 반대쪽 다리를 천천히 들어 올립니다.",
                    "4. 상체를 앞으로 기울이며 자세를 유지합니다."
                ])
            ],
            "video_path": os.path.join(os.path.dirname(__file__), '../src/mp4/video3.mp4')
        },
        "런지 사이트 스트레칭(Lunging Side Stretch)": {
            "title": "런지 사이트 스트레칭(Lunging Side Stretch)",
            "description": [
                ("자세 설명", [
                    "• 한쪽 다리를 앞으로 내밀어 깊은 런지 자세를 취합니다.",
                    "• 뒷다리는 쭉 펴서 발뒤꿈치를 들어올립니다.",
                    "• 양팔을 머리 위로 들어 올리고 한쪽으로 상체를 기울입니다."
                ]),
                ("효과", [
                    "• 하체 근력 강화 (대퇴사두근, 햄스트링, 엉덩이 근육)",
                    "• 코어 안정성 향상",
                    "• 측면 몸통 근육 스트레칭"
                ]),
                ("주의사항", [
                    "• 무릎 문제가 있는 경우 주의가 필요합니다.",
                    "• 과도한 스트레칭은 피하고 개인의 유연성 수준에 맞춥니다."
                ]),
                ("실행 방법", [
                    "1. 발을 어깨 너비로 벌리고 서서 시작합니다.",
                    "2. 한 발을 앞으로 크게 내딛어 런지 자세를 취합니다.",
                    "3. 양팔을 머리 위로 들어 올립니다.",
                    "4. 천천히 상체를 옆으로 기울이며 10-30초 유지합니다."
                ])
            ],
            "video_path": os.path.join(os.path.dirname(__file__), '../src/mp4/video4.mp4')
        }
    }
    
    # 나머지 코드는 그대로 유지
    selected_action = st.session_state.selected_action
    st.write(action_info[selected_action]["title"])

    video_path = action_info[selected_action]["video_path"]
    if os.path.exists(video_path):
        with open(video_path, 'rb') as video_file:
            video_bytes = video_file.read()
            st.video(video_bytes, format="video/mp4")
    else:
        st.error(f"동영상을 찾을 수 없습니다: {video_path}")

    col1, col2 = st.columns([1, 1])  
    with col1:
        if st.button("목록", key="previous_button"):
            st.session_state.selected_page = "main"

    with col2:
        if st.button("다음", key="next_button"):
            st.session_state.selected_page = "page2"

    # 동작 설명 출력
    description = action_info[selected_action]["description"]
    for section_title, section_content in description:
        st.markdown(f"### {section_title}")
        for line in section_content:
            st.markdown(f"- {line}")

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