# Rodam AI Chatbot

OpenAI Assistant API를 사용한 Streamlit 기반 챗봇 애플리케이션입니다.

## 기능

- OpenAI Assistant API를 통한 AI 대화
- 실시간 채팅 인터페이스
- 대화 히스토리 관리
- 새 대화 시작 기능
- Streamlit Cloud 배포 지원

## 로컬 실행

### 1. 저장소 클론

```bash
git clone <repository-url>
cd chatbot_mac
```

### 2. 가상환경 생성 및 활성화

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정

`.streamlit/secrets.toml` 파일을 생성하고 다음 내용을 추가하세요:

```toml
OPENAI_API_KEY = "your_openai_api_key_here"
ASSISTANT_ID = "your_assistant_id_here"
```

### 5. 애플리케이션 실행

```bash
streamlit run app.py
```

## Streamlit Cloud 배포

### 1. GitHub에 저장소 업로드

이 저장소를 GitHub에 업로드하세요.

### 2. Streamlit Cloud에서 앱 배포

1. [Streamlit Cloud](https://share.streamlit.io/)에 접속
2. "New app" 클릭
3. GitHub 저장소 선택
4. 메인 파일 경로: `app.py`
5. "Deploy!" 클릭

### 3. Secrets 설정

Streamlit Cloud 대시보드에서 "Secrets" 탭으로 이동하여 다음 값들을 설정하세요:

```toml
OPENAI_API_KEY = "your_actual_openai_api_key"
ASSISTANT_ID = "your_actual_assistant_id"
```

## 사용법

1. 메시지를 입력하고 Enter를 누르세요
2. AI가 응답을 생성할 때까지 기다리세요
3. 새 대화를 시작하려면 사이드바의 '새 대화 시작' 버튼을 클릭하세요

## 요구사항

- Python 3.7+
- Streamlit 1.50.0+
- OpenAI 2.1.0+

## 보안 주의사항

- API 키는 절대 코드에 하드코딩하지 마세요
- 로컬 개발 시에는 `.streamlit/secrets.toml` 파일을 사용하세요
- Streamlit Cloud 배포 시에는 대시보드의 Secrets 기능을 사용하세요
- `.streamlit/secrets.toml` 파일은 `.gitignore`에 추가하여 버전 관리에서 제외하세요
