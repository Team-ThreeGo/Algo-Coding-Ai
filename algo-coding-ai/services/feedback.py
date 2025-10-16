import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# .env는 여기서 한 번만 로드
#load_dotenv(dotenv_path="C:/beyond/Algo-Project/Algo-Coding-Ai/algo-coding-ai/.env")
dotenv_path = "C:/beyond/Algo-Project/Algo-Coding-Ai/algo-coding-ai/.env"
load_dotenv(dotenv_path=dotenv_path)
#api_key = os.getenv("OPENAI_API_KEY")

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

def get_openai_client():
    """요청 시점에 클라이언트 생성"""
    dotenv_path = "C:/beyond/Algo-Project/Algo-Coding-Ai/algo-coding-ai/.env"
    load_dotenv(dotenv_path=dotenv_path)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("환경 변수 OPENAI_API_KEY가 설정되지 않았습니다!")
    return OpenAI(api_key=api_key.strip())

def generate_feedback(title: str, content: str, problem: str) -> dict:
    """
    OpenAI GPT 모델 호출해서 JSON 피드백 반환
    """
    client = get_openai_client()  # 요청 시점에 새로 생성
    user_prompt = f"문제: {problem}\n제출 답안: {content}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
        )

        raw_content = response.choices[0].message.content.strip()
        feedback_dict = json.loads(raw_content)

        return {
            "aiBigO": feedback_dict.get("aiBigO", ""),
            "aiGood": feedback_dict.get("aiGood", "").replace("\\n", "\n"),
            "aiBad": feedback_dict.get("aiBad", "").replace("\\n", "\n"),
            "aiPlan": feedback_dict.get("aiPlan", "").replace("\\n", "\n"),
        }

    except json.JSONDecodeError:
        raise ValueError(f"AI 응답을 JSON으로 파싱할 수 없습니다: {raw_content}")
    except Exception as e:
        raise RuntimeError(f"AI 피드백 생성 실패: {str(e)}")
