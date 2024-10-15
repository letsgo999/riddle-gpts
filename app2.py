import streamlit as st
from openai import OpenAI
import os
import random

# OpenAI API Key 확인
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API 키가 설정되지 않았습니다. 환경 변수를 확인해주세요.")
    st.stop()

# OpenAI 클라이언트 초기화
try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    st.error(f"OpenAI 클라이언트 초기화 중 오류 발생: {str(e)}")
    st.stop()

@st.cache_data(ttl=3600)  # 1시간 동안 캐시 유지
def generate_riddles(num_riddles=10):
    riddles = []
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 창의적이고 재미있는 한국어 수수께끼를 만드는 전문가입니다. 어린이부터 어른까지 모두가 즐길 수 있는 명확하고 흥미로운 수수께끼를 만들어주세요."},
                {"role": "user", "content": f"서로 다른 주제의 재미있고 명확한 한국어 수수께끼 {num_riddles}개를 만들어주세요. 각 수수께끼는 새로운 줄에 시작하고, 답은 괄호 안에 포함시켜주세요."}
            ],
            max_tokens=500
        )
        riddles_text = response.choices[0].message.content.strip().split('\n')
        for riddle in riddles_text:
            if '(' in riddle and ')' in riddle:
                question, answer = riddle.rsplit('(', 1)
                answer = answer.rstrip(')')
                riddles.append((question.strip(), answer.strip()))
    except Exception as e:
        st.error(f"수수께끼 생성 중 오류 발생: {str(e)}")
    return riddles

def check_answer(user_answer, correct_answer):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 수수께끼 답변을 평가하는 전문가입니다. 사용자의 답변이 정답과 의미상 일치하는지 판단하고, 재미있고 격려하는 방식으로 피드백을 제공해주세요."},
                {"role": "user", "content": f"수수께끼의 정답은 '{correct_answer}'이고, 사용자의 답변은 '{user_answer}'입니다. 이 답변이 맞는지 평가하고 피드백을 해주세요."}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"답변 확인 중 오류 발생: {str(e)}")
        return "답변을 확인할 수 없습니다."

# Streamlit UI 설정
st.title("🧩 GPT-4 수수께끼 게임 🧠")

# 세션 상태 초기화
if "riddles" not in st.session_state:
    st.session_state.riddles = generate_riddles()
if "current_riddle_index" not in st.session_state:
    st.session_state.current_riddle_index = 0
if "result" not in st.session_state:
    st.session_state.result = ""

# 현재 수수께끼 표시
current_riddle, current_answer = st.session_state.riddles[st.session_state.current_riddle_index]
st.write("### 수수께끼:")
st.write(current_riddle)

# 사용자 입력
user_answer = st.text_input("당신의 답변")

# 제출 버튼
if st.button("제출하기"):
    if user_answer:
        st.session_state.result = check_answer(user_answer, current_answer)
    else:
        st.session_state.result = "답을 입력해주세요."

# 결과 표시
if st.session_state.result:
    st.write(st.session_state.result)

# 다음 수수께끼 버튼
if st.button("다음 수수께끼"):
    st.session_state.current_riddle_index = (st.session_state.current_riddle_index + 1) % len(st.session_state.riddles)
    st.session_state.result = ""
    st.rerun()

# 새로운 수수께끼 세트 생성 버튼
if st.button("새로운 수수께끼 세트 생성"):
    st.session_state.riddles = generate_riddles()
    st.session_state.current_riddle_index = 0
    st.session_state.result = ""
    st.rerun()