import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import chardet

model = APIRouter()

BOOK_FILE_DIRECTORY = "./book_file/"
if not os.path.exists(BOOK_FILE_DIRECTORY):
    os.makedirs(BOOK_FILE_DIRECTORY)

async def summarize(file_path: str) -> str:
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            confidence = result['confidence']

        if confidence < 0.7:
            encoding = 'utf-8'  # Fallback to UTF-8 if confidence is low

        try:
            content = raw_data.decode(encoding, errors='replace')  # Handle decoding errors
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="File encoding not supported or invalid byte sequences")
        
        # Dummy summary generation for demonstration
        summary = content[:200] + '...'  # Summarize the first 200 characters for demo
        return summary

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@model.post("/api/summarize/")
async def summarize_book(file: UploadFile = File(...)):
    file_path = os.path.join(BOOK_FILE_DIRECTORY, file.filename)
    try:
        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        # Call the summarize function
        summary = await summarize(file_path)
        return {"summary": summary}
    except HTTPException as e:
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
