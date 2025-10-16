from fastapi import FastAPI, HTTPException
from urllib.parse import unquote
from dotenv import load_dotenv
import os

from models import FeedbackRequest, FeedbackResponse
from services.feedback import generate_feedback

# 최상단에서 .env 로드
dotenv_path = "C:/beyond/Algo-Project/Algo-Coding-Ai/algo-coding-ai/.env"
load_dotenv(dotenv_path=dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError(f"환경 변수 OPENAI_API_KEY를 읽을 수 없습니다! (.env 경로: {dotenv_path})")
os.environ["OPENAI_API_KEY"] = api_key.strip()

app = FastAPI()

@app.post("/feedback", response_model=FeedbackResponse)
def feedback(req: FeedbackRequest):
    decoded_content = unquote(req.content)
    ai_response = generate_feedback(req.title, decoded_content, req.problem)
    return ai_response

@app.get("/check_key")
def check_key():
    """
    환경 변수 OPENAI_API_KEY 확인
    """
    key = os.getenv("OPENAI_API_KEY")
    return {
        "key_loaded": bool(key),
        "key_repr": repr(key),
        "length": len(key) if key else 0,
        "starts_with": key[:4] if key else None
    }

@app.get("/test_openai")
def test_openai():
    """
    OpenAI 호출 테스트
    """
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"success": False, "error": "OPENAI_API_KEY 없음"}

    client = OpenAI(api_key=api_key.strip())
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello in one sentence."}
            ]
        )
        message_content = response.choices[0].message.content
        return {"success": True, "response": message_content}
    except Exception as e:
        return {"success": False, "error": str(e)}
