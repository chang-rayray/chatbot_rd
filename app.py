import streamlit as st
import openai
from datetime import datetime
import json

# OpenAI API 설정
openai.api_key = "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"
ASSISTANT_ID = "asst_JEYa2Ve77FdlOZQQc23AN2X5"

# 페이지 설정
st.set_page_config(
    page_title="Rodam AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "run_id" not in st.session_state:
    st.session_state.run_id = None

def create_thread():
    """새로운 대화 스레드 생성"""
    try:
        thread = openai.beta.threads.create()
        return thread.id
    except Exception as e:
        st.error(f"스레드 생성 중 오류가 발생했습니다: {str(e)}")
        return None

def send_message(thread_id, message):
    """메시지를 스레드에 추가"""
    try:
        openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message
        )
        return True
    except Exception as e:
        st.error(f"메시지 전송 중 오류가 발생했습니다: {str(e)}")
        return False

def run_assistant(thread_id):
    """어시스턴트 실행"""
    try:
        run = openai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID
        )
        return run.id
    except Exception as e:
        st.error(f"어시스턴트 실행 중 오류가 발생했습니다: {str(e)}")
        return None

def get_run_status(thread_id, run_id):
    """실행 상태 확인"""
    try:
        run = openai.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        return run.status
    except Exception as e:
        st.error(f"실행 상태 확인 중 오류가 발생했습니다: {str(e)}")
        return None

def get_messages(thread_id):
    """스레드의 메시지들 가져오기"""
    try:
        messages = openai.beta.threads.messages.list(thread_id=thread_id)
        return messages.data
    except Exception as e:
        st.error(f"메시지 가져오기 중 오류가 발생했습니다: {str(e)}")
        return []

def main():
    st.title("🤖 Rodam AI Chatbot")
    st.markdown("OpenAI로 로담데이터를 사용한 챗봇입니다.")
    
    # 사이드바
    with st.sidebar:
        st.header("설정")
        
        if st.button("새 대화 시작", type="primary"):
            st.session_state.messages = []
            st.session_state.thread_id = None
            st.session_state.run_id = None
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 사용법")
        st.markdown("""
        1. 메시지를 입력하고 Enter를 누르세요
        2. AI가 응답을 생성할 때까지 기다리세요
        3. 새 대화를 시작하려면 '새 대화 시작' 버튼을 클릭하세요
        """)
    
    # 메시지 표시 영역
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # 사용자 입력
    if prompt := st.chat_input("메시지를 입력하세요..."):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 스레드가 없으면 새로 생성
        if st.session_state.thread_id is None:
            st.session_state.thread_id = create_thread()
            if st.session_state.thread_id is None:
                st.error("대화 스레드를 생성할 수 없습니다.")
                return
        
        # 메시지 전송
        if not send_message(st.session_state.thread_id, prompt):
            return
        
        # 어시스턴트 실행
        run_id = run_assistant(st.session_state.thread_id)
        if run_id is None:
            return
        
        st.session_state.run_id = run_id
        
        # 실행 완료까지 대기
        with st.spinner("AI가 응답을 생성하고 있습니다..."):
            while True:
                status = get_run_status(st.session_state.thread_id, run_id)
                if status == "completed":
                    break
                elif status == "failed":
                    st.error("AI 응답 생성에 실패했습니다.")
                    return
                elif status is None:
                    return
        
        # 응답 가져오기
        messages = get_messages(st.session_state.thread_id)
        if messages:
            # 가장 최근 어시스턴트 메시지 찾기
            assistant_message = None
            for message in messages:
                if message.role == "assistant":
                    assistant_message = message
                    break
            
            if assistant_message:
                response_content = ""
                for content in assistant_message.content:
                    if content.type == "text":
                        response_content += content.text.value
                
                # 어시스턴트 응답 추가
                st.session_state.messages.append({"role": "assistant", "content": response_content})
                
                with st.chat_message("assistant"):
                    st.markdown(response_content)
            else:
                st.error("AI 응답을 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
