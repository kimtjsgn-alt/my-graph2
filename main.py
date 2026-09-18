import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 스트림릿 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # genre: '|' 기호로 여러 개 적힌 경우 첫 번째 장르만 추출
    if 'genre' in df.columns:
        df['genre'] = df['genre'].astype(str).apply(
            lambda x: x.split('|')[0].strip() if x != 'nan' and x != '' else '기타'
        )
    
    # 숫자형 데이터 타입 변환 및 결측치 처리
    num_cols = ['first_scrn', 'first_show', 'first_week_audi', 'total_audi', 'days_in_top10']
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 대시보드 제목 및 기본 안내
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown("KOBIS 박스오피스 데이터를 바탕으로 **장르 분포**, **총 관객 수 구성**, **관객 수 분포 패턴**, 그리고 **변수 간의 관계**를 다각도로 분석합니다.")

st.divider()

# 사이드바 필터링 기능
st.sidebar.header("🔍 데이터 필터링")
all_genres = sorted(df['genre'].unique())
selected_genres = st.sidebar.multiselect(
    "장르 선택",
    options=all_genres,
    default=all_genres
)

# 필터링 적용
filtered_df = df[df['genre'].isin(selected_genres)].copy()

st.sidebar.markdown("---")
st.sidebar.metric(label="📊 분석 대상 영화 수", value=f"{len(filtered_df)} 편")

st.subheader("1. 장르별 영화 편수 분포 (도넛 그래프)")

genre_counts = filtered_df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

fig_donut = go.Figure(data=[go.Pie(
    labels=genre_counts['genre'],
    values=genre_counts['count'],
    hole=0.4,
    textinfo='percent+label',
    hovertemplate="<b>장르: %{label}</b><br>영화 수: %{value}편<br>비율: %{percent}<extra></extra>",
    marker=dict(colors=px.colors.qualitative.Pastel)
)])

fig_donut.update_layout(
    margin=dict(t=30, b=20, l=20, r=20),
    showlegend=True
)

st.plotly_chart(fig_donut, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 주요 장르별 영화 개봉 비율을 비교하여 박스오피스 상위권에 가장 자주 진입하는 주류 장르가 무엇인지 직관적으로 확인할 수 있습니다.")

st.divider()

st.subheader("2. 장르 및 영화별 총 관객 수 (트리맵)")

fig_treemap = px.treemap(
    filtered_df,
    path=[px.Constant("전체 영화"), 'genre', 'movieNm'],
    values='total_audi',
    color='genre',
    color_discrete_sequence=px.colors.qualitative.Set3,
    title=None
)

fig_treemap.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,.0f}명<extra></extra>"
)

fig_treemap.update_layout(
    margin=dict(t=30, b=20, l=20, r=20)
)

