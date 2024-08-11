from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from url_shortener.presentation.api import router
from config import settings
from url_shortener.infrastructure.dependencies import get_url_service

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.API_PREFIX, dependencies=[Depends(get_url_service)])


@app.get("/")
def health_check():
    return {"message": "ok"}
