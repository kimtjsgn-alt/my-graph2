import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

# 데이터 불러오기 및 전처리 함수
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르가 세로막대 기호(|)로 묶여 있는 경우 첫 번째 장르만 추출
    df['genre'] = df['genre'].astype(str).apply(lambda x: x.split('|')[0] if '|' in x else x)
    
    return df

data = load_data()

st.markdown("---")

# 첫 번째 그래프 구역: 장르별 영화 편수 (도넛 그래프)
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_counts = data['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '편수']

# Plotly 도넛 그래프 생성
fig1 = px.pie(
    genre_counts, 
    values='편수', 
    names='장르', 
    hole=0.4,
    title="장르별 영화 비율"
)

# 마우스 호버 시 편수와 비율이 함께 표시되도록 설정
fig1.update_traces(
    textposition='inside', 
    textinfo='percent+label',
    hovertemplate="<b>장르: %{label}</b><br>편수: %{value}편<br>비율: %{percent}"
)

st.plotly_chart(fig1, use_container_width=True)

# '이 그래프로 알 수 있는 것' 안내 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 특정 장르에 영화 개봉이 집중되어 있는지, 혹은 다양한 장르가 균등하게 분포해 있는지 한눈에 비교할 수 있습니다.")
