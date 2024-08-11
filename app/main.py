from fastapi import BackgroundTasks, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from url_shortener.application.services import URLService
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

def delete_expired_urls(url_service: URLService):
    deleted_count = url_service.delete_expired_urls()
    print(f"Deleted {deleted_count} expired URLs")

@app.get("/")
async def root(background_tasks: BackgroundTasks, url_service: URLService = Depends(get_url_service)):
    background_tasks.add_task(delete_expired_urls, url_service)
    return {"message": "Welcome to URL Shortener API"}

