import streamlit as st
from openai import OpenAI
import os

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

def generate_riddle():
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 수수께끼 전문가입니다. 한국어로 대답해주세요."},
                {"role": "user", "content": "재미있는 한국어 수수께끼를 하나 만들어주세요."}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"수수께끼 생성 중 오류 발생: {str(e)}")
        return "수수께끼를 생성할 수 없습니다."

def check_answer(user_answer, riddle):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 수수께끼 전문가입니다. 한국어로 대답해주세요."},
                {"role": "user", "content": f"다음 수수께끼의 답이 '{user_answer}'가 맞나요? 수수께끼: '{riddle}'"}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"답변 확인 중 오류 발생: {str(e)}")
        return "답변을 확인할 수 없습니다."

# Streamlit UI 설정
st.title("GPT-4 수수께끼 게임")

# 세션 상태 초기화
if "riddle" not in st.session_state:
    st.session_state.riddle = generate_riddle()
if "answer" not in st.session_state:
    st.session_state.answer = ""

st.write("수수께끼: " + st.session_state.riddle)

# 사용자 입력 처리
def process_answer():
    if st.session_state.answer:
        result = check_answer(st.session_state.answer, st.session_state.riddle)
        st.write(result)
    else:
        st.write("답을 입력해주세요.")

# 입력 폼
with st.form(key='answer_form', clear_on_submit=True):
    st.text_input("당신의 답변", key="answer", on_change=process_answer)
    submitted = st.form_submit_button("제출하기")
    if submitted:
        process_answer()

# 다음 수수께끼 버튼
if st.button("다음 수수께끼"):
    st.session_state.riddle = generate_riddle()
    st.session_state.answer = ""  # 답변 입력창 초기화
    st.rerun()
