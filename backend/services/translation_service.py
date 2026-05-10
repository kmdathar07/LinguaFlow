import os
import json
import urllib.parse
from typing import Optional

import httpx
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Initialize Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY", "")
)

# Default model (can be overridden in .env)
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


# ---------------------------------------------------------
# Gemini Translation (Primary)
# ---------------------------------------------------------
async def _translate_with_gemini(
    text: str,
    source_lang: str,
    target_lang: str
) -> str:
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

Translate naturally like Google Translate.

Rules:
- Preserve the exact meaning.
- Use fluent, natural {target_name}.
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

Text to translate:
{text}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        raise Exception("Gemini returned an empty response.")

    return response.text.strip()


# ---------------------------------------------------------
# MyMemory Translation (Fallback)
# ---------------------------------------------------------
async def _translate_with_mymemory(
    text: str,
    source_lang: str,
    target_lang: str
) -> str:
    source = "auto" if source_lang == "auto" else source_lang

    # MyMemory requires a specific source language.
    # If source is auto, use English as a safe default and let
    # detected language logic below correct future calls.
    if source == "auto":
        source = "en"

    langpair = f"{source}|{target_lang}"

    url = (
        "https://api.mymemory.translated.net/get"
        f"?q={urllib.parse.quote(text)}"
        f"&langpair={urllib.parse.quote(langpair)}"
    )

    async with httpx.AsyncClient(timeout=30) as http:
        response = await http.get(url)
        response.raise_for_status()
        data = response.json()

    translated = (
        data.get("responseData", {})
        .get("translatedText", "")
        .strip()
    )

    if not translated:
        raise Exception("MyMemory returned an empty response.")

    return translated


# ---------------------------------------------------------
# Language Detection (Gemini)
# ---------------------------------------------------------
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

    detected = response.text.strip().lower()
    detected = detected.replace('"', "").replace("'", "").strip()

    if detected not in LANGUAGE_NAMES:
        return "en"

    return detected


# ---------------------------------------------------------
# Public Translation Function
# ---------------------------------------------------------
async def translate_text(
    text: str,
    target_lang: str,
    source_lang: str = "auto"
) -> dict:
    # Detect source language first if auto
    detected_lang = source_lang

    if source_lang == "auto":
        try:
            detected_lang = await _detect_language_with_gemini(text)
        except Exception:
            detected_lang = "en"

    # ---------------- Primary: Gemini ----------------
    try:
        translated = await _translate_with_gemini(
            text=text,
            source_lang=source_lang,
            target_lang=target_lang
        )
        translation_engine = "gemini"

    # ---------------- Fallback: MyMemory ----------------
    except Exception as gemini_error:
        try:
            translated = await _translate_with_mymemory(
                text=text,
                source_lang=detected_lang,
                target_lang=target_lang
            )
            translation_engine = "mymemory"
        except Exception:
            # If both fail, show Gemini error so user knows to retry later
            raise Exception(
                f"Gemini is temporarily unavailable or quota exceeded. "
                f"Please try again after some time.\n\n"
                f"Original error: {str(gemini_error)}"
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
        "translation_engine": translation_engine
    }


# ---------------------------------------------------------
# Public Language Detection Function
# ---------------------------------------------------------
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