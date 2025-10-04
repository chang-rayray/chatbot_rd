# AI Assistant Chatbot

OpenAI Assistant API를 사용한 Streamlit 기반 챗봇 애플리케이션입니다.

## 기능

- OpenAI Assistant API를 통한 AI 대화
- 실시간 채팅 인터페이스
- 대화 히스토리 관리
- 새 대화 시작 기능

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 애플리케이션 실행

```bash
streamlit run app.py
```

### 3. 브라우저에서 확인

애플리케이션이 실행되면 자동으로 브라우저가 열리거나, 터미널에 표시되는 URL로 접속하세요.

## 사용법

1. 메시지를 입력하고 Enter를 누르세요
2. AI가 응답을 생성할 때까지 기다리세요
3. 새 대화를 시작하려면 사이드바의 '새 대화 시작' 버튼을 클릭하세요

## 설정

- OpenAI API 키와 Assistant ID는 `app.py` 파일에 하드코딩되어 있습니다.
- 보안을 위해 실제 운영 환경에서는 환경 변수를 사용하는 것을 권장합니다.

## 요구사항

- Python 3.7+
- Streamlit 1.28.0+
- OpenAI 1.3.0+
