import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# api_key 가져오기 (None이면 에러 발생)
api_key = os.getenv("OPENAI_API_KEY")
# print("DEBUG >> feedback.py - OPENAI_API_KEY:", api_key)  # 디버깅 로그

if not api_key:
    raise ValueError("환경 변수 OPENAI_API_KEY가 설정되지 않았습니다!")

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
너는 코딩 테스트 문제 풀이를 평가하는 AI 코치다.
다음 기준으로 JSON 형식 피드백을 생성해라.

출력 형식:
{
  "aiBigO": "O(N*M)",
  "aiGood": "잘한 점을 요약 (1~3가지, 문자열 하나로 합침)",
  "aiBad": "문제점을 요약 (문자열)",
  "aiPlan": "개선방안을 요약 (문자열)"
}

규칙:
1. 시간복잡도는 Big-O 표기만. (예: O(N*M))
2. 잘한 점, 문제점, 개선방안은 전공자 수준에서 이해할 수 있도록 간결하게 설명.
3. 잘한 점은 1~3개 정도만.
4. 변경할 필요 없는 로직은 언급하지 말 것.
5. 이전 제출 기록은 무시하고, 현재 답안만 평가.
6. 반드시 JSON 형식으로만 답하라.
"""

def generate_feedback(title: str, content: str, problem: str) -> dict:
    user_prompt = f"""
문제: {problem}
제출 답안: {content}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        response_format={ "type": "json_object" }
    )

    # 추가
    raw_content = response.choices[0].message.content

    # JSON 문자열 → dict 변환 (줄바꿈 포함)
    feedback_dict = json.loads(raw_content)

    # return response.choices[0].message.content
    # 줄바꿈이 반영된 문자열로 리턴
    return {
        "aiBigO": feedback_dict.get("aiBigO", ""),
        "aiGood": feedback_dict.get("aiGood", "").replace("\\n", "\n"),
        "aiBad": feedback_dict.get("aiBad", "").replace("\\n", "\n"),
        "aiPlan": feedback_dict.get("aiPlan", "").replace("\\n", "\n"),
    }