st.plotly_chart(fig_treemap, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 타일의 면적을 통해 특정 장르 내에서 어떤 영화가 가장 많은 관객을 동원하며 장르 전체 실적을 견인했는지 한눈에 파악할 수 있습니다.")

st.divider()

st.subheader("3. 총 관객 수 분포 (히스토그램)")

fig_hist = px.histogram(
    filtered_df,
    x="total_audi",
    nbins=30,
    color_discrete_sequence=['#4B6BFB'],
    labels={'total_audi': '총 관객 수 (명)'},
    title=None
)

fig_hist.update_traces(
    hovertemplate="<b>관객 수 구간: %{x}</b><br>영화 수: %{y}편<extra></extra>"
)

fig_hist.update_layout(
    xaxis_title="총 관객 수 (명)",
    yaxis_title="영화 편수",
    margin=dict(t=30, b=20, l=20, r=20)
)

st.plotly_chart(fig_hist, use_container_width=True)

# 히스토그램 상세 통계 문구 계산
if not filtered_df.empty:
    top_movie = filtered_df.loc[filtered_df['total_audi'].idxmax()]
    top_movie_name = top_movie['movieNm']
    top_movie_audi = int(top_movie['total_audi'])
    
    under_2m_count = len(filtered_df[filtered_df['total_audi'] <= 2000000])
    under_2m_ratio = (under_2m_count / len(filtered_df)) * 100
    
    st.markdown(f"""
    📌 **관객 수 분포 통계 요약:**
    - 대다수의 영화(**{under_2m_count}편, 약 {under_2m_ratio:.1f}%**)가 **총 관객 수 200만 명 이하 구간**에 밀집되어 있습니다.
    - 현재 선택된 데이터 중 가장 많은 관객을 동원한 영화는 **'{top_movie_name}'** (총 **{top_movie_audi:,.0f}명**)입니다.
    """)
else:
    st.warning("선택된 장르에 해당되는 데이터가 없습니다.")

st.info("💡 **이 그래프로 알 수 있는 것:** 영화 흥행 실적의 치우침 현상(L-자형 비대칭 구조)을 보여주며, 소수의 대형 흥행작을 제외하면 대부분의 영화가 특정 중소 관객 수 구간에 집중되어 있음을 알 수 있습니다.")

st.divider()

st.subheader("4. 개봉일 스크린수와 총 관객수의 관계 (산점도)")

fig_scatter = px.scatter(
    filtered_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    hover_data={
        "first_scrn": ":,.0f",
        "total_audi": ":,.0f",
        "genre": True
    },
    labels={
        "first_scrn": "개봉일 스크린 수 (개)",
        "total_audi": "총 관객 수 (명)",
        "genre": "장르"
    },
    title=None
)

fig_scatter.update_traces(
    marker=dict(size=10, opacity=0.8),
    hovertemplate="<b>%{hovertext}</b><br>장르: %{customdata[0]}<br>개봉일 스크린수: %{x:,.0f}개<br>총 관객수: %{y:,.0f}명<extra></extra>"
)

fig_scatter.update_layout(
    xaxis_title="개봉일 스크린 수 (개)",
    yaxis_title="총 관객 수 (명)",
    margin=dict(t=30, b=20, l=20, r=20),
    legend_title_text="장르"
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 개봉 초기에 얼마나 많은 스크린 수를 확보했는지가 최종 총 관객 수와 어떠한 양의 상관관계를 형성하는지 파악할 수 있습니다.")

st.divider()

st.subheader("5. 영화 10편 이상 주요 장르별 총 관객 수 (박스플롯)")

# 영화 수 10편 이상인 장르만 필터링
genre_counts_series = filtered_df['genre'].value_counts()
major_genres = genre_counts_series[genre_counts_series >= 10].index.tolist()

if major_genres:
    boxplot_df = filtered_df[filtered_df['genre'].isin(major_genres)].copy()

    fig_box = px.box(
        boxplot_df,
        x="genre",
        y="total_audi",
        color="genre",
        points="outliers",
        hover_name="movieNm",
        hover_data={
            "total_audi": ":,.0f",
            "genre": True
        },
        labels={
            "genre": "장르",
            "total_audi": "총 관객 수 (명)"
        },
        title=None
    )

    fig_box.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>장르: %{customdata[0]}<br>총 관객수: %{y:,.0f}명<extra></extra>"
    )

    fig_box.update_layout(
        xaxis_title="주요 장르 (10편 이상)",
        yaxis_title="총 관객 수 (명)",
        margin=dict(t=30, b=20, l=20, r=20),
        showlegend=False
    )

    st.plotly_chart(fig_box, use_container_width=True)
    
    st.info("💡 **이 그래프로 알 수 있는 것:** 주요 장르별 관객 수의 중간값과 분포 범위(변동성)를 비교할 수 있으며, 박스 밖의 이상치(Outlier) 점을 통해 장르 내에서 독보적인 대박 흥행을 기록한 영화를 쉽게 식별할 수 있습니다.")
else:
    st.warning("선택한 필터 조건 내에 영화 수 10편 이상인 장르가 존재하지 않습니다.")

st.divider()

st.subheader("6. 스크린수, 첫 주 관객, 총 관객수의 관계 (버블 그래프)")

fig_bubble = px.scatter(
    filtered_df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=50,
    hover_data={
        "first_scrn": ":,.0f",
        "first_week_audi": ":,.0f",
        "total_audi": ":,.0f",
        "genre": True
    },
    labels={
        "first_scrn": "개봉일 스크린 수 (개)",
        "total_audi": "총 관객 수 (명)",
        "first_week_audi": "첫 주 관객 수 (명)",
        "genre": "장르"
    },
    title=None
)

fig_bubble.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "장르: %{customdata[0]}<br>"
        "개봉일 스크린수: %{x:,.0f}개<br>"
        "첫 주 관객수: %{marker.size:,.0f}명<br>"
        "총 관객수: %{y:,.0f}명<extra></extra>"
    )
)

fig_bubble.update_layout(
    xaxis_title="개봉일 스크린 수 (개)",
    yaxis_title="총 관객 수 (명)",
    margin=dict(t=30, b=20, l=20, r=20),
    legend_title_text="장르"
)

st.plotly_chart(fig_bubble, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 개봉일 스크린 수(X축)와 총 관객 수(Y축)에 더해 '첫 주 관객 수'(버블 크기)를 다차원적으로 비교하여, 초반 입소문으로 장기 흥행에 성공한 영화와 초반 세에 비해 뒷심이 부족했던 영화를 종합적으로 파악할 수 있습니다.")

st.divider()

with st.expander("📄 Raw Data 요약표 보기"):
    st.dataframe(
        filtered_df[['movieCd', 'movieNm', 'openDt', 'genre', 'nation', 'first_scrn', 'first_show', 'first_week_audi', 'total_audi', 'days_in_top10']],
        use_container_width=True
    )
