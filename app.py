import streamlit as st
from openai import OpenAI
from datetime import datetime
import time

# --------------------------------------------------
# 환경 설정
# --------------------------------------------------
api_key = st.secrets.get("OPENAI_API_KEY")
ASSISTANT_ID = st.secrets.get("ASSISTANT_ID")

if not api_key:
    st.error("⚠️ OpenAI API 키가 설정되지 않았습니다. Streamlit Cloud의 Secrets 설정을 확인해주세요.")
    st.stop()

if not ASSISTANT_ID:
    st.error("⚠️ Assistant ID가 설정되지 않았습니다. Streamlit Cloud의 Secrets 설정을 확인해주세요.")
    st.stop()

client = OpenAI(api_key=api_key)

# --------------------------------------------------
# 에러 처리 헬퍼
# --------------------------------------------------
def handle_error(e, context="작업"):
    error_msg = str(e)
    if "401" in error_msg or "invalid_api_key" in error_msg:
        st.error("🔑 API 키가 유효하지 않습니다.")
    elif "429" in error_msg:
        st.error("⏰ API 요청 한도를 초과했습니다. 잠시 후 다시 시도해주세요.")
    else:
        st.error(f"{context} 중 오류 발생: {error_msg}")

# --------------------------------------------------
# OpenAI API 관련 함수
# --------------------------------------------------
def create_thread():
    try:
        thread = client.beta.threads.create()
        return thread.id
    except Exception as e:
        handle_error(e, "스레드 생성")
        return None

def send_message(thread_id, message):
    try:
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message
        )
        return True
    except Exception as e:
        handle_error(e, "메시지 전송")
        return False

def run_assistant(thread_id):
    try:
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID
        )
        return run.id
    except Exception as e:
        handle_error(e, "어시스턴트 실행")
        return None

def get_run_status(thread_id, run_id):
    try:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        return run.status
    except Exception as e:
        handle_error(e, "실행 상태 확인")
        return None

def wait_for_completion(thread_id, run_id, max_retries=30, delay=1):
    """응답이 완료될 때까지 대기 (최대 30초)"""
    for _ in range(max_retries):
        status = get_run_status(thread_id, run_id)
        if status == "completed":
            return True
        elif status == "failed":
            return False
        time.sleep(delay)
    return False  # 제한 시간 초과

def get_messages(thread_id):
    try:
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        return messages.data
    except Exception as e:
        handle_error(e, "메시지 가져오기")
        return []

def extract_assistant_response(messages):
    """메시지 중에서 assistant 응답만 추출"""
    assistant_message = next((m for m in messages if m.role == "assistant"), None)
    if not assistant_message:
        return None
    return "".join(
        content.text.value
        for content in assistant_message.content
        if content.type == "text"
    )

# --------------------------------------------------
# 메인 앱
# --------------------------------------------------
def main():
    st.set_page_config(
        page_title="Rodam AI Chatbot",
        page_icon="🤖",
        layout="wide"
    )

    st.title("🤖 Rodam AI Chatbot")
    st.markdown("OpenAI 기반 로담 챗봇")

    # 사이드바
    with st.sidebar:
        st.header("설정")
        if st.button("새 대화 시작", type="primary"):
            st.session_state.clear()
            st.rerun()

        st.markdown("---")
        st.markdown("### 사용법")
        st.markdown("""
        1. 메시지를 입력하고 Enter를 누르세요
        2. AI가 응답을 생성할 때까지 기다리세요
        3. 새 대화를 시작하려면 '새 대화 시작' 버튼을 클릭하세요
        """)

    # 대화 이력 표시
    for msg in st.session_state.get("messages", []):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 사용자 입력
    if prompt := st.chat_input("메시지를 입력하세요..."):
        # 사용자 메시지 출력
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 스레드 생성 (최초 대화일 경우)
        if "thread_id" not in st.session_state:
            st.session_state.thread_id = create_thread()
            if not st.session_state.thread_id:
                return

        # 메시지 전송
        if not send_message(st.session_state.thread_id, prompt):
            return

        # 어시스턴트 실행
        run_id = run_assistant(st.session_state.thread_id)
        if not run_id:
            return

        # 실행 완료 대기
        with st.spinner("AI가 응답을 생성 중..."):
            if not wait_for_completion(st.session_state.thread_id, run_id):
                st.error("AI 응답 생성에 실패했습니다.")
                return

        # 응답 가져오기
        messages = get_messages(st.session_state.thread_id)
        response = extract_assistant_response(messages)

        if response:
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
        else:
            st.error("AI 응답을 찾을 수 없습니다.")

# --------------------------------------------------
# 실행
# --------------------------------------------------
if __name__ == "__main__":
    main()

