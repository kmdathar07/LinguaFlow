import os
import json
import asyncio

from dotenv import load_dotenv
from google import genai
from deep_translator import GoogleTranslator

# Load environment variables
load_dotenv()

# Initialize Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY", "")
)

# Default model
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash-lite")

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


async def _detect_language_with_gemini(text: str) -> str:
    prompt = f"""What language is this text written in?

Reply with ONLY the ISO 639-1 language code.
Examples: en, hi, ta, ar, fr

Text:
{text[:200]}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        return "en"

    code = response.text.strip().lower()
    code = code.replace('"', "").replace("'", "").strip()

    if code not in LANGUAGE_NAMES:
        return "en"

    return code


async def _translate_with_gemini(
    text: str,
    source_lang: str,
    target_lang: str
) -> str:
    source_name = LANGUAGE_NAMES.get(source_lang, source_lang)
    target_name = LANGUAGE_NAMES.get(target_lang, target_lang)

    prompt = f"""Translate from {source_name} to {target_name}.

Translate naturally like Google Translate.

Rules:
- Preserve the exact meaning.
- Use fluent and natural {target_name}.
- Handle Hinglish, Tanglish, Roman Urdu, and transliterated text correctly.
- Understand context, not word-by-word translation.
- Return ONLY the translated text.
- No explanations.
- No quotes.
- No labels.

Examples:
main ghar ja raha hun -> I am going home.
mujhe nahi khaana -> I don't want to eat.
naan veliya poren -> I am going outside.

Text:
{text}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        raise Exception("Empty response from Gemini.")

    return response.text.strip()


def _translate_with_google_fallback(
    text: str,
    source_lang: str,
    target_lang: str
) -> str:
    # deep-translator uses "auto" for automatic language detection
    source = "auto" if source_lang == "auto" else source_lang

    translator = GoogleTranslator(
        source=source,
        target=target_lang
    )

    translated = translator.translate(text)

    if not translated:
        raise Exception("Google fallback returned empty response.")

    return translated.strip()


async def translate_text(
    text: str,
    target_lang: str,
    source_lang: str = "auto"
) -> dict:
    if not text.strip():
        return {
            "translated_text": "",
            "detected_language": "en",
            "detected_language_name": "English",
            "source_lang": source_lang,
            "target_lang": target_lang,
            "character_count": 0,
        }

    # Detect source language
    detected_lang = source_lang
    if source_lang == "auto":
        try:
            detected_lang = await _detect_language_with_gemini(text)
        except Exception:
            detected_lang = "auto"

    # PRIMARY: Gemini
    try:
        translated = await _translate_with_gemini(
            text=text,
            source_lang=detected_lang if source_lang == "auto" else source_lang,
            target_lang=target_lang
        )
        translation_engine = "gemini"

    # FALLBACK: Google Translate via deep-translator
    except Exception:
        try:
            translated = await asyncio.to_thread(
                _translate_with_google_fallback,
                text,
                "auto" if source_lang == "auto" else source_lang,
                target_lang
            )
            translation_engine = "google-fallback"
        except Exception:
            raise Exception(
                "Gemini quota exceeded and fallback translation is "
                "temporarily unavailable. Please try again later."
            )

    return {
        "translated_text": translated,
        "detected_language": (
            detected_lang if detected_lang != "auto" else "en"
        ),
        "detected_language_name": LANGUAGE_NAMES.get(
            detected_lang if detected_lang != "auto" else "en",
            "English"
        ),
        "source_lang": source_lang,
        "target_lang": target_lang,
        "character_count": len(text),
        "translation_engine": translation_engine
    }


async def detect_language(text: str) -> dict:
    try:
        code = await _detect_language_with_gemini(text)
        return {
            "code": code,
            "name": LANGUAGE_NAMES.get(code, code),
            "confidence": 98
        }
    except Exception:
        return {
            "code": "en",
            "name": "English",
            "confidence": 50
        }