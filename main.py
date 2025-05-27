from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from routers import face, whisper, yolo, youtube
app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="www/static"), name="static")

@app.get("/")
def main_page():
    return FileResponse("www/templates/index.html")

app.include_router(yolo.router, prefix="/api/yolo")
app.include_router(whisper.router, prefix="/api/whisper")
app.include_router(face.router, prefix="/api/face")
app.include_router(youtube.router, prefix="/api/youtube")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
