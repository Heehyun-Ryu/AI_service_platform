import tempfile
from fastapi.responses import JSONResponse

import os

async def transcribe(file, model):
    # 임시 파일 생성
    with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
        # 파일 데이터를 임시 파일에 쓰기
        audio_data = await file.read()
        temp_file.write(audio_data)
        temp_file_path = temp_file.name

    try:
        # Whisper 모델은 오디오 파일 경로를 직접 처리 가능
        result = model.transcribe(temp_file_path)

        # 처리 후 임시 차일 삭제
        os.unlink(temp_file_path)

        return JSONResponse(content={"text": result["text"]})
    except Exception as e:
        # 오류 발생 시에도 임시 파일 삭제 시도
        try:
            os.unlink(temp_file_path)
        except:
            pass

        print(f'Error: {e}')
        return JSONResponse(content={"error": str(e)}, status_code=500)

