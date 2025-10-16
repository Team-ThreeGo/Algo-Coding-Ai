# app.py
from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI(title="AI Feedback Server")

# 요청 DTO
class CodeRequest(BaseModel):
    code: str

# 피드백 응답 엔드포인트
@app.post("/feedback")
def get_feedback(req: CodeRequest):
    # TODO: OpenAI API 호출하거나 자체 AI 로직 작성
    return {
        "aiBigO": "O(N log N)",
        "aiGood": "코드가 명확합니다.",
        "aiBad": "예외 처리가 부족합니다.",
        "aiPlan": "입력값 검증 추가 필요"
    }

# 테스트용 루트
@app.get("/")
def root():
    return {"message": "FastAPI 서버가 정상 작동 중입니다."}

@app.get("/check_key")
def check_key():
    return {"key_loaded": repr(os.getenv("OPENAI_API_KEY"))}
