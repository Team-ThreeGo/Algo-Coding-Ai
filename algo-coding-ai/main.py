from fastapi import FastAPI
from dotenv import load_dotenv
import os
from models import FeedbackRequest, FeedbackResponse
from services.feedback import generate_feedback
import json
from urllib.parse import unquote 

# 반드시 최상단에서 호출
load_dotenv()

# print("DEBUG >> OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))  # 테스트용

app = FastAPI()

@app.post("/feedback", response_model=FeedbackResponse)
def feedback(req: FeedbackRequest):
    ai_response = generate_feedback(req.title, req.content, req.problem)
    decoded_content = unquote(req.content)
    return ai_response
