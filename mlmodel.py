from transformers import pipeline
from fastapi import APIRouter,  HTTPException

model = APIRouter(name="")

summarizer = pipeline("summarization")

class Book(BaseModel):
    title: str
    publisher: str
    text: str = None
    summary: str = None

@model.post("/summarize/", response_model=str)
def summarize_book(text: str):
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']
