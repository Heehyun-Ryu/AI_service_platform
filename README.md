# 문제정의

다양한 AI 기능에 대한 발전과 수요가 증가하고 있습니다.  AI 기술과 외부 API 사용으로 발전된 AI의 모습을 개략적으로 보여주자 합니다. 

해당 프로젝트에서는 이미지, 음성과 같은 미디어를 처리하는 것을 보여주고자 다음과 같이 문제를 정의했습니다.

- **다양한 AI 기능 통합 필요**: 얼굴 인식, 음성 변환, 객체 탐지, 유튜브 검색 등 다양한 AI 기능을 하나의 플랫폼에서 제공
- **실시간 처리 요구**: 웹 기반 실시간 객체 탐지 및 얼굴 인식 요구사항 대응 필요
- **확장성 부족 문제 해결**: 모듈화된 확장 가능 아키텍처 구축 필요

# 요구사항 분석

| 기능 영역 | 기술 요구사항 | 비기능 요구사항 |
| --- | --- | --- |
| 실시간 음성 인식 | Whisper base 모델 활용  | 5초 이내 변환 |
| 객체 인식 | YOLOv8n 경량화 모델 적용   | 95% 이상의 정확도 |
| YouTube 동영상 검색 | Google API 사용     | 3초 이내 응답 |
| 안면 인식 | MediaPipe 기반 실시간 처리  | 95% 이상의 정확도 |

# 기술 스택 및 아키텍처

**Frontend**

  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB"> <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> <img src="https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css&logoColor=white">


**Backend**

<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white">


**AI Framework**

<img src="https://img.shields.io/badge/YOLO-FFBB00?style=for-the-badge">  <img src="https://img.shields.io/badge/Whisper-262626?style=for-the-badge&logo=openai&logoColor=white"> <img src="https://img.shields.io/badge/MediaPipe-FF6F00?style=for-the-badge&logo=google&logoColor=white">

**API**

<img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white">

![Image](https://github.com/user-attachments/assets/ada33770-7e07-4465-9212-d70cd350b634)

# 핵심 알고리즘 및 처리 매커니즘

### (1) 실시간 음성 인식 서비스

위 서비스는 Whisper 모델을 활용하여 오디오에서 음성 언어를 감지하고, 텍스트로 변환(transcribe)하는 서비스를 제공합니다.

Whishper 모델은 OpenAI에 의해 개발된 자동 음성 인식 모델로 Transfomer 기반의 sequence-to-sequence 모델로 구성됩니다.

1) 사용자의 음성을 녹음 후 'WebM' 포맷으로 병합 후 FormData형식으로 /api/whisper/transcribe로 POST 요청

2) `Whisper` 모델을 로드한 후 transcribe 결과를 JSON 형식으로 응답

3) 응답 결과를 박스 형태로 화면에 생성

### (2) YOLOv8 객체인식

위 서비스는 YOLO 모델을 활용하여 카메라로 찍은 이미지에서 객체를 감지하고, 객체 위치와 객체에 대한 정보를 표시하는 서비스를 제공합니다

1) 카메라 이미지 캡쳐 및 이미지 POST 요청

2) `YOLOv8` 모델로 객체 감지 수행

3) 수행 결과 객체의 바운딩 박스와 객체의 정보를 나타낸 이미지 반환

4) 응답 받은 이미지를 실시간 표시

5) 10초마다 객체를 감지하고, 사용자가 객체 감지 버튼을 누르는 경우에 객체 감지 및 결과 표시

### (3) YouTube 동영상 검색

본 서비스은 사용자가 입력한 검색어에 대해 YouTube API를 통해 관련 동영상을 검색하고, 검색된 동영상을 리스트 형태로 클라이언트에 보여주며, 각각의 동영상에 대해 상세 정보를 제공하는 기능을 수행합니다.

1) 사용자가 검색어를 입력하고 `searchVideos()` 호출

2) `/api/youtube/search/<검색어>` 경로로 `fetch` 요청

3) 결과 수신 후 `setVideos(data.results)`로 상태 저장 → 화면에 렌더링

4) 사용자가 동영상을 클릭하면 `window.open()`을 통해 YouTube 웹페이지로 이동

### (4) 안면인식 서비스

본 서비스는 `MediaPipe`의 `FaceMesh`와 `FaceDetection`을 사용용하여 사용자 얼굴 등록 및 인식 서비스를 제공합니다. 

등록은 `FaceMesh`를 이용하여 얼굴의 3D 좌표를 추출하여 특징 값과 사용자를 함께 저장합니다. 

인식은 `FaceDetection`를 이용하여 얼굴을 탐지하고, `FaceMesh`를 이용해 특징 값을 추출한 뒤 저장된 값과 **cosine similarity** 방식으로 유사도를 비교하여 결과를 나타냅니다.

1) 등록할 이름 입력 후 등록 완료 버튼 클릭

2) 카메라 캡쳐 이미지와 등록할 이름 POST 요청

3) MediaPipe의 FaceMesh를 이용하여 얼굴 특징값 추출 후 저장

4) 안면 인식 버튼 클릭 시 카메라 캡쳐 이미지 POST 요청

5) MediaPipe의 FaceDetection과 FacceMesh를 이용하여 얼굴 탐지 및 특징값 분석

6) **cosine similarity**로 유사도 측정 후 결과 반환(인식 여부 + 얼굴 위치 좌표)

# 결론 & 향후 개선 방안

- 4개 주요 AI 모듈 성공적 통합
- 모듈간 독립성 확보로 확장성 보장
- 사용자 친화적 웹 인터페이스 제공

본 프로젝트는 다양한 인공지능 기능을 FastAPI 기반으로 통합하여 하나의 웹 API 서비스로 제공하는 데 성공하였습니다. 각 기능이 독립적이면서도 통합된 구조로 운영되며, 실제 애플리케이션에 쉽게 연동 가능하도록 설계되었습니다.

- **보안 강화**: JWT 기반 인증 시스템 구축
- **모니터링 고도화**: 실시간 성능 대시보드 구축
- **OCR 기능**: 문서/이미지 텍스트 추출 서비스 개발
- **DB 연동** : 임베딩 및 결과 기록 저장
