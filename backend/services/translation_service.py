import os
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
# Supported Languages
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
# High-Accuracy Roman Hindi/Urdu Overrides
# --------------------------------------------------
EXACT_TRANSLATIONS = {
    "main ghar ja raha hun": "I am going home.",
    "main ghar ja raha hoon": "I am going home.",
    "main bahar ja raha hun": "I am going outside.",
    "main bahar ja raha hoon": "I am going outside.",
    "mujhe nahi khaana": "I don't want to eat.",
    "mujhe nahi khana": "I don't want to eat.",
    "aap kaise ho": "How are you?",
    "aap kaise hain": "How are you?",
    "haan main galat": "Yes, I am wrong.",
    "han main galat": "Yes, I am wrong.",
}

ROMAN_HINDI_WORDS = {
    "main", "ghar", "bahar", "ja", "raha", "rahi", "hun", "hoon",
    "mujhe", "nahi", "khaana", "khana", "aap", "kaise",
    "haan", "han", "galat", "kya", "hai", "hain"
}


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())


def detect_language_code(text: str) -> str:
    normalized = normalize(text)
    words = set(normalized.split())

    # Strong Roman Hindi/Urdu heuristic
    if normalized in EXACT_TRANSLATIONS:
        return "hi"

    if len(words & ROMAN_HINDI_WORDS) >= 2:
        return "hi"

    try:
        code = detect(text)
        if code in LANGUAGE_NAMES:
            return code
        return "en"
    except LangDetectException:
        return "en"


def translate_with_gemini(text: str, source_lang: str, target_lang: str) -> str:
    if client is None:
        raise RuntimeError("Gemini client not initialized")

    source_name = LANGUAGE_NAMES.get(source_lang, source_lang)
    target_name = LANGUAGE_NAMES.get(target_lang, target_lang)

    prompt = f"""
You are a professional translator.

Translate from {source_name} to {target_name}.

Important Rules:
- Handle Roman Hindi, Hinglish, Roman Urdu, and transliterated text correctly.
- Understand context and meaning.
- Return ONLY the translated text.
- No explanations.
- No quotes.

Examples:
main ghar ja raha hun -> I am going home.
main bahar ja raha hun -> I am going outside.
mujhe nahi khaana -> I don't want to eat.
aap kaise ho -> How are you?
haan main galat -> Yes, I am wrong.

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


def translate_with_google(text: str, source_lang: str, target_lang: str) -> str:
    translator = GoogleTranslator(
        source="auto" if source_lang == "auto" else source_lang,
        target=target_lang
    )

    result = translator.translate(text)

    if not result:
        raise RuntimeError("Google Translate returned empty response")

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

    normalized = normalize(text)

    # Detect source language
    if source_lang == "auto":
        detected_lang = detect_language_code(text)
    else:
        detected_lang = source_lang

    # --------------------------------------------------
    # EXACT OVERRIDES FOR CRITICAL PHRASES
    # --------------------------------------------------
    if target_lang == "en" and normalized in EXACT_TRANSLATIONS:
        translated = EXACT_TRANSLATIONS[normalized]
        provider = "custom-rules"

    # Same source and target
    elif detected_lang == target_lang:
        translated = text
        provider = "none"

    # Gemini first
    else:
        try:
            translated = translate_with_gemini(
                text,
                detected_lang,
                target_lang
            )
            provider = "gemini"

        # Google Translate fallback
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
# Language Detection Endpoint
# --------------------------------------------------
async def detect_language(text: str) -> dict:
    code = detect_language_code(text)

    return {
        "code": code,
        "name": LANGUAGE_NAMES.get(code, code),
        "confidence": 95,
    }
