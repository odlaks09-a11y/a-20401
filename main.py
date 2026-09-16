import pandas as pd
import plotly.express as px
import streamlit as st


# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르가 세로막대 기호(|)로 나뉘어 있으면 첫 번째 장르만 추출
    df["genre"] = df["genre"].astype(str).apply(lambda x: x.split("|")[0])

    return df


df = load_data()

# 앱 제목 설정
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

# ----------------------------------------------------
# 1. 장르별 영화 편수 (도넛 그래프)
# ----------------------------------------------------
st.subheader("1. 장르별 영화 편수")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig1 = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.4,
    title="장르별 영화 비율",
)

fig1.update_traces(
    textinfo="percent+label",
    hovertemplate="장르: %{label}<br>편수: %{value}편<br>비율: %{percent}",
)

st.plotly_chart(fig1, use_container_width=True, key="chart_fig1_pie")

st.markdown("---")
st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.caption(
    "어떤 장르의 영화가 시장에서 가장 큰 비중을 차지하고 있는지 한눈에 비교할 수 있습니다."
)
st.markdown("---")

# ----------------------------------------------------
# 2. 장르별 영화 총 관객 수 트리맵
# ----------------------------------------------------
st.subheader("2. 장르 및 영화별 총 관객 수 분포")

fig2 = px.treemap(
    df,
    path=[px.Constant("전체 장르"), "genre", "movieNm"],
    values="total_audi",
    color="genre",
    title="장르 및 영화별 총 관객 수 (칸 크기 = 총 관객 수)",
    hover_data={"total_audi": ":,f"},
)

fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,.0f}명"
)

st.plotly_chart(fig2, use_container_width=True, key="chart_fig2_treemap")

st.markdown("---")
st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.caption(
    "특정 장르 내에서 어떤 영화가 흥행을 주도했는지, 장르 전체 대비 개별 영화의 관객 점유 규모를 한눈에 볼 수 있습니다."
)
st.markdown("---")

# ----------------------------------------------------
# 3. 총 관객 수 히스토그램
# ----------------------------------------------------
st.subheader("3. 총 관객 수 분포 (히스토그램)")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 수 분포",
    labels={"total_audi": "총 관객 수", "count": "영화 수"},
)

fig3.update_traces(
    hovertemplate="총 관객 수 구간: %{x}<br>영화 수: %{y}편"
)

st.plotly_chart(fig3, use_container_width=True, key="chart_fig3_histogram")

# 가장 많은 관객을 동원한 영화 자동 추출
top_movie = df.loc[df["total_audi"].idxmax()]
top_movie_name = top_movie["movieNm"]
top_movie_audi = top_movie["total_audi"]

st.markdown("---")
st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.caption(
    f"대부분의 영화가 관객 수 200만 명 이하의 초반 구간에 집중되어 있으며, 가장 많은 관객을 기록한 영화는 **'{top_movie_name}'**({top_movie_audi:,.0f}명)입니다."
)
st.markdown("---")

# ----------------------------------------------------
# 4. 개봉일 스크린 수와 총 관객 수의 관계 (산점도)
# ----------------------------------------------------
st.subheader("4. 개봉일 스크린 수와 총 관객 수의 관계")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린 수(first_scrn) vs 총 관객 수(total_audi)",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "genre": "장르",
    },
    hover_data={
        "first_scrn": ":,f",
        "total_audi": ":,f",
        "genre": True,
    },
)

fig4.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>장르: %{customdata[0]}<br>개봉일 스크린 수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명"
)

st.plotly_chart(fig4, use_container_width=True, key="chart_fig4_scatter")

st.markdown("---")
st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.caption(
    "개봉일 스크린 수가 많을수록 대체로 총 관객 수가 증가하는 양의 상관관계를 보이지만, 스크린 수가 적음에도 높은 흥행 성적을 거둔 예외적인 산점도 분포도 함께 확인할 수 있습니다."
)
st.markdown("---")

# ----------------------------------------------------
# 5. 주요 장르별 총 관객 수 상자 그림 (박스플롯)
# ----------------------------------------------------
st.subheader("5. 주요 장르별 총 관객 수 분포 (박스플롯)")

genre_counts_series = df["genre"].value_counts()
top_genres = genre_counts_series[genre_counts_series >= 10].index
df_top_genres = df[df["genre"].isin(top_genres)]

fig5 = px.box(
    df_top_genres,
    x="genre",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    points="all",
    title="10편 이상 개봉 장르별 총 관객 수 분포",
    labels={
        "genre": "장르",
        "total_audi": "총 관객 수",
    },
)

fig5.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>장르: %{x}<br>총 관객 수: %{y:,.0f}명"
)

st.plotly_chart(fig5, use_container_width=True, key="chart_fig5_box")

