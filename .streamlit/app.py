import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="공영주차장 안내", layout="wide")

st.title("🅿 공영주차장 정보 안내")

uploaded_file = st.file_uploader(
    "공영주차장 CSV 업로드",
    type=["csv"]
)

# CSV 읽기
def load_csv(file):
    encodings = ["utf-8", "utf-8-sig", "cp949", "euc-kr"]

    for enc in encodings:
        try:
            file.seek(0)
            return pd.read_csv(file, encoding=enc)
        except:
            continue

    raise Exception("CSV 파일을 읽을 수 없습니다.")

if uploaded_file:

    try:
        df = load_csv(uploaded_file)

    except Exception as e:
        st.error(e)
        st.stop()

    st.success("파일 업로드 완료!")

    # 숫자형 변환
    df["위도"] = pd.to_numeric(df["위도"], errors="coerce")
    df["경도"] = pd.to_numeric(df["경도"], errors="coerce")

    df = df.dropna(subset=["위도", "경도"])

    st.subheader("주소 또는 주차장 검색")

    keyword = st.text_input("주소 또는 주차장명을 입력하세요")

    result = df

    if keyword:
        result = df[
            df["주소"].astype(str).str.contains(keyword, case=False, na=False)
            |
            df["주차장명"].astype(str).str.contains(keyword, case=False, na=False)
        ]

    if len(result) == 0:
        st.warning("검색 결과가 없습니다.")

    else:

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
            ]
        )

    st.subheader("주차장 지도")

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=result,
        get_position="[경도, 위도]",
        get_fill_color=[0, 120, 255, 180],
        get_radius=60,
        pickable=True
    )

    view = pdk.ViewState(
        latitude=result["위도"].mean(),
        longitude=result["경도"].mean(),
        zoom=12
    )

    tooltip = {
        "html": """
<b>{주차장명}</b><br>

주소 : {주소}<br>

기본요금 : {기본 주차 요금}원<br>

추가요금 : {추가 단위 요금}원<br>

일 최대요금 : {일 최대 요금}원<br>

주차면수 : {총 주차면}면
""",
        "style": {
            "backgroundColor": "#1565C0",
            "color": "white"
        }
    }

    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view,
            tooltip=tooltip
        )
    )
