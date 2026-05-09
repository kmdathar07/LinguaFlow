import os
import json
from typing import Optional

from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
load_dotenv()

# Initialize Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY", "")
)

# Model name from .env, fallback to gemini-2.5-flash
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

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
- Return ONLY the translated text, nothing else — no explanations, no labels, no quotes

Text to translate:
{text}"""

    # Generate translation with Gemini
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    translated = response.text.strip()

    # Detect source language
    detected_lang = source_lang

    if source_lang == "auto":
        detect_prompt = f"""What language is this text written in?

Reply with ONLY the ISO 639-1 language code
(e.g., en, es, fr, ja, ar, hi, ta).

Nothing else.

Text:
{text[:200]}"""

        detect_response = client.models.generate_content(
            model=MODEL_NAME,
            contents=detect_prompt
        )

        detected_lang = detect_response.text.strip().lower()

        # Clean up potential formatting issues
        detected_lang = detected_lang.replace('"', '').replace("'", "").strip()

        # Fallback if Gemini returns an unexpected value
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

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    result = response.text.strip()

    try:
        return json.loads(result)
    except Exception:
        return {
            "code": "en",
            "name": "English",
            "confidence": 50
        }