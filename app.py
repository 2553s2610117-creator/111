import streamlit as st
from google import genai
from google.genai import types

# 페이지 설정
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💝",
    layout="centered"
)

st.title("💝 AI 연애상담 챗봇")
st.caption("연애 고민을 편하게 이야기해보세요.")

# API 키 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("GEMINI_API_KEY가 Secrets에 설정되지 않았습니다.")
    st.stop()

# Gemini Client 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 초기화 실패: {e}")
    st.stop()

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요 😊\n\n"
                "저는 연애상담 AI입니다.\n"
                "연애, 썸, 이별, 재회, 인간관계 고민 등을 편하게 이야기해주세요."
            )
        }
    ]

# 기존 대화 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
if prompt := st.chat_input("연애 고민을 입력하세요..."):

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini 호출
    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):

            try:
                # 시스템 프롬프트
                system_prompt = """
                당신은 공감 능력이 뛰어난 연애상담 전문가입니다.

                원칙:
                - 사용자의 감정을 존중한다.
                - 현실적이고 건강한 조언을 제공한다.
                - 강요하지 않는다.
                - 지나친 확신을 피한다.
                - 친절하고 자연스러운 한국어로 답변한다.
                """

                # 대화 이력 구성
                conversation_text = system_prompt + "\n\n"

                for m in st.session_state.messages:
                    role = "사용자" if m["role"] == "user" else "상담사"
                    conversation_text += f"{role}: {m['content']}\n"

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=conversation_text,
                    config=types.GenerateContentConfig(
                        temperature=0.8,
                        max_output_tokens=1000,
                    )
                )

                answer = response.text

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:
                error_msg = (
                    "죄송합니다. 답변 생성 중 오류가 발생했습니다.\n\n"
                    f"오류 내용: {str(e)}"
                )

                st.error(error_msg)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_msg
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
                    "안녕하세요 😊\n\n"
                    "저는 연애상담 AI입니다.\n"
                    "무슨 고민이 있으신가요?"
                )
            }
        ]
        st.rerun()

    st.divider()

    st.info(
        "이 서비스는 전문 상담을 대체하지 않습니다.\n\n"
        "심각한 정신건강 문제나 위기 상황에서는 전문가의 도움을 받으세요."
    )
