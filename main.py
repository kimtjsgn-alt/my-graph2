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
    
    # 장르가 세로막대 기호(|)로 묶여 있는 경우 첫 번째 장르만 추출 (.str 메서드로 오류 방지)
    df['genre'] = df['genre'].astype(str).str.split('|').str[0]
    
    return df

data = load_data()

st.markdown("---")

# ---------------------------------------------------------
# 첫 번째 그래프 구역: 장르별 영화 편수 (도넛 그래프)
# ---------------------------------------------------------
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

st.markdown("---")

# ---------------------------------------------------------
# 두 번째 그래프 구역: 장르 및 영화별 총 관객수 (트리맵)
# ---------------------------------------------------------
st.subheader("2. 장르 및 영화별 총 관객수 분포 (트리맵)")

# Plotly 트리맵 생성 (계층 구조: 장르 -> 영화명, 사각형 크기: 총 관객수)
fig2 = px.treemap(
    data,
    path=['genre', 'movieNm'],
    values='total_audi',
    color='genre',
    title="장르 및 영화별 총 관객수 트리맵"
)

# 마우스 호버 툴팁 설정 (영화명/장르명과 총 관객수 표시)
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,}명<extra></extra>"
)

st.plotly_chart(fig2, use_container_width=True)

# '이 그래프로 알 수 있는 것' 안내 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 전체 흥행 관객수에서 특정 장르 및 개별 영화가 차지하는 비중과 규모를 한눈에 파악할 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 세 번째 그래프 구역: 총 관객수 분포 (히스토그램)
# ---------------------------------------------------------
st.subheader("3. 총 관객수 분포 (히스토그램)")

# Plotly 히스토그램 생성
fig3 = px.histogram(
    data, 
    x='total_audi', 
    nbins=30,
    title="영화별 총 관객수 분포 히스토그램",
    labels={'total_audi': '총 관객수(명)'},
    hover_data=['movieNm']
)
fig3.update_layout(yaxis_title="영화 수")

st.plotly_chart(fig3, use_container_width=True)

# 동적 연산: 가장 관객수가 많은 영화 및 관객수 추출
top_movie = data.loc[data['total_audi'].idxmax()]
top_movie_name = top_movie['movieNm']
top_movie_audi = top_movie['total_audi']

# '이 그래프로 알 수 있는 것' 안내 구역 (밀집 구간 및 최다 관객 영화 표기)
st.info(
    f"💡 **이 그래프로 알 수 있는 것:** 대부분의 영화는 총 관객수 100만~200만 명대 이하의 하위 구간에 밀집해 있으며, "
    f"가장 관객 수가 많은 영화는 **'{top_movie_name}'**(총 {top_movie_audi:,}명)입니다."
)

st.markdown("---")

# ---------------------------------------------------------
# 네 번째 그래프 구역: 개봉일 스크린수 vs 총 관객수 (산점도)
# ---------------------------------------------------------
st.subheader("4. 개봉일 스크린수와 총 관객수의 관계 (산점도)")

# Plotly 산점도 생성 (x축: 개봉일 스크린수, y축: 총 관객수, 색상: 장르)
fig4 = px.scatter(
    data,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title="개봉일 스크린수 vs 총 관객수 산점도",
    labels={
        'first_scrn': '개봉일 스크린수(개)',
        'total_audi': '총 관객수(명)',
        'genre': '장르'
    },
    hover_data={
        'first_scrn': ':,d',
        'total_audi': ':,d',
        'genre': True
    }
)

# 호버 템플릿 설정
fig4.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig4, use_container_width=True)

# '이 그래프로 알 수 있는 것' 안내 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 개봉일 스크린수가 많을수록 대체로 총 관객수도 증가하는 양의 상관관계를 보이는지, 장르별로 스크린 확보 및 관객 동원력의 차이가 존재하는지 확인할 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 다섯 번째 그래프 구역: 장르별 총 관객수 상자 그림 (박스플롯)
# ---------------------------------------------------------
st.subheader("5. 주요 장르별 총 관객수 분포 (박스플롯)")

# 영화 수 10편 이상인 장르만 필터링
genre_counts_series = data['genre'].value_counts()
major_genres = genre_counts_series[genre_counts_series >= 10].index
filtered_data = data[data['genre'].isin(major_genres)]

# Plotly 박스플롯 생성
fig5 = px.box(
    filtered_data,
    x='genre',
    y='total_audi',
    color='genre',
    points='outliers',  # 이상치 점 표시
    hover_name='movieNm',  # 호버 시 영화명 표시
    title="주요 장르별(10편 이상) 총 관객수 분포 및 이상치",
    labels={
        'genre': '장르',
        'total_audi': '총 관객수(명)'
    },
    hover_data={'total_audi': ':,d'}
)

# 호버 템플릿 설정 (이상치 및 모든 데이터 포인트 공통 적용)
fig5.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig5, use_container_width=True)

# '이 그래프로 알 수 있는 것' 안내 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 영화가 10편 이상 개봉한 주요 장르별 총 관객수의 중간값과 흥행 편차를 비교할 수 있으며, 일반적인 장르 평균을 뛰어넘어 엑스트라 히트를 기록한 이상치 영화들을 확인할 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 여섯 번째 그래프 구역: 개봉 첫 주 관객수 크기가 반영된 버블 차트
# ---------------------------------------------------------
st.subheader("6. 개봉일 스크린수, 총 관객수 및 첫 주 관객수의 관계 (버블 차트)")

# Plotly 버블 차트 생성 (x: 개봉일 스크린수, y: 총 관객수, size: 개봉 첫 주 관객수)
fig6 = px.scatter(
    data,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi',
    color='genre',
    hover_name='movieNm',
    title="개봉일 스크린수 vs 총 관객수 (원의 크기 = 개봉 첫 주 관객수)",
    labels={
        'first_scrn': '개봉일 스크린수(개)',
        'total_audi': '총 관객수(명)',
        'first_week_audi': '개봉 첫 주 관객수(명)',
        'genre': '장르'
    },
    hover_data={
        'first_scrn': ':,d',
        'total_audi': ':,d',
        'first_week_audi': ':,d',
        'genre': True
    },
    size_max=40  # 버블 최대 크기 지정
)

# 호버 템플릿 설정
fig6.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig6, use_container_width=True)

# '이 그래프로 알 수 있는 것' 안내 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 개봉일 스크린수(X축)와 총 관객수(Y축)의 관계 외에도 개봉 첫 주 관객수(원의 크기)를 동시에 비교하여, 초반 흥행 기세가 최종 관객수로 이어지는 양상을 다차원적으로 파악할 수 있습니다.")

st.markdown("---")

# ---------------------------------------------------------
# 일곱 번째 그래프 구역: 제작 국가별-장르별 영화 편수 (선버스트 차트)
# ---------------------------------------------------------
st.subheader("7. 제작 국가 및 장르별 영화 편수 분포 (선버스트)")

# 계층 구조 생성: nation -> genre
fig7 = px.sunburst(
    data,
    path=['nation', 'genre'],
    title="제작 국가 및 장르별 영화 편수 선버스트 차트"
)

# 호버 및 텍스트 설정 (편수와 비율 표시)
fig7.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<br>비율: %{percentParent:.1%}<extra></extra>"
)

st.plotly_chart(fig7, use_container_width=True)

# '이 그래프로 알 수 있는 것' 안내 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 제작 국가별 영화 점유율과 각 국가 내부에서 주로 제작·개봉된 장르 구성 비율을 원형 계층 구조로 한눈에 파악할 수 있습니다.")
