from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.translate import router as translate_router
from routes.detect import router as detect_router
from routes.tts import router as tts_router

app = FastAPI(
    title="LinguaFlow API",
    description="Production-grade AI Translation API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(translate_router, prefix="/api")
app.include_router(detect_router, prefix="/api")
app.include_router(tts_router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "LinguaFlow API"}
