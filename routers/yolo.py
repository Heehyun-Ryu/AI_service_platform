from fastapi import APIRouter, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from services.yolo_service import detect_objects

router = APIRouter()
templates = Jinja2Templates(directory="www/templates")

@router.get("/yolo")
async def yolo_detect_page(request: Request):
    return templates.TemplateResponse("yolo_detect.html", {"request": request})

@router.post("/detect")
async def yolo_detect(image: UploadFile = File(...)):
    return await detect_objects(image)
