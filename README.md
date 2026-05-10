# 🌐 LinguaFlow — AI-Powered Real-Time Translator

A production-grade full-stack translation web application powered by **Google Gemini AI** with an automatic **Google Translate fallback** to ensure accurate translations even when Gemini quota is exceeded.

---

## ✨ Features

- 🧠 Gemini AI Translation (Primary)
- 🔄 Automatic Google Translate Fallback
- 🌍 30+ Languages Supported
- 🔍 Auto Language Detection
- 🎙️ Voice Input (Speech-to-Text)
- 🔊 Text-to-Speech Output
- ⚡ Real-Time Translation
- 📋 Translation History
- 📥 Download Translation
- 📋 Copy to Clipboard
- 🔁 Swap Languages
- 🌙 Dark / Light Theme
- 📱 Fully Responsive Premium UI

---

## 🧠 Translation Engine Priority

### 1. Google Gemini 2.5 Flash Lite
Primary translation engine for:
- Natural translations
- Context-aware understanding
- Hinglish, Tanglish, Roman Urdu support

### 2. Google Translate (deep-translator)
Automatic fallback when:
- Gemini quota is exceeded
- Gemini is temporarily unavailable

This ensures:
- Accurate translations
- Automatic language detection
- Reliable service with no poor word-by-word output

---

## 🛠️ Tech Stack

### Frontend
- React 18
- Vite
- Modern CSS (Glassmorphism UI)

### Backend
- FastAPI
- Python 3.11+

### Translation Engines
- Google Gemini API
- deep-translator (Google Translate fallback)

### Deployment
- Vercel (Frontend)
- Render (Backend)

---

## 📁 Project Structure

\`\`\`
LinguaFlow/
├── backend/
│   ├── services/
│   │   └── translation_service.py
│   ├── routes/
│   ├── main.py
│   ├── requirements.txt
│   ├── runtime.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── .env
│
├── .gitignore
└── README.md
\`\`\`

---

## ⚙️ Environment Variables

### Backend (`backend/.env`)

\`\`\`env
GEMINI_API_KEY=your_actual_gemini_api_key
MODEL_NAME=gemini-2.5-flash-lite
\`\`\`

### Frontend (`frontend/.env`)

\`\`\`env
VITE_API_URL=https://your-render-backend-url.onrender.com/api
\`\`\`

---

## 🚀 Run Locally

### Backend

\`\`\`bash
cd backend
pip install -r requirements.txt
python3 -m uvicorn main:app --reload --port 8000
\`\`\`

Backend runs at:
- http://127.0.0.1:8000

### Frontend

\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

Frontend runs at:
- http://localhost:3000

---

## ☁️ Deployment

### Backend on Render

**Root Directory**
\`\`\`
backend
\`\`\`

**Build Command**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

**Start Command**
\`\`\`bash
uvicorn main:app --host 0.0.0.0 --port \$PORT
\`\`\`

**Environment Variables**
- GEMINI_API_KEY
- MODEL_NAME=gemini-2.5-flash-lite

---

### Frontend on Vercel

Set the following environment variable:

\`\`\`env
VITE_API_URL=https://your-render-backend-url.onrender.com/api
\`\`\`

---

## 🌍 Supported Languages

English, Hindi, Tamil, Telugu, Malayalam, Urdu, Arabic, French, German, Spanish, Japanese, Korean, Chinese, Russian, Portuguese, and many more.

---

## 🧪 Example Translations

| Input | Output |
|------|------|
| main ghar ja raha hun | I am going home. |
| mujhe nahi khaana | I don't want to eat. |
| naan veliya poren | I am going outside. |
| aap kya kar rahe ho | What are you doing? |

---

## 📡 API Endpoints

### POST /api/translate

**Request**
\`\`\`json
{
  "text": "main ghar ja raha hun",
  "source_lang": "auto",
  "target_lang": "en"
}
\`\`\`

**Response**
\`\`\`json
{
  "translated_text": "I am going home.",
  "detected_language": "hi",
  "target_lang": "en",
  "translation_engine": "gemini"
}
\`\`\`

---

### POST /api/detect

Detects the language of input text.

---

## 🛡️ Error Handling

If Gemini quota is exceeded:
1. Automatically switches to Google Translate fallback.
2. If fallback is also unavailable, a friendly error message is shown.

---

## 📸 Highlights

- Premium glassmorphism interface
- Real-time translation panel
- Voice input and text-to-speech
- Translation history
- Dark / Light mode

---

## 📄 License

MIT License

---

## 👨‍💻 Author

**Mohammed Athar K**

- GitHub: https://github.com/kmdathar07
- Email: kmdathar07@gmail.com

---
Built with ❤️ using React, FastAPI, and Google Gemini AI.
