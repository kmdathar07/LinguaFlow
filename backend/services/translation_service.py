import os
import json
from dotenv import load_dotenv
from google import genai
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException

load_dotenv()

# --------------------------------------------------
# Gemini Configuration
# --------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash-lite")

client = None
if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception:
        client = None

# --------------------------------------------------
# Language Names
# --------------------------------------------------
LANGUAGE_NAMES = {
    "auto": "Auto-Detect",
    "en": "English",
    "hi": "Hindi",
    "ur": "Urdu",
    "ta": "Tamil",
    "te": "Telugu",
    "ml": "Malayalam",
    "kn": "Kannada",
    "ar": "Arabic",
    "bn": "Bengali",
    "gu": "Gujarati",
    "mr": "Marathi",
    "pa": "Punjabi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
    "tr": "Turkish",
    "nl": "Dutch",
    "pl": "Polish",
    "sv": "Swedish",
    "th": "Thai",
    "vi": "Vietnamese",
    "id": "Indonesian",
    "ms": "Malay",
}

# --------------------------------------------------
# Roman Hindi/Urdu Detection Heuristics
# --------------------------------------------------
ROMAN_HINDI_WORDS = {
    "main", "ghar", "ja", "raha", "rahi", "hun", "hoon",
    "mujhe", "nahi", "khaana", "khana", "tum", "aap",
    "kya", "kaise", "hai", "tha", "thi", "kar", "rahe"
}


def detect_language_code(text: str) -> str:
    lower = text.lower()
    words = set(lower.split())

    # Detect Roman Hindi/Urdu transliteration
    if len(words & ROMAN_HINDI_WORDS) >= 2:
        return "hi"

    try:
        code = detect(text)
        if code in LANGUAGE_NAMES:
            return code
        return "en"
    except LangDetectException:
        return "en"


# --------------------------------------------------
# Gemini Translation
# --------------------------------------------------
def translate_with_gemini(text: str, source_lang: str, target_lang: str) -> str:
    if client is None:
        raise RuntimeError("Gemini client not initialized")

    source_name = LANGUAGE_NAMES.get(source_lang, source_lang)
    target_name = LANGUAGE_NAMES.get(target_lang, target_lang)

    if source_lang == "auto":
        source_instruction = "Automatically detect the source language."
    else:
        source_instruction = f"Source language is {source_name}."

    prompt = f"""
You are a professional translator.

{source_instruction}
Translate the text into {target_name}.

Important Rules:
- If text is written in Roman Hindi/Urdu (example: 'main ghar ja raha hun'), interpret it correctly.
- Return ONLY the translated text.
- No explanations.
- No quotes.
- Preserve meaning naturally.

Text:
{text}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError("Empty response from Gemini")

    return response.text.strip()


# --------------------------------------------------
# Google Translate Fallback
# --------------------------------------------------
def translate_with_google(text: str, source_lang: str, target_lang: str) -> str:
    source = "auto" if source_lang == "auto" else source_lang

    translator = GoogleTranslator(source=source, target=target_lang)
    result = translator.translate(text)

    if not result:
        raise RuntimeError("Google Translate fallback returned empty response")  # noqa: E501

    return result.strip()


# --------------------------------------------------
# Main Translation Function
# --------------------------------------------------
async def translate_text(
    text: str,
    target_lang: str,
    source_lang: str = "auto"
) -> dict:

    if not text.strip():
        raise ValueError("Text cannot be empty")

    # Detect language if auto mode
    if source_lang == "auto":
        detected_lang = detect_language_code(text)
    else:
        detected_lang = source_lang

    # If source and target are same, return original
    if detected_lang == target_lang:
        translated = text
        provider = "none"
    else:
        # Try Gemini first
        try:
            translated = translate_with_gemini(
                text,
                detected_lang,
                target_lang
            )
            provider = "gemini"

        # Automatic fallback to Google Translate
        except Exception:
            translated = translate_with_google(
                text,
                detected_lang,
                target_lang
            )
            provider = "google-fallback"

    return {
        "translated_text": translated,
        "detected_language": detected_lang,
        "detected_language_name": LANGUAGE_NAMES.get(
            detected_lang,
            detected_lang
        ),
        "source_lang": source_lang,
        "target_lang": target_lang,
        "character_count": len(text),
        "provider": provider,
    }


# --------------------------------------------------
# Standalone Language Detection
# --------------------------------------------------
async def detect_language(text: str) -> dict:
    code = detect_language_code(text)

    return {
        "code": code,
        "name": LANGUAGE_NAMES.get(code, code),
        "confidence": 95,
    }