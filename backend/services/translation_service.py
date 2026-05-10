import httpx

LANGUAGE_NAMES = {
    "auto": "Auto-Detect",
    "en": "English", "es": "Spanish", "fr": "French", "de": "German",
    "it": "Italian", "pt": "Portuguese", "ru": "Russian", "ja": "Japanese",
    "ko": "Korean", "zh": "Chinese", "ar": "Arabic", "hi": "Hindi",
    "nl": "Dutch", "pl": "Polish", "tr": "Turkish", "sv": "Swedish",
    "da": "Danish", "fi": "Finnish", "cs": "Czech", "hu": "Hungarian",
    "ro": "Romanian", "uk": "Ukrainian", "th": "Thai", "vi": "Vietnamese",
    "id": "Indonesian", "he": "Hebrew", "el": "Greek", "bn": "Bengali",
    "ta": "Tamil", "te": "Telugu", "ml": "Malayalam",
}


async def translate_text(text: str, target_lang: str, source_lang: str = "auto") -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://libretranslate.com/translate",
            json={
                "q": text,
                "source": "auto" if source_lang == "auto" else source_lang,
                "target": target_lang,
                "format": "text"
            }
        )
        response.raise_for_status()
        data = response.json()

    detected_lang = source_lang if source_lang != "auto" else "auto"

    return {
        "translated_text": data["translatedText"],
        "detected_language": detected_lang,
        "detected_language_name": LANGUAGE_NAMES.get(detected_lang, detected_lang),
        "source_lang": source_lang,
        "target_lang": target_lang,
        "character_count": len(text),
    }


async def detect_language(text: str) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://libretranslate.com/detect",
            json={"q": text}
        )
        response.raise_for_status()
        data = response.json()

    if isinstance(data, list) and data:
        best = data[0]
        code = best.get("language", "en")
        confidence = int(best.get("confidence", 50))
        return {
            "code": code,
            "name": LANGUAGE_NAMES.get(code, code),
            "confidence": confidence
        }

    return {
        "code": "en",
        "name": "English",
        "confidence": 50
    }