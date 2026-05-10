import json
import os
from urllib.parse import quote

import httpx
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

# Initialize Gemini only if API key exists
gemini_client = None
if GEMINI_API_KEY:
    try:
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception:
        gemini_client = None


LANGUAGE_NAMES = {
    "auto": "Auto-Detect",
    "en": "English", "es": "Spanish", "fr": "French", "de": "German",
    "it": "Italian", "pt": "Portuguese", "ru": "Russian", "ja": "Japanese",
    "ko": "Korean", "zh": "Chinese (Simplified)", "zh-TW": "Chinese (Traditional)",
    "ar": "Arabic", "hi": "Hindi", "nl": "Dutch", "pl": "Polish",
    "tr": "Turkish", "sv": "Swedish", "da": "Danish", "fi": "Finnish",
    "no": "Norwegian", "cs": "Czech", "hu": "Hungarian", "ro": "Romanian",
    "uk": "Ukrainian", "th": "Thai", "vi": "Vietnamese", "id": "Indonesian",
    "ms": "Malay", "he": "Hebrew", "el": "Greek", "ca": "Catalan",
    "bn": "Bengali", "ta": "Tamil", "te": "Telugu", "ml": "Malayalam",
}


def normalize_lang(code: str) -> str:
    if code == "auto":
        return "auto"
    if code == "zh-TW":
        return "zh-TW"
    return code.split("-")[0]


async def gemini_translate(
    text: str,
    target_lang: str,
    source_lang: str = "auto"
):
    """
    High-quality translation using Gemini.
    Raises exception if quota is exceeded or API fails.
    """
    if gemini_client is None:
        raise Exception("Gemini API key not configured")

    target_name = LANGUAGE_NAMES.get(target_lang, target_lang)

    if source_lang == "auto":
        instruction = (
            f"Detect the source language automatically and translate the text into {target_name}. "
            "If the input is Romanized Hindi/Urdu (written in English letters), "
            "understand the meaning and translate naturally."
        )
    else:
        source_name = LANGUAGE_NAMES.get(source_lang, source_lang)
        instruction = (
            f"Translate from {source_name} to {target_name}. "
            "If the input is Romanized Hindi/Urdu (written in English letters), "
            "understand the meaning and translate naturally."
        )

    prompt = f"""
{instruction}

Rules:
- Preserve the exact meaning.
- Handle Romanized Hindi/Urdu/Hinglish naturally.
- Translate idioms and slang appropriately.
- Keep formatting intact.
- Return ONLY the translated text.
- Do not include quotes or explanations.

Text:
{text}
"""

    response = gemini_client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text.strip()


async def mymemory_translate(
    text: str,
    target_lang: str,
    source_lang: str = "auto"
):
    """
    Free fallback translation using MyMemory.
    No API key required.
    """
    detected_lang = source_lang

    if source_lang == "auto":
        detection = await detect_language(text)
        detected_lang = detection["code"]

    source_code = normalize_lang(detected_lang)
    target_code = normalize_lang(target_lang)

    encoded_text = quote(text)

    url = (
        "https://api.mymemory.translated.net/get"
        f"?q={encoded_text}&langpair={source_code}|{target_code}"
    )

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

    translated = (
        data.get("responseData", {})
        .get("translatedText", "")
        .strip()
    )

    if not translated:
        translated = text

    return translated


async def translate_text(
    text: str,
    target_lang: str,
    source_lang: str = "auto"
) -> dict:
    """
    Main translation function:
    1. Try Gemini first.
    2. If Gemini fails or quota is exceeded, fallback to MyMemory.
    """
    detected_lang = source_lang

    if source_lang == "auto":
        detection = await detect_language(text)
        detected_lang = detection["code"]

    # Try Gemini first
    try:
        translated = await gemini_translate(
            text=text,
            target_lang=target_lang,
            source_lang=source_lang
        )
    except Exception:
        # Automatic fallback to free API
        translated = await mymemory_translate(
            text=text,
            target_lang=target_lang,
            source_lang=detected_lang
        )

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
    }


async def detect_language(text: str) -> dict:
    """
    Detect language using Gemini if available,
    otherwise use simple heuristics.
    """
    if gemini_client is not None:
        try:
            prompt = f"""
Detect the language of the following text.

Important:
- If the text is Romanized Hindi/Urdu/Hinglish written in English letters,
  return "hi".

Reply ONLY with valid JSON:
{{"code":"hi","name":"Hindi","confidence":95}}

Text:
{text[:300]}
"""

            response = gemini_client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            return json.loads(response.text.strip())
        except Exception:
            pass

    # Fallback heuristics
    sample = text[:300]

    if any("\u0600" <= ch <= "\u06FF" for ch in sample):
        code = "ar"
    elif any("\u0B80" <= ch <= "\u0BFF" for ch in sample):
        code = "ta"
    elif any("\u0900" <= ch <= "\u097F" for ch in sample):
        code = "hi"
    elif any("\u3040" <= ch <= "\u30FF" for ch in sample):
        code = "ja"
    elif any("\u4E00" <= ch <= "\u9FFF" for ch in sample):
        code = "zh"
    else:
        # Treat Romanized Hindi/Hinglish as Hindi by default
        code = "hi"

    return {
        "code": code,
        "name": LANGUAGE_NAMES.get(code, code),
        "confidence": 90
    }