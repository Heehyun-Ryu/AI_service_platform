import cv2
import numpy as np
import pickle
from pathlib import Path
from fastapi import HTTPException
from utils.image_utils import read_image

REGISTERED_FACES_DIR = Path("registered_faces")
REGISTERED_FACES_DIR.mkdir(exist_ok=True)

def extract_face_embedding(image, face_mesh):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_image)

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]
        landmarks = []
        for landmark in face_landmarks.landmark:
            landmarks.extend([landmark.x, landmark.y, landmark.z])
        return np.array(landmarks)
    return None

def compare_embeddings(embedding1, embedding2):
    if embedding1 is None or embedding2 is None:
        return 0.0
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    similarity = dot_product / (norm1 * norm2)
    return similarity

def get_face_detection_info(image, face_detection):
    """얼굴 감지 정보 추출"""
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_image)

    if results.detections:
        detection = results.detections[0]
        bbox = detection.location_data.relative_bounding_box
        h, w, _ = image.shape

        return {
            "face_detected": True,
            "face_location": {
                "left": int(bbox.xmin * w),
                "top": int(bbox.ymin * h),
                "width": int(bbox.width * w),
                "height": int(bbox.height * h)
            }
        }

    return {"face_detected": False}

async def register_face(image_file, name, face_mesh):
    if not name.strip():
        raise HTTPException(status_code=400, detail="이름을 입력해주세요.")

    img = await read_image(image_file)
    embedding = extract_face_embedding(img, face_mesh)

    if embedding is None:
        raise HTTPException(status_code=400, detail="얼굴을 찾을 수 없습니다.")

    for file in REGISTERED_FACES_DIR.glob("*.pkl"):
        with open(file, "rb") as f:
            registered_data = pickle.load(f)
            registered_embedding = registered_data["embedding"]
            similarity = compare_embeddings(embedding, registered_embedding)
            if similarity > 0.95:
                raise HTTPException(
                    status_code=400,
                    detail=f"이미 등록된 얼굴입니다. (유사도: {similarity * 100:.1f}%)"
                )
    face_data = {
        "name": name,
        "embedding": embedding
    }
    filename = f"{name}_{len(list(REGISTERED_FACES_DIR.glob('*.pkl')))}.pkl"
    with open(REGISTERED_FACES_DIR / filename, "wb") as f:
        pickle.dump(face_data, f)
    return {"message": f"{name}님의 얼굴이 성공적으로 등록되었습니다."}


async def recognize_face(image_file, face_detection,face_mesh):
    img = await read_image(image_file)

    detection_info = get_face_detection_info(img, face_detection)
    print(detection_info)

    embedding = extract_face_embedding(img, face_mesh)
    if embedding is None:
        return {"recognized": False, "message": "얼굴을 찾을 수 없습니다."}

    best_match = None
    best_similarity = 0

    for file in REGISTERED_FACES_DIR.glob("*.pkl"):
        with open(file, "rb") as f:
            registered_data = pickle.load(f)
            registered_embedding = registered_data["embedding"]
            similarity = compare_embeddings(embedding, registered_embedding)

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = registered_data["name"]

    if best_similarity > 0.85:
        results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        num_landmarks = len(results.multi_face_landmarks[0].landmark) if results.multi_face_landmarks else 0

        return {
            **detection_info,
            "recognized": True,
            "name": best_match,
            "confidence": float(best_similarity),
            "num_landmarks": num_landmarks,
            "message": f"{best_match}님으로 인식되었습니다."
        }
    else:
        return {
            **detection_info,
            "recognized": False,
            "confidence": float(best_similarity),
            "message": "등록되지 않은 얼굴입니다."
        }