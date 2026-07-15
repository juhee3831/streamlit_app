import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="공영주차장 안내", layout="wide")

st.title("🅿 공영주차장 정보 서비스")

uploaded_file = st.file_uploader(
    "CSV 또는 Excel 파일 업로드",
    type=["csv", "xlsx"]
)

# ----------------------------
# 파일 읽기
# ----------------------------
def load_file(file):

    if file.name.endswith(".xlsx"):
        return pd.read_excel(file)

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
            continue

    raise Exception("파일을 읽을 수 없습니다.")

# ----------------------------
# 컬럼 자동 찾기
# ----------------------------
def find_column(df, keywords):

    for col in df.columns:
        for key in keywords:
            if key in col:
                return col
    return None


if uploaded_file:

    try:

        df = load_file(uploaded_file)

    except Exception as e:

        st.error(str(e))
        st.stop()

    st.success("파일을 성공적으로 읽었습니다.")

    st.subheader("데이터")

    st.dataframe(df)

    # 컬럼 자동 검색

    name_col = find_column(df, ["주차장"])

    addr_col = find_column(df, ["주소"])

    fee_col = find_column(df, ["요금"])

    lat_col = find_column(df, ["위도"])

    lon_col = find_column(df, ["경도"])

    # 컬럼 확인

    if None in [name_col, addr_col, fee_col]:

        st.error("주차장명, 주소, 요금 컬럼을 찾을 수 없습니다.")

        st.write(df.columns)

        st.stop()

    # ----------------------------

    st.subheader("주소 검색")

    keyword = st.text_input("주소 입력")

    if keyword:

        result = df[
            df[addr_col].astype(str).str.contains(keyword, na=False)
        ]

        if len(result) == 0:

            st.warning("검색 결과가 없습니다.")

        else:

            st.success(f"{len(result)}개의 주차장을 찾았습니다.")

            st.dataframe(
                result[
                    [
                        name_col,
                        addr_col,
                        fee_col
                    ]
                ]
            )

    # ----------------------------

    if lat_col and lon_col:

        st.subheader("주차장 지도")

        df[lat_col] = pd.to_numeric(df[lat_col], errors="coerce")
        df[lon_col] = pd.to_numeric(df[lon_col], errors="coerce")

        df = df.dropna(subset=[lat_col, lon_col])

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=f"[{lon_col}, {lat_col}]",
            get_radius=60,
            get_fill_color=[0, 128, 255, 180],
            pickable=True,
        )

        view = pdk.ViewState(
            latitude=df[lat_col].mean(),
            longitude=df[lon_col].mean(),
            zoom=12,
        )

        tooltip = {
            "html": f"""
            <b>주차장</b><br/>
            {{{name_col}}}<br/><br/>

            <b>주소</b><br/>
            {{{addr_col}}}<br/><br/>

            <b>요금</b><br/>
            {{{fee_col}}}
            """,

            "style": {
                "backgroundColor": "#2c3e50",
                "color": "white"
            }
        }

        st.pydeck_chart(
            pdk.Deck(
                layers=[layer],
                initial_view_state=view,
                tooltip=tooltip,
            )
        )

    else:

        st.warning("위도·경도 컬럼이 없어 지도를 표시할 수 없습니다.")
