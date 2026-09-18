import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # genre(장르) 열 전처리: 세로막대 기호(|) 기준 첫 번째 장르만 추출 및 결측치 처리
    df['genre'] = df['genre'].fillna('기타').astype(str).apply(lambda x: x.split('|')[0].strip())
    df['genre'] = df['genre'].replace({'': '기타', 'nan': '기타'})
    
    # nation(제작 국가) 결측치 및 빈 문자열 처리
    df['nation'] = df['nation'].fillna('기타').astype(str).apply(lambda x: x.strip())
    df['nation'] = df['nation'].replace({'': '기타', 'nan': '기타'})
    
    return df

df = load_data()

# -------------------------------------------------------------------
# 그래프 1: 장르별 영화 편수 (도넛 차트)
# -------------------------------------------------------------------
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '영화 편수']

# Plotly 도넛 차트 생성
fig1 = px.pie(
    genre_counts,
    names='장르',
    values='영화 편수',
    hole=0.4,
    title="장르별 영화 편수 비중"
)

# 마우스 호버 시 편수와 비율(퍼센트) 표시
fig1.update_traces(
    hovertemplate="<b>장르: %{label}</b><br>영화 편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

st.plotly_chart(fig1, use_container_width=True)

# 구분선 및 알 수 있는 점 작성 구역
st.divider()
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("박스오피스 상위권 영화 중 특정 장르가 차지하는 비율과 가장 많이 제작/개봉된 주요 장르 분포를 한눈에 파악할 수 있습니다.")


# -------------------------------------------------------------------
# 그래프 2: 장르 및 영화별 총 관객 수 (트리맵)
# -------------------------------------------------------------------
st.write("---")
st.subheader("2. 장르 및 영화별 총 관객 수")

# Plotly 트리맵 생성 (계층: 장르 > 영화명, 크기: 총 관객 수)
fig2 = px.treemap(
    df,
    path=[px.Constant("전체 장르"), 'genre', 'movieNm'],
    values='total_audi',
    title="장르 및 영화별 총 관객 수 분포"
)

# 마우스 호버 시 영화명과 총 관객 수 표시
fig2.update_traces(
    hovertemplate="<b>영화명: %{label}</b><br>총 관객 수: %{value:,.0f}명<extra></extra>"
)

st.plotly_chart(fig2, use_container_width=True)

# 구분선 및 알 수 있는 점 작성 구역
st.divider()
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("각 장르 내에서 어떤 영화가 전체 관객 수 증가를 견인했는지, 장르별 흥행 규모와 대표 흥행작을 직관적으로 비교할 수 있습니다.")


# -------------------------------------------------------------------
# 그래프 3: 총 관객 수 분포 (히스토그램)
# -------------------------------------------------------------------
st.write("---")
st.subheader("3. 총 관객 수 분포 (히스토그램)")

# Plotly 히스토그램 생성
fig3 = px.histogram(
    df,
    x='total_audi',
    nbins=30,
    title="영화별 총 관객 수 분포 구간",
    labels={'total_audi': '총 관객 수(명)', 'count': '영화 수'}
)

fig3.update_traces(
    hovertemplate="<b>관객 수 구간: %{x}명</b><br>영화 수: %{y}편<extra></extra>"
)

st.plotly_chart(fig3, use_container_width=True)

# 최고 관객 수 영화 정보 자동 추출
top_movie = df.loc[df['total_audi'].idxmax()]
top_movie_name = top_movie['movieNm']
top_movie_audi = top_movie['total_audi']

# 구분선 및 알 수 있는 점 작성 구역
st.divider()
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info(
        f"대부분의 영화는 **상대적으로 관객 수가 적은 하위~중위 구간**에 집중적으로 몰려 있는 오른쪽 꼬리가 긴 형태를 보입니다. "
        f"반면 가장 많은 관객을 동원한 최고 흥행작은 **'{top_movie_name}'**(총 {top_movie_audi:,.0f}명)으로 극소수의 메가 히트작이 전체 관객 수의 상단을 형성하고 있음을 알 수 있습니다."
    )


# -------------------------------------------------------------------
# 그래프 4: 개봉일 스크린수와 총 관객 수의 관계 (산점도)
# -------------------------------------------------------------------
st.write("---")
st.subheader("4. 개봉일 스크린수와 총 관객 수의 관계")

# Plotly 산점도 생성
fig4 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title="개봉일 스크린수 vs 총 관객 수",
    labels={
        'first_scrn': '개봉일 스크린수(개)',
        'total_audi': '총 관객 수(명)',
        'genre': '장르'
    }
)

# 마우스 호버 시 영화명, 개봉일 스크린수, 총 관객 수 표시
fig4.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명<extra></extra>"
)

st.plotly_chart(fig4, use_container_width=True)

# 구분선 및 알 수 있는 점 작성 구역
st.divider()
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("개봉일 스크린수가 많을수록 대체로 총 관객 수도 증가하는 양(+)의 상관관계를 보이며, 장르에 따라 초기 스크린 확보 수준과 최종 흥행 규모의 차이를 함께 확인할 수 있습니다.")


