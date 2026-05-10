import json
from urllib.parse import quote

import httpx

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


async def translate_text(
    text: str,
    target_lang: str,
    source_lang: str = "auto"
) -> dict:
    source_name = LANGUAGE_NAMES.get(source_lang, source_lang)
    target_name = LANGUAGE_NAMES.get(target_lang, target_lang)

    # Preserved structure
    if source_lang == "auto":
        lang_instruction = (
            f"Detect the language of the input text and translate it to {target_name}."
        )
    else:
        lang_instruction = (
            f"Translate from {source_name} to {target_name}."
        )

    prompt = f"""{lang_instruction}

Rules:
- Preserve the original tone, style, and formatting exactly
- Handle idioms, slang, and cultural expressions naturally
- Keep proper nouns, brand names, and technical terms appropriately
- If the text is already in the target language, return it as-is
- Return ONLY the translated text, nothing else

Text to translate:
{text}"""

    # Auto-detect source language if needed
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
    # Lightweight heuristic for common languages
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
        code = "en"

    result = {
        "code": code,
        "name": LANGUAGE_NAMES.get(code, code),
        "confidence": 90
    }

    # Preserved JSON parsing concept
    try:
        return json.loads(json.dumps(result))
    except Exception:
        return {
            "code": "en",
            "name": "English",
            "confidence": 50
        }