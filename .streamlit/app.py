import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="서울시 공영주차장 안내",
    layout="wide"
)

st.title("🅿 서울시 공영주차장 정보")

st.write("서울시 공영주차장 CSV 파일을 업로드하세요.")

uploaded_file = st.file_uploader(
    "CSV 파일",
    type=["csv"]
)


# -------------------------------
# CSV 읽기
# -------------------------------
def load_csv(file):

    encodings = [
        "utf-8",
        "utf-8-sig",
        "cp949",
        "euc-kr"
    ]

    for enc in encodings:
        try:
            file.seek(0)
            return pd.read_csv(file, encoding=enc)
        except Exception:
            pass

    raise Exception("CSV를 읽을 수 없습니다.")


if uploaded_file:

    try:
        df = load_csv(uploaded_file)

    except Exception as e:
        st.error(e)
        st.stop()

    # 숫자 변환
    df["위도"] = pd.to_numeric(df["위도"], errors="coerce")
    df["경도"] = pd.to_numeric(df["경도"], errors="coerce")

    df = df.dropna(subset=["위도", "경도"])

    st.success(f"총 {len(df)}개의 주차장 정보를 불러왔습니다.")

    st.subheader("🔍 주소 또는 주차장명 검색")

    keyword = st.text_input(
        "주소 또는 주차장명을 입력하세요"
    )

    result = df

    if keyword:

        result = df[
            df["주소"].astype(str).str.contains(keyword, case=False, na=False)
            |
            df["주차장명"].astype(str).str.contains(keyword, case=False, na=False)
        ]

    if len(result) == 0:

        st.warning("검색 결과가 없습니다.")
        st.stop()

    st.subheader("검색 결과")

    st.dataframe(
        result[
            [
                "주차장명",
                "주소",
                "기본 주차 요금",
                "추가 단위 요금",
                "일 최대 요금",
                "총 주차면"
            ]
        ],
        use_container_width=True
    )

    # -----------------------
    # 지도 생성
    # -----------------------

    center_lat = result["위도"].mean()
    center_lon = result["경도"].mean()

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12
    )

    for _, row in result.iterrows():

        popup = f"""
        <b>{row['주차장명']}</b><br><br>

        주소 : {row['주소']}<br>

        기본요금 : {row['기본 주차 요금']}원<br>

        추가요금 : {row['추가 단위 요금']}원<br>

        일 최대요금 : {row['일 최대 요금']}원<br>

        총 주차면 : {row['총 주차면']}면
        """

        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=folium.Popup(popup, max_width=350),
            tooltip=row["주차장명"],
            icon=folium.Icon(
                color="blue",
                icon="info-sign"
            )
        ).add_to(m)

    st.subheader("🗺 공영주차장 지도")

    st_folium(
        m,
        width=1200,
        height=700
    )
