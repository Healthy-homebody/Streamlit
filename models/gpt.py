import os
import openai

# OpenAI API 키 로딩
openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = ""  # OpenAI API 키

def get_advice_based_on_similarity(dtw_distance: float, action_name: str) -> str:
    """
    DTW 유사도 거리 값에 기반하여 GPT-4 ChatCompletion API를 사용해 피드백을 생성하는 함수입니다.
    
    Parameters:
    - dtw_distance: DTW 거리 값 (float)
    - action_name: 동작 이름 (str)
    
    Returns:
    - 피드백 메시지 (str)
    """
    # 사용자 입력 데이터를 텍스트로 변환하여 AI에 전달
    user_message = (
        f"사용자와 '{action_name}' 동작을 비교한 결과, DTW 거리 값은 {dtw_distance}입니다.\n"
        "이 값에 기반하여 다음과 같은 피드백을 제공해주세요:\n"
        "- 유사도가 낮을 경우: 자세를 교정하기 위한 구체적인 피드백 제공.\n"
        "- 유사도가 높을 경우: 칭찬과 간단한 개선점을 제안.\n"
    )

    # OpenAI에게 전달할 메시지 설정
    messages = [
        {
            "role": "system",
            "content": (
                "당신은 피트니스 전문가입니다. 사용자의 운동 동작과 유사도를 평가하고, "
                "그에 따른 개선 피드백을 제공하는 데 전문성을 갖고 있습니다."
            )
        },
        {"role": "user", "content": user_message}
    ]

    try:
        # GPT-4 ChatCompletion API 호출
        result = openai.ChatCompletion.create(
            model="gpt-4",  # 최신 ChatCompletion 모델 지정
            messages=messages,
            temperature=0.7
        )

        # AI 응답에서 텍스트 추출
        advice = result['choices'][0]['message']['content'].strip()
        print(f"GPT Response:\n{advice}")  # 디버깅을 위해 응답 출력
        return advice

    except Exception as e:
        # 에러 발생 시 기본 메시지 반환
        print(f"Error: {str(e)}")  # 에러 출력
        return (
            "피드백을 생성하는 동안 문제가 발생했습니다. 하지만 다음을 참고하세요:\n"
            "운동을 반복하면서 올바른 자세를 유지하려고 노력하세요. 꾸준함이 중요합니다!"
        )
