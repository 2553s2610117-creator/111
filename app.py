import streamlit as st
import pandas as pd
from datetime import datetime
import os

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="학생 집중 관리 앱",
    page_icon="📚",
    layout="centered"
)

st.title("📚 학생 집중 관리 앱")
st.write("학생들의 공부 시간과 집중도를 관리해보세요!")

# -----------------------------
# 데이터 파일 설정
# -----------------------------
DATA_FILE = "study_log.csv"

# CSV 파일 생성
if not os.path.exists(DATA_FILE):
    empty_df = pd.DataFrame(
        columns=["날짜", "과목", "공부시간", "집중도"]
    )
    empty_df.to_csv(DATA_FILE, index=False)

# CSV 읽기
try:
    df = pd.read_csv(DATA_FILE)
except:
    df = pd.DataFrame(
        columns=["날짜", "과목", "공부시간", "집중도"]
    )

# -----------------------------
# 공부 기록 입력
# -----------------------------
st.header("✏️ 공부 기록 추가")

subject = st.selectbox(
    "과목 선택",
    ["국어", "영어", "수학", "과학", "사회", "코딩", "기타"]
)

study_time = st.slider(
    "공부 시간 (분)",
    min_value=10,
    max_value=300,
    value=60
)

focus_score = st.slider(
    "집중도 점수",
    min_value=1,
    max_value=10,
    value=7
)

# 저장 버튼
if st.button("저장하기"):

    new_row = {
        "날짜": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "과목": subject,
        "공부시간": study_time,
        "집중도": focus_score
    }

    new_df = pd.DataFrame([new_row])

    df = pd.concat([df, new_df], ignore_index=True)

    df.to_csv(DATA_FILE, index=False)

    st.success("✅ 공부 기록이 저장되었습니다!")

# -----------------------------
# 통계
# -----------------------------
st.header("📊 공부 통계")

if len(df) > 0:

    total_time = int(df["공부시간"].sum())
    average_focus = round(df["집중도"].mean(), 1)

    col1, col2 = st.columns(2)

    col1.metric("총 공부 시간", f"{total_time}분")
    col2.metric("평균 집중도", f"{average_focus}/10")

    st.subheader("과목별 공부 시간")

    chart_data = df.groupby("과목")["공부시간"].sum()

    st.bar_chart(chart_data)

    st.subheader("최근 공부 기록")

    st.dataframe(df[::-1], use_container_width=True)

else:
    st.info("아직 저장된 데이터가 없습니다.")

# -----------------------------
# 집중 팁
# -----------------------------
st.header("🔥 집중 팁")

tips = [
    "25분 집중 후 5분 쉬기",
    "휴대폰 멀리 두기",
    "오늘 목표 먼저 정하기",
    "조용한 환경 만들기"
]

for tip in tips:
    st.write("✅", tip)
