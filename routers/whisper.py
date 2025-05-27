from fastapi import APIRouter, UploadFile, File, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


from services.whisper_service import transcribe

import whisper

router = APIRouter()

templates = Jinja2Templates(directory="www/templates")

def get_whisper_model():
    return whisper.load_model("base")


@router.get("/whisper", response_class=HTMLResponse)
async def whisper_router(request: Request):
    return templates.TemplateResponse("whisper.html", {"request": request})

@router.post("/transcribe")
async def transcribe_router(file: UploadFile = File(...), model=Depends(get_whisper_model)):
    try:
        result = await transcribe(file, model)
        return result
    except Exception as e:
        raise HTTPException(500, detail=str(e))
