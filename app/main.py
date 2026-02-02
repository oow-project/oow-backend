from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config.redis import init_redis
from app.config.supabase import init_supabase
from app.exceptions import AppError
from app.routers import chat, heroes
from app.scheduler.scheduler import shutdown_scheduler, start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_supabase()
    await init_redis()
    start_scheduler()
    yield
    shutdown_scheduler()


app = FastAPI(title="OOW.GG API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(heroes.router)
app.include_router(chat.router)


@app.exception_handler(AppError)
async def handle_app_error(request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.message})


@app.exception_handler(Exception)
async def handle_unexpected(request, exc: Exception):
    return JSONResponse(
        status_code=500, content={"error": "서버 내부 오류가 발생했습니다"}
    )


@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now(UTC).isoformat()}
