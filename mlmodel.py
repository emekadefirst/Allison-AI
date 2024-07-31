import os
import fitz
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi.responses import JSONResponse
from fastapi import APIRouter, UploadFile, File, HTTPException

model = APIRouter()
load_dotenv()

BOOK_FILE_DIRECTORY = "./book_file/"
if not os.path.exists(BOOK_FILE_DIRECTORY):
    os.makedirs(BOOK_FILE_DIRECTORY)

async def extract_text_from_pdf(file_path: str) -> str:
    try:
        pdf_document = fitz.open(file_path)
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        pdf_document.close()
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def summarize(file_path: str):
    genai.configure(api_key=os.environ.get('gemini_api'))
    model = genai.GenerativeModel('gemini-1.5-flash')
    text_content = await extract_text_from_pdf(file_path)
    prompt = f"""Please provide a summary of the following text, ensuring that the summary contains key points and values in clear and understandable language:
    {text_content}"""
    response = model.generate_content(prompt)
    if response.text:
        analysis_text = response.text
    return analysis_text

@model.post("/api/summarize/")
async def summarize_book(file: UploadFile = File(...)):
    file_path = os.path.join(BOOK_FILE_DIRECTORY, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        summary = await summarize(file_path)
        return {"summary": summary}
    except HTTPException as e:
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
