import json
from typing import Optional

import httpx

# Stable public LibreTranslate instance
BASE_URL = "https://translate.argosopentech.com"

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


async def translate_text(
    text: str,
    target_lang: str,
    source_lang: str = "auto"
) -> dict:
    source_name = LANGUAGE_NAMES.get(source_lang, source_lang)
    target_name = LANGUAGE_NAMES.get(target_lang, target_lang)

    # Preserved logic and structure
    if source_lang == "auto":
        lang_instruction = (
            f"Detect the language of the input text and translate it to {target_name}."
        )
    else:
        lang_instruction = (
            f"Translate from {source_name} to {target_name}."
        )

    # Preserved prompt construction (kept for structural compatibility)
    prompt = f"""{lang_instruction}

Rules:
- Preserve the original tone, style, and formatting exactly
- Handle idioms, slang, and cultural expressions naturally
- Keep proper nouns, brand names, and technical terms appropriately
- If the text is already in the target language, return it as-is
- Return ONLY the translated text, nothing else — no explanations, no labels, no quotes

Text to translate:
{text}"""

    # Translation using stable Argos Open Tech endpoint
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{BASE_URL}/translate",
            json={
                "q": text,
                "source": "auto" if source_lang == "auto" else source_lang,
                "target": target_lang,
                "format": "text"
            },
            headers={
                "Content-Type": "application/json"
            }
        )
        response.raise_for_status()
        data = response.json()

    translated = data["translatedText"].strip()

    # Detect source language (same logical flow as your original code)
    detected_lang = source_lang

    if source_lang == "auto":
        detect_prompt = f"""What language is this text written in?

Reply with ONLY the ISO 639-1 language code
(e.g., en, es, fr, ja, ar, hi, ta).

Nothing else.

Text:
{text[:200]}"""

        async with httpx.AsyncClient(timeout=30) as client:
            detect_response = await client.post(
                f"{BASE_URL}/detect",
                json={"q": text[:300]},
                headers={
                    "Content-Type": "application/json"
                }
            )
            detect_response.raise_for_status()
            detect_data = detect_response.json()

        if isinstance(detect_data, list) and detect_data:
            detected_lang = detect_data[0].get("language", "en").strip().lower()
        else:
            detected_lang = "en"

        # Cleanup and validation preserved from your original logic
        detected_lang = detected_lang.replace('"', "").replace("'", "").strip()

        if detected_lang not in LANGUAGE_NAMES:
            detected_lang = "en"

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
    prompt = f"""Detect the language of this text.

Reply with a JSON object containing:
- "code": ISO 639-1 language code (e.g., "en", "es", "fr")
- "name": Full language name in English
- "confidence": confidence percentage (0-100)

Reply ONLY with the JSON object, nothing else.

Text:
{text[:300]}"""

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{BASE_URL}/detect",
            json={"q": text[:300]},
            headers={
                "Content-Type": "application/json"
            }
        )
        response.raise_for_status()
        data = response.json()

    if isinstance(data, list) and data:
        best = data[0]
        code = best.get("language", "en")
        confidence = int(best.get("confidence", 50))

        result = {
            "code": code,
            "name": LANGUAGE_NAMES.get(code, code),
            "confidence": confidence
        }

        # Preserved json parsing structure concept
        try:
            return json.loads(json.dumps(result))
        except Exception:
            pass

    return {
        "code": "en",
        "name": "English",
        "confidence": 50
    }