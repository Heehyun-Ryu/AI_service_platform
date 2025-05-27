from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from services.youtube_service import search_youtube, video_details

router = APIRouter()

templates = Jinja2Templates(directory="www/templates")

@router.get("/youtube", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("youtube.html", {"request": request})

@router.get("/search/{query}")
async def search_query(query: str, max_results: int = 100):
    return await search_youtube(query, max_results)

@router.get("/video/{video_id}")
async def get_video_details(video_id: str):
    return await video_details(video_id)

