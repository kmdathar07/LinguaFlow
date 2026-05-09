from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from services.translation_service import translate_text

router = APIRouter()

class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)
    source_lang: str = Field(default="auto")
    target_lang: str = Field(default="en")

class TranslateResponse(BaseModel):
    translated_text: str
    detected_language: str
    detected_language_name: str
    source_lang: str
    target_lang: str
    character_count: int

@router.post("/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    if request.source_lang == request.target_lang and request.source_lang != "auto":
        return TranslateResponse(
            translated_text=request.text,
            detected_language=request.source_lang,
            detected_language_name=request.source_lang,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            character_count=len(request.text)
        )
    try:
        result = await translate_text(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        return TranslateResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")
