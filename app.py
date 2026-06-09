import streamlit as st
from google import genai

# 페이지 설정
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💖",
    layout="centered"
)

st.title("💖 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반")

# API Key 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error(
        "GEMINI_API_KEY가 설정되지 않았습니다. "
        "Streamlit Secrets를 확인하세요."
    )
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 초기화 실패: {e}")
    st.stop()

# 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요 💖\n\n"
                "연애, 썸, 이별, 재회, 인간관계 고민을 편하게 이야기해 주세요."
            )
        }
    ]

# 기존 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
user_input = st.chat_input("고민을 입력하세요")

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        try:
            with st.spinner("생각 중..."):

                # 시스템 프롬프트
                system_prompt = """
                당신은 공감 능력이 뛰어난 연애상담 전문가입니다.

                규칙:
                - 친절하고 따뜻하게 답변
                - 사용자의 감정을 존중
                - 단정적으로 판단하지 말 것
                - 실질적인 조언 제공
                - 답변은 한국어로 작성
                - 너무 길지 않게 작성
                """

                # 대화 이력 구성
                history_text = ""

                for msg in st.session_state.messages:
                    role = "사용자" if msg["role"] == "user" else "상담사"
                    history_text += f"{role}: {msg['content']}\n"

                prompt = f"""
                {system_prompt}

                아래는 지금까지의 대화입니다.

                {history_text}

                상담사:
                """

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=prompt
                )

                answer = response.text

        except Exception as e:
            answer = (
                "죄송해요. 응답을 생성하는 중 오류가 발생했습니다.\n\n"
                f"오류 내용: {e}"
            )

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# 사이드바
with st.sidebar:
    st.header("설정")

    if st.button("대화 초기화"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "안녕하세요 💖\n\n"
                    "연애 고민을 편하게 이야기해 주세요."
                )
            }
        ]
        st.rerun()
