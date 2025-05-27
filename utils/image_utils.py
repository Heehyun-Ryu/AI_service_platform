import numpy as np
import cv2

async def read_image(upload_file):
    contents = await upload_file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img
