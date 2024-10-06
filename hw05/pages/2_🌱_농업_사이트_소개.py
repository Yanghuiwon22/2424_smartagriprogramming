import streamlit as st
import pandas as pd

# 데이터 목록
data = {
    "제목": ["농촌진흥청",
        "농업교육포털",
        "농사로",
        "흙토람",
        "농업과학도서관",
        "농산물 유통정보",
        " 😊계속 추가될 예정입니다..."
    ],
    "설명": ["농촌진흥청에서 운영하고 있는 농촌진흥청 홈페이지는 농업 관련 최신 정보와 정책, "
           "연구 성과,교육 프로그램 등에 대한 정보를 손쉽게 확인할 수 있습니다."
        ,#2 농업교츅포털
        "농업교육포털은 농림수산식품교육문화정보원에서 운영하고 있는 사이트로 농업에 관한 무료 온라인 교육을 "
        "제공하고 있습니다. "
        ,#3 농사로
        "농촌진흥청에서 운영하고 있는 농사로 사이트는 농업자재, "
        "영농기술, 농업경영, 연구정보, 생활농업, 농사로소식으로 메뉴를 운영하고 있으며 농업기술에 대한"
        " 최신기술과 자료를 제공하고 있습니다."
        ,#4 흙토람
        "농촌진흥청에서 운영하고 있는 흙토람 사이트는 토양정보를 제공하고, 토양에 따라 알맞은 비료량을 추천해주는"
        " 서비스를 제공하고 있습니다."
        ,#5 농업과학도서관
        "농촌진흥청에서 운영하는 농업과학도서관 사이트는 농촌진흥청의 발간자료들이나 "
        "소장자료검색, 전자정보 검색 등 농업인이라면 알아두면 좋을만한 다양한 정보를 제공하고 있습니다. "
        ,#6 농산물 유통정보
        "한국농수산식품유통공사에서 운영하는 농산물 유통정보 사이트는 농축수산물의 소,도매가격 정보와 통계를"
        "제공하고 있으며 농축수산물의 동향과 유통실태,친환경 유통정보 등에 관한 자료를 제공하고 있습니다.  "
        ,# 추가
           ""
    ],
    "링크": ["https://www.rda.go.kr/main/mainPage.do",
           #2
        "https://agriedu.net/",
           #3
        "https://www.nongsaro.go.kr/portal/portalMain.ps?menuId=PS00001",
           #4
        "https://soil.rda.go.kr/soil/index.jsp",
           #5
        "https://lib.rda.go.kr/main.do",
           #6
        "https://www.kamis.or.kr/customer/main/main.do",
           #7 추가
        "Comming Soon..."

    ]
}


df = pd.DataFrame(data)
# 제목
st.title("🌱농업 사이트 소개")
st.header("🔎농업 사이트 목록")

# 데이터 목록 표시
for index, row in df.iterrows():
    st.subheader(row['제목'])
    st.write(row['설명'])
    st.markdown(f"[사이트 가기➡️]({row['링크']})({row['링크']})")
