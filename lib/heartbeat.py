import streamlit as st
import pandas as pd
import altair as alt
import requests 

# 心拍数の取得
@st.cache_data()
def get_heartbeat(headers, params):

    heartbeat_endpoint_url = 'https://api.ouraring.com/v2/usercollection/heartrate' 
    response = requests.get(heartbeat_endpoint_url, headers=headers, params=params)
    data = response.json()
    heartbeat_data = pd.DataFrame(data['data'])
    return heartbeat_data

# 心拍数の表示
@st.cache_data(ttl=5 * 60)
def heartbeat_display(data):
     # 最大値、最小値、平均値
    max, min, avg = st.columns(3)

    # 日中平均心拍数
    activate = data[data["source"] == "awake"]

    max.metric("Maximum", str(data["bpm"].max()) + "bpm")
    min.metric("Minimum", str(data["bpm"].min()) + "bpm")
    avg.metric("Activity Average",  "{:.1f}".format(activate["bpm"].mean()) + "bpm")

# 心拍数のchart表示
@st.cache_data(ttl=5 * 60)
def heartbeat_chart(data):   
    # altairによるチャートグラフ作成
    base_chart = alt.Chart(data).mark_line().encode(
        x=alt.X('timestamp:T'),
        y=alt.Y('bpm:Q'),
    )

    hover = alt.selection_point(
        fields=["timestamp"],
        on='mouseover',
        nearest=True,
        empty='none'
    )
    
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            y="bpm",
            opacity=alt.value(0),
            tooltip=[
            alt.Tooltip('timestamp:T',format='%m/%d %H:%M',title='timestamp'),
            'bpm:Q', 
            alt.Tooltip('source:N', title='status')
        ]
        )
        .add_params(hover)
    )

    chart = alt.layer(
        base_chart,
        base_chart.transform_filter(hover).mark_circle(size=64).encode
        (
            color=alt.condition(hover, alt.value('lightgray'), alt.value('blue'))
        ),
        tooltips
    ).configure_axisX(
        format='%m/%d %H:%M'
    ).interactive()

    st.altair_chart(chart, use_container_width=True)
