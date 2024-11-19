# models/gpt.py
import openai
import os

# OpenAI API 키 로딩 (환경변수로 설정된 키 사용)
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_advice_based_on_similarity(dtw_distance: float, action_name: str) -> str:
    """
    DTW 유사도 거리 값에 기반하여 GPT-4 모델을 사용해 조언을 생성하는 함수입니다.
    
    Parameters:
    - dtw_distance: DTW 거리 값 (float)
    - action_name: 동작 이름 (str)
    
    Returns:
    - 조언 메시지 (str)
    """
    
    # GPT-4에게 제공할 프롬프트 생성
    prompt = f"""
    사용자와 {action_name} 동작을 비교한 결과, DTW 거리 값은 {dtw_distance}입니다.
    이 값에 대한 피드백을 제공해주세요. 유사도가 낮다면 자세 교정을 위한 피드백을, 유사도가 높다면 잘 수행했다고 칭찬하는 피드백을 부탁드립니다.
    """
    
    try:
        # GPT-4 API 호출
        response = openai.Completion.create(
            engine="gpt-4o-mini", 
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,  # 창의적인 피드백을 위해 적당한 온도 설정
            n=1,
            stop=None
        )

        # GPT-4의 응답에서 텍스트 부분만 추출
        advice = response.choices[0].text.strip()
        return advice
    
    except Exception as e:
        # 에러 발생 시 기본 메시지 반환
        return f"조언을 생성하는 데 실패했습니다: {str(e)}"
