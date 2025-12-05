from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from datetime import datetime
import uvicorn

app = FastAPI(
    title="FastAPI with Nginx",
    description="Lightweight FastAPI app behind Nginx (root auto-redirects to /docks)",
    version="1.0.0",
)

# Простая CORS-конфигурация (открытая). Замените allow_origins по необходимости.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def utc_now_iso() -> str:
    """UTC timestamp in ISO format."""
    return datetime.utcnow().isoformat()


@app.get("/", include_in_schema=False)
async def root_redirect():
    """Автоматический редирект на /docks."""
    return RedirectResponse(url="/docks", status_code=307)


@app.get("/docks")
async def docks_info():
    """Целевая страница после редиректа."""
    return {
        "service": "FastAPI with Nginx",
        "status": "running",
        "timestamp": utc_now_iso(),
        "note": "Root (/) redirects here."
    }


@app.get("/health")
async def health_check():
    """Health check."""
    return {"status": "healthy", "timestamp": utc_now_iso()}


@app.get("/api/time")
async def get_current_time():
    """Текущее время сервера (UTC)."""
    return {"timestamp": utc_now_iso(), "timezone": "UTC", "format": "ISO 8601"}


@app.get("/api/hello/{name}")
async def say_hello(name: str):
    """Персональное приветствие. Имя только буквы (включая Unicode)."""
    if not name.isalpha():
        raise HTTPException(status_code=400, detail="Name should contain only letters")
    return {"message": f"Hello, {name}! Welcome to FastAPI with Nginx!", "timestamp": utc_now_iso()}


if __name__ == "__main__":
    # Для разработки можно запускать: python main.py
    # На проде рекомендую запуск через: uvicorn main:app --host 0.0.0.0 --port 8000 --workers N
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