# -------------------------------------------------------------------
# 그래프 5: 주요 장르별 총 관객 수 분포 (박스플롯)
# -------------------------------------------------------------------
st.write("---")
st.subheader("5. 주요 장르별 총 관객 수 분포 (박스플롯)")

# 영화가 10편 이상인 장르만 필터링
genre_counts_series = df['genre'].value_counts()
valid_genres = genre_counts_series[genre_counts_series >= 10].index
df_filtered = df[df['genre'].isin(valid_genres)]

# Plotly 박스플롯 생성
fig5 = px.box(
    df_filtered,
    x='genre',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    points="outliers",
    title="영화 10편 이상 주요 장르별 총 관객 수 분포",
    labels={
        'genre': '장르',
        'total_audi': '총 관객 수(명)'
    }
)

# 상자 밖으로 튀는 점(이상치) 호버 시 영화명과 총 관객 수 표시
fig5.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객 수: %{y:,.0f}명<extra></extra>"
)

st.plotly_chart(fig5, use_container_width=True)

# 구분선 및 알 수 있는 점 작성 구역
st.divider()
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("장르별 평균적인 관객 분포와 변동 폭을 비교할 수 있으며, 박스 상단 밖으로 튀어 나온 점들을 통해 장르 평균을 뛰어넘는 메가 히트 이상치(Outlier) 영화들을 확인할 수 있습니다.")


# -------------------------------------------------------------------
# 그래프 6: 개봉일 스크린수, 총 관객 수, 첫 주 관객 수 (버블 차트)
# -------------------------------------------------------------------
st.write("---")
st.subheader("6. 개봉일 스크린수 · 총 관객 수 · 첫 주 관객 수의 종합 관계 (버블 차트)")

# Plotly 버블 차트 생성 (size = first_week_audi)
fig6 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi',
    color='genre',
    hover_name='movieNm',
    size_max=50,
    title="개봉일 스크린수 vs 총 관객 수 (원 크기: 첫 주 관객 수)",
    labels={
        'first_scrn': '개봉일 스크린수(개)',
        'total_audi': '총 관객 수(명)',
        'first_week_audi': '첫 주 관객 수(명)',
        'genre': '장르'
    },
    custom_data=['first_week_audi']
)

# 마우스 호버 시 영화명, 개봉일 스크린수, 총 관객 수, 첫 주 관객 수 표시
fig6.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명<br>첫 주 관객 수: %{customdata[0]:,.0f}명<extra></extra>"
)

st.plotly_chart(fig6, use_container_width=True)

# 구분선 및 알 수 있는 점 작성 구역
st.divider()
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("개봉 첫 주 관객 수가 많을수록(버블 크기가 클수록) 최종 총 관객 수와 초기 스크린 확보 수가 모두 높은 편임을 보여주어, 초반 흥행 기세가 최종 성과에 미치는 영향력을 3차원적(X-Y-크기)으로 비교할 수 있습니다.")


# -------------------------------------------------------------------
# 그래프 7: 제작 국가 및 장르별 영화 편수 (선버스트)
# -------------------------------------------------------------------
st.write("---")
st.subheader("7. 제작 국가 및 장르별 영화 편수 (선버스트)")

# 제작 국가 및 장르별 영화 편수 집계
sunburst_df = df.groupby(['nation', 'genre']).size().reset_index(name='count')

# 선버스트 차트 생성
fig7 = px.sunburst(
    sunburst_df,
    path=['nation', 'genre'],
    values='count',
    title="제작 국가별 장르 구성 (칸 크기: 영화 편수)"
)

# 마우스 호버 시 구획명, 영화 편수, 비율 표시
fig7.update_traces(
    hovertemplate="<b>구분: %{label}</b><br>영화 편수: %{value}편<br>비율: %{percentParent:.1%} (상위 항목 대비)<extra></extra>"
)

st.plotly_chart(fig7, use_container_width=True)

# 구분선 및 알 수 있는 점 작성 구역
st.divider()
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("국가별로 주로 제작/수입되는 영화 장르의 다변화 수준과 비중을 중앙에서 외곽으로 확장되는 동심원 계층 구조를 통해 한눈에 비교할 수 있습니다.")


# -------------------------------------------------------------------
# 그래프 8: 장르별 총 관객 수 산점도
# -------------------------------------------------------------------
st.write("---")
question_title = "어떤 장르가 총 관객 수가 많은지 알려줘"
st.subheader(f"8. {question_title}")

# Plotly 산점도 생성 (가로축: 장르, 세로축: 총 관객)
fig8 = px.scatter(
    df,
    x='genre',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title=question_title,
    labels={
        'genre': '장르',
        'total_audi': '총 관객 수(명)'
    }
)

# 마우스 호버 시 영화명과 총 관객 수 표시
fig8.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객 수: %{y:,.0f}명<extra></extra>"
)

st.plotly_chart(fig8, use_container_width=True)

# 구분선 및 알 수 있는 점 작성 구역
st.divider()
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info("각 장르별 개별 영화들의 관객 수 개별 위치와 분포 높이를 직관적으로 확인할 수 있어, 어떤 장르에 대형 흥행작이 많이 위치해 있는지 한눈에 비교할 수 있습니다.")
