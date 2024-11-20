import openai

client = openai.OpenAI(api_key=api_key)

def get_response_from_openai(prompt: str) -> str:
    """
    OpenAI gpt-4o-mini 모델을 사용해 사용자의 입력(prompt)에 대한 응답을 생성합니다.

    Parameters:
    - prompt: 사용자 질문 또는 요청 (str)

    Returns:
    - OpenAI 응답 메시지 (str)
    """
    try:
        # GPT-4o-mini 모델 사용
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )

        # 응답 텍스트 추출
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        # 에러 처리
        return f"오류 발생: {str(e)}"

if __name__ == "__main__":
    # 콘솔에서 사용자 입력 받기
    user_input = input("AI에게 물어볼 내용을 입력하세요: ")
    ai_response = get_response_from_openai(user_input)
    print("\n[AI의 응답]")
    print(ai_response)
