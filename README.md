# 🌐 LinguaFlow — AI-Powered Real-Time Translator

A premium full-stack translation web application that delivers real-time multilingual translation with voice input/output, automatic language detection, and a modern glassmorphism interface.

## ✨ Features

- 🧠 Powered by Google Gemini AI
- 🔄 Automatic fallback to MyMemory API when Gemini quota is exceeded
- ⚡ Real-time translation as you type
- 🌍 Supports 30+ languages
- 🔄 Automatic language detection
- 🎙️ Voice-to-text input
- 🔊 Text-to-speech output
- 📋 Translation history with search
- 🌙 Dark and light mode
- 📥 Download translations as text files
- 📋 One-click copy to clipboard
- 🔁 Instant language swapping
- 📊 Live character count

## 🛠️ Tech Stack

- Frontend: React 18 + Vite
- Backend: FastAPI
- AI Engine: Google Gemini API (`gemini-2.5-flash-lite`)
- Fallback Engine: MyMemory Translation API
- Voice: Web Speech API
- Storage: LocalStorage
- Deployment: Vercel + Render

## 📸 Highlights

- Premium glassmorphism UI
- Responsive design for desktop and mobile
- High-quality translation with automatic failover
- Production-ready architecture

## 🚀 Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
python3 -m uvicorn main:app --reload --port 8000

### Frontend

```bash
cd frontend
npm install
npm run dev

🔐 Environment Variables
Backend .env
GEMINI_API_KEY=your_api_key_here
MODEL_NAME=gemini-2.5-flash-lite
Frontend .env
VITE_API_URL=http://127.0.0.1:8000/api

🌍 Supported Languages

English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese, Arabic, Hindi, Tamil, Telugu, Malayalam, Bengali, and many more.

🚀 Deployment
Frontend: Vercel
Backend: Render

📄 License

MIT License