# 🌍 LinguaFlow — AI-Powered Real-Time Translator

LinguaFlow is a production-grade AI translation web application built for the Pinnacle Labs Internship.

It provides high-quality translations using Google's Gemini AI and automatically falls back to Google Translate when Gemini quota is exhausted.

---

## ✨ Features

- 🤖 AI-powered translation using Gemini 2.5 Flash Lite
- 🔄 Automatic fallback to Google Translate
- 🌐 Auto language detection
- 🗣️ Voice input (Speech Recognition)
- 🔊 Text-to-Speech output
- 📋 Copy translated text
- 📥 Download translation
- 🌙 Dark and Light themes
- ⚡ Real-time translation mode
- 📱 Fully responsive design
- 🇮🇳 Accurate Roman Hindi/Urdu translation support

---

## 🧠 Translation Architecture

Input Text
→ Auto Language Detection
→ Gemini AI Translation (Primary)
→ If quota exceeded or error
→ Google Translate Fallback
→ Final Accurate Translation

---

## 🎯 Example Translations

| Input | Output |
|------|------|
| main ghar ja raha hun | I am going home |
| mujhe nahi khaana | I don't want to eat |
| haan main galat | Yes, I am wrong |
| aap kya kar rahe hain | What are you doing? |
| मैं घर जा रहा हूँ | I am going home |

---

## 🛠️ Tech Stack

### Frontend
- React.js
- Vite
- JavaScript
- CSS3

### Backend
- FastAPI
- Python 3.11

### AI & Translation
- Google Gemini API
- deep-translator
- langdetect

### Deployment
- Vercel (Frontend)
- Render (Backend)

---

## 📂 Project Structure

linguaflow/
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── .env
│
├── backend/
│   ├── services/
│   │   └── translation_service.py
│   ├── routes/
│   ├── main.py
│   ├── requirements.txt
│   ├── runtime.txt
│   └── .env
│
├── .gitignore
└── README.md

---

## ⚙️ Environment Variables

### Backend (.env)

GEMINI_API_KEY=your_actual_gemini_api_key
MODEL_NAME=gemini-2.5-flash-lite

### Frontend (.env)

VITE_API_URL=https://your-render-backend-url.onrender.com/api

---

## 🚀 Local Installation

### 1. Clone Repository

git clone https://github.com/kmdathar07/LinguaFlow.git
cd LinguaFlow

### 2. Backend Setup

cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

### 3. Frontend Setup

cd ../frontend
npm install
npm run dev

---

## 🌐 Deployment

### Backend Deployment (Render)

Build Command:
pip install -r requirements.txt

Start Command:
uvicorn main:app --host 0.0.0.0 --port \$PORT

Environment Variables:
- GEMINI_API_KEY
- MODEL_NAME=gemini-2.5-flash-lite

### Frontend Deployment (Vercel)

Environment Variable:
- VITE_API_URL=https://your-render-backend-url.onrender.com/api

---

## 🔁 Translation Strategy

### Primary Translator
Gemini 2.5 Flash Lite

### Fallback Translator
Google Translate (deep-translator)

### Language Detection
- langdetect
- Custom Roman Hindi heuristics

---

## 📸 Screenshots

### Main Interface
- Clean modern UI
- Dual translation panels
- Voice and audio controls

### Real-Time Translation
- Instant translation as you type

### Auto Language Detection
- Detects both native and transliterated languages

---

## 💼 Internship Highlights

This project demonstrates:

- AI API integration
- Fallback architecture
- Error handling
- Real-time UX
- Speech recognition
- Production deployment
- Full-stack development

---

## 📈 Performance Features

- Fast translation responses
- Automatic quota handling
- Reliable fallback system
- Responsive UI
- Cross-browser compatibility

---

## 🔐 Security

- API keys stored in environment variables
- Sensitive files excluded via .gitignore
- No secrets exposed in GitHub

---

## 👨‍💻 Author

Mohammed Athar K

- GitHub: https://github.com/kmdathar07
- Email: kmdathar07@gmail.com

---

## 🏢 Internship

Developed as part of the Pinnacle Labs Internship Program.

---

## 📜 License

This project is for educational and internship purposes.

---

## ⭐ Repository

If you like this project, please star the repository.

https://github.com/kmdathar07/LinguaFlow
