import base64
import cv2
from ultralytics import YOLO

from utils.image_utils import read_image

async def detect_objects(image_file):
    img = await read_image(image_file)

    yolo_model = YOLO("yolov8n.pt")

    results = yolo_model(img)
    result = results[0]

    detected_objects = []
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        cls_name = result.names[cls_id]

        detected_objects.append({
            "class": cls_name,
            "confidence": round(conf, 2),
            "bbox": [x1, y1, x2, y2]
        })

    # 바운딩 박스가 있는 이미지 생성
    for obj in detected_objects:
        x1, y1, x2, y2 = obj["bbox"]
        cls_name = obj["class"]
        conf = obj["confidence"]

        # 바운딩 박스 그리기
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # 레이블 텍스트
        label = f"{cls_name} {conf:.2f}"

        # 텍스트 배경
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(img, (x1, y1 - 20), (x1 + w, y1), (0, 255, 0), -1)

        # 텍스트 추가
        cv2.putText(img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

    # 이미지를 base64로 인코딩
    _, buffer = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    return {
        "detected_objects": detected_objects,
        "processed_image": f"data:image/jpeg;base64,{img_base64}"
    }