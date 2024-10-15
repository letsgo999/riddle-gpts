import streamlit as st
   from openai import OpenAI
   import os

   # OpenAI API Key를 환경 변수에서 불러오기
   client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

   def generate_riddle():
       # GPT-4 엔진을 사용한 수수께끼 생성
       response = client.chat.completions.create(
           model="gpt-4",  # 사용 가능한 최신 모델로 변경
           messages=[
               {"role": "system", "content": "You are a riddle master."},
               {"role": "user", "content": "Give me a riddle."}
           ],
           max_tokens=100  # 수수께끼를 만들기 위한 적당한 토큰 수
       )
       return response.choices[0].message.content.strip()

   def check_answer(user_answer, riddle):
       # GPT-4 엔진을 사용한 정답 확인
       response = client.chat.completions.create(
           model="gpt-4",  # 사용 가능한 최신 모델로 변경
           messages=[
               {"role": "system", "content": "You are a riddle master."},
               {"role": "user", "content": f"The riddle is: '{riddle}'. Is the answer '{user_answer}' correct?"}
           ],
           max_tokens=50  # 정답 확인을 위한 적당한 토큰 수
       )
       return response.choices[0].message.content.strip()

   # Streamlit UI 설정
   st.title("Riddle Game with GPT-4")

   if "riddle" not in st.session_state:
       st.session_state["riddle"] = generate_riddle()

   st.write("Riddle: " + st.session_state["riddle"])

   user_answer = st.text_input("Your Answer")

   if st.button("Submit Answer"):
       if user_answer:
           result = check_answer(user_answer, st.session_state["riddle"])
           st.write(result)
       else:
           st.write("Please enter an answer.")

   if st.button("Next Riddle"):
       st.session_state["riddle"] = generate_riddle()
       st.experimental_rerun()