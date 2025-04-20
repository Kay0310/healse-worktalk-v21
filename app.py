import streamlit as st
from PIL import Image
import datetime
import base64

st.set_page_config(page_title="WORK TALK", layout="wide")

st.markdown("<h1 style='text-align: center;'> <img src='data:image/png;base64,{}' width='200'/> </h1>", unsafe_allow_html=True)

st.markdown("사진 1장 업로드 ➜ 질문 4개 응답 ➜ 저장 ➜ 다음 사진 순서대로 진행해 주세요.")

if "step" not in st.session_state:
    st.session_state.step = 1
if "responses" not in st.session_state:
    st.session_state.responses = []

if st.session_state.step == 1:
    with st.form("input_form"):
        name = st.text_input("이름")
        department = st.text_input("부서")
        uploaded_file = st.file_uploader("작업 사진 업로드", type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("저장하기")
        if submitted and name and department and uploaded_file:
            st.session_state.responses.append({
                "이름": name,
                "부서": department,
                "파일명": uploaded_file.name,
                "이미지": uploaded_file.read()
            })
            st.session_state.step = 2

elif st.session_state.step == 2:
    response = st.session_state.responses[-1]
    st.image(response["이미지"], caption=response["파일명"])

    with st.form("question_form"):
        q1 = st.text_input("어떤 작업을 하고 있는 건가요?")
        q2 = st.text_input("이 작업은 왜 위험하다고 생각하나요?")
        q3 = st.radio("이 작업은 얼마나 자주 하나요?", ["연 1-2회", "반기 1-2회", "월 2-3회", "주 1회 이상", "매일"])
        q4 = st.radio("이 작업은 얼마나 위험하다고 생각하나요?", [
            "약간의 위험: 일회용 밴드 치료 필요 가능성 있음",
            "조금 위험: 병원 치료 필요. 1-2일 치료 및 휴식",
            "위험: 보름 이상의 휴식이 필요한 중상 가능성 있음",
            "매우 위험: 불가역적 장애 또는 사망 가능성 있음"
        ])
        submitted = st.form_submit_button("저장하기")
        if submitted:
            response.update({
                "질문1": q1,
                "질문2": q2,
                "질문3": q3,
                "질문4": q4,
                "시간": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            st.success("저장 완료! 다음 사진을 입력해 주세요.")
            st.session_state.step = 1