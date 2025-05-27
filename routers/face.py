from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
import mediapipe as mp
from services.face_service import register_face, recognize_face
from fastapi.responses import FileResponse

router = APIRouter()
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh

def get_face_detection():
    return mp_face_detection.FaceDetection(
        min_detection_confidence=0.5,
    )

def get_face_mesh():
    return mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        min_detection_confidence=0.5
    )

@router.get("/face_detection")
async def face_detection():
    return FileResponse("www/templates/face_detection.html")

@router.post("/register")
async def register_face_route(
    image: UploadFile = File(...),
    name: str = Form(...),
    face_mesh=Depends(get_face_mesh)
):
    try:
        return await register_face(image, name, face_mesh)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recognize")
async def recognize_face_route(
    image: UploadFile = File(...),
    face_detection=Depends(get_face_detection),
    face_mesh=Depends(get_face_mesh)
):
    return await recognize_face(image, face_detection, face_mesh)