st.markdown("---")
st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.caption(
    "주요 장르별 관객 수의 중간값과 분포 범위를 비교할 수 있으며, 박스 상단 밖으로 길게 이어진 이상치(점)를 통해 장르 내 초대박 흥행작의 존재를 확인할 수 있습니다."
)
st.markdown("---")

# ----------------------------------------------------
# 6. 개봉일 스크린 수, 총 관객 수, 개봉 첫 주 관객 수의 관계 (버블 차트)
# ----------------------------------------------------
st.subheader("6. 개봉일 스크린 수 vs 총 관객 수 (원 크기 = 첫 주 관객 수)")

fig6 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=40,
    title="개봉일 스크린 수 vs 총 관객 수 (버블 크기: 개봉 첫 주 관객 수)",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "first_week_audi": "첫 주 관객 수",
        "genre": "장르",
    },
    hover_data={
        "first_scrn": ":,f",
        "total_audi": ":,f",
        "first_week_audi": ":,f",
        "genre": True,
    },
)

fig6.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>장르: %{customdata[0]}<br>개봉일 스크린 수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명<br>첫 주 관객 수: %{customdata[2]:,.0f}명"
)

st.plotly_chart(fig6, use_container_width=True, key="chart_fig6_bubble")

st.markdown("---")
st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.caption(
    "개봉일 스크린 수와 총 관객 수의 관계에 더해 원의 크기로 개봉 첫 주 흥행 파급력을 동시에 비교할 수 있으며, 초기 흥행(첫 주 관객)이 최종 성적으로 이어지는 양상을 한눈에 파악할 수 있습니다."
)
st.markdown("---")

# ----------------------------------------------------
# 7. 제작 국가 및 장르별 영화 편수 (선버스트 차트)
# ----------------------------------------------------
st.subheader("7. 제작 국가 및 장르별 영화 편수 (선버스트)")

fig7 = px.sunburst(
    df,
    path=["nation", "genre"],
    title="제작 국가 및 장르별 영화 편수 구조",
)

fig7.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<br>상위 대비 비율: %{percentParent:.1%}<br>전체 대비 비율: %{percentRoot:.1%}"
)

st.plotly_chart(fig7, use_container_width=True, key="chart_fig7_sunburst")

st.markdown("---")
st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.caption(
    "각 제작 국가별로 어떤 장르의 영화가 주로 수입·제작되어 개봉했는지 국가와 장르 간의 계층적 비중 구성을 한눈에 파악할 수 있습니다."
)
st.markdown("---")

# ----------------------------------------------------
# 8. 재개봉 영화 TOP 3 및 관객 수 (막대 그래프)
# ----------------------------------------------------
st.subheader("8. 주요 재개봉 영화 및 관객 수 TOP 3")

# openDt(개봉일, YYYYMMDD 형태)에서 연도(YYYY) 추출
df["openYear"] = df["openDt"].astype(str).str[:4].astype(int)

# 개봉 연도가 최근 수집 기간(예: 2018년 이전)보다 오래된 영화를 재개봉작으로 정의
# (데이터셋 내 대다수 영화의 개봉년도 대비 과거 연도 기준 필터링)
rerelease_df = df[df["openYear"] < 2018].sort_values(
    by="total_audi", ascending=False
)

# 상위 3개 재개봉 영화 추출
top3_rerelease = rerelease_df.head(3)

fig8 = px.bar(
    top3_rerelease,
    x="movieNm",
    y="total_audi",
    color="genre",
    text="total_audi",
    title="재개봉 영화 중 총 관객 수 TOP 3",
    labels={
        "movieNm": "영화명",
        "total_audi": "총 관객 수",
        "genre": "장르",
    },
)

fig8.update_traces(
    texttemplate="%{text:,.0f}명",
    textposition="outside",
    hovertemplate="<b>%{x}</b><br>개봉일: %{customdata}<br>총 관객 수: %{y:,.0f}명",
    customdata=top3_rerelease["openDt"],
)

st.plotly_chart(fig8, use_container_width=True, key="chart_fig8_rerelease")

# 상위 3개 재개봉 영화 이름과 관객 수 출력
top3_list = [
    f"**'{row['movieNm']}'**({row['total_audi']:,.0f}명, 개봉일: {row['openDt']})"
    for _, row in top3_rerelease.iterrows()
]
top3_str = ", ".join(top3_list)

st.markdown("---")
st.markdown("**💡 이 그래프로 알 수 있는 것**")
st.caption(
    f"과거 개봉 후 해당 기간에 재개봉하여 박스오피스 상위권에 진입한 영화 중, 가장 관객 수가 많은 상위 3개 영화는 {top3_str}입니다."
)
st.markdown("---")
