import streamlit as st
import pandas as pd
import os
from datetime import datetime


#1 페이지 설정
st.set_page_config(page_title="간단 설문조사", page_icon="❤️", layout="centered")
st.title("❤️ 우리 동네 거리 설문조사")
st.write("""이 설문은 **우리 동네 거리(street)에 대해 여러분의 생각을 모으기 위한 것입니다.**""")

#2 설문 항목
with st.form("survey_form") :
    name = st.text_input("이름을 입력하세요")
    street = st.selectbox("가장 좋아하는 우리 동네 거리 이름을 선택하세요", ["상남대로", "중앙대로", "팔용산길", "반송로", "불종거리", "그 외"])
    cleanliness = st.slider("해당 거리를 얼마나 꺠끗하다고 느끼나요 (1. 매우 불만족 ~ 5 매우 만족)", min_value=1, max_value=5, value=3)
    safety = st.radio("해당 거리를 얼마나 안전하다고 느끼나요?", options=[1, 2, 3, 4, 5], index=2,format_func=lambda x: f"{x}점")
    comments = st.text_area("추가로 하고 싶은 말이 있으면 적어주세요 (선택사항)")
    submitted = st.form_submit_button("제출하기")

#3 응답 저장
DATA_PATH = "data/responses.csv"
os.makedirs("data", exist_ok=True)

if submitted :
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = {"timestamp": now, "name": name, "street": street, "cleanliness": cleanliness, "safety": safety, "comments": comments}


#CSV 파일이 없으면 헤더 포함 생성, 있으면 append

    if not os.path.isfile(DATA_PATH) :
        df = pd.DataFrame([new_row])
        df.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")
    else : 
        df = pd.read_csv(DATA_PATH)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")
    st.success("설문이 제출되었습니다! 감사합니다❤️")

#4 요약 리포트 보기
st.header("요약 리포트")
if os.path.isfile(DATA_PATH) :
    df = pd.read_csv(DATA_PATH)

#4-1 전체 응답 수
    total = len(df)
    st.write(f" - 전체 응답 수 : **{total}명**")

#4-2 거리별 응답 분포
    street_counts = df["street"].value_counts()
    st.subheader("1)거리별 응답 분포")
    st.bar_chart(street_counts)

#4-3 평균 점수
    avg_clean = df["cleanliness"].mean()
    avg_safe = df["safety"].mean()
    st.subheader("2) 평균 점수")
    st.write(f"깨끗함 평균 : **{avg_clean:.2f}**점")
    st.write(f" 안전함 평균 : **{avg_safe:.2f}점**")

#4-4 원한다면 원본 데이터도 보기
    with st.expander("원본 응답 데이터 보기") :
        st.dataframe(df)    
else :
    st.info("아직 제출된 설문이 없습니다.")
