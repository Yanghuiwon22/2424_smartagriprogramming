import matplotlib
import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import seaborn as sns

# 교육 자료 샘플 데이터 생성
data = {
    "제목": ["농촌진흥청",
        "농업교육포털",
        "농사로",
        "흙토람",
        "친환경 농업 기법",
        "토양 관리와 비료 사용"
    ],
    "설명": ["농촌진흥청이지",
        "농업 교육포털잉ㅁ다",
        "농사로",
        "흙토람",
        "친환경 농업의 필요성과 기법에 대해 설명합니다.",
        "토양 관리의 중요성과 비료 사용법에 대한 자료입니다."
    ],
    "링크": ["https://www.rda.go.kr/main/mainPage.do",
        "https://agriedu.net/",
        "https://www.nongsaro.go.kr/portal/portalMain.ps?menuId=PS00001",
        "https://soil.rda.go.kr/soil/index.jsp",
        "https://example.com/eco-farming",
        "https://example.com/soil-management"
    ]
}


df = pd.DataFrame(data)
# 앱 제목
st.title("🌱농업 사이트 소개 앱")
# 검색 기능
st.header("🔎농업 사이트 목록")

# 자료 목록 표시
for index, row in df.iterrows():
    st.subheader(row['제목'])
    st.write(row['설명'])
    st.markdown(f"[사이트 가기➡️]({row['링크']})({row['링크']})")
