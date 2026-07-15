import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(
    page_title="공영주차장 안내",
    layout="wide"
)

st.title("🅿 공영주차장 정보 안내")

st.write("CSV 파일을 업로드하세요.")

uploaded_file = st.file_uploader(
    "CSV 업로드",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success("데이터 업로드 완료")

    st.subheader("데이터 미리보기")
    st.dataframe(df)

    st.markdown("---")

    st.subheader("주소 검색")

    keyword = st.text_input("주소를 입력하세요")

    if keyword != "":
        result = df[df["주소"].str.contains(keyword, case=False, na=False)]

        if len(result) == 0:
            st.warning("검색 결과가 없습니다.")

        else:

            st.success(f"{len(result)}개의 주차장을 찾았습니다.")

            st.dataframe(
                result[["주차장명", "주소", "주차요금"]]
            )

    st.markdown("---")

    st.subheader("공영주차장 지도")

    # 지도 표시를 위해 위도/경도가 있어야 함
    # CSV에는 반드시 아래 컬럼이 있어야 함.
    #
    # 위도
    # 경도

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[경도, 위도]',
        get_radius=40,
        get_fill_color='[255,0,0,180]',
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=df["위도"].mean(),
        longitude=df["경도"].mean(),
        zoom=12,
        pitch=0,
    )

    tooltip = {
        "html": """
        <b>주차장</b> : {주차장명}<br/>
        <b>주소</b> : {주소}<br/>
        <b>주차요금</b> : {주차요금}
        """,
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
    )

    st.pydeck_chart(deck)
