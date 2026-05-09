from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.translation_service import detect_language

router = APIRouter()

class DetectRequest(BaseModel):
    text: str

@router.post("/detect")
async def detect(request: DetectRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    try:
        return await detect_language(request.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
