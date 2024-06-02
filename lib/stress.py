import streamlit as st
import pandas as pd
import requests 

import lib.common as cn

# ストレスデータを取得
@st.cache_data(ttl=60 * 60 * 24)
def get_stress_data(headers, params):
    stress_endpoint_url = 'https://api.ouraring.com/v2/usercollection/daily_stress'
    response = requests.get(stress_endpoint_url, headers=headers, params=params)
    data = response.json()
    stress_data = pd.DataFrame(data['data'])
    return stress_data

def display_stress_status(data):
    if data == 'restored':
        return 'リラックス :satisfied:'
    elif data == 'normal':
        return '正常 :flushed:'
    elif data == 'stressful':
        return 'ストレスフル :scream:'
    else:
        return '不明 :confused:'

# ストレスデータの表示
@st.cache_data(ttl=60 * 60 * 24)
def stress_display(data, today, yesterday):
    stress_time, relax_time = st.columns(2)
    
    # ストレス値の取得確認
    today_data = data[data["day"] == today]
    yesterday_data = data[data["day"] == yesterday]
    
    if today_data.empty:
        today_data = yesterday_data

    # ストレス値の表示
    if today_data.empty:
        # 前日のストレス値
        st_hours, st_minutes, st_seconds = cn.seconds_to_time(int(yesterday_data["stress_high"].iloc[0]))
        re_hours, re_minutes, re_seconds = cn.seconds_to_time(int(yesterday_data["recovery_high"].iloc[0]))
        stress_time.metric("StressFullTime", f"{st_hours}h {st_minutes}m {st_seconds}s")
        relax_time.metric("RelaxTime", f"{re_hours}h {re_minutes}m {re_seconds}s")
    else:
        # 本日のストレス値
        st_hours, st_minutes, _ = cn.seconds_to_time(int(today_data["stress_high"].iloc[0]))
        re_hours, re_minutes, _ = cn.seconds_to_time(int(today_data["recovery_high"].iloc[0]))
          
        # 前日との差分
        stress = int(today_data["stress_high"].iloc[0]) - int(yesterday_data["stress_high"].iloc[0])
        relax = int(today_data["recovery_high"].iloc[0]) - int(yesterday_data["recovery_high"].iloc[0])
        
        delta_stress_hours, delta_stress_minutes, _  = cn.seconds_to_time(stress)
        delta_relax_hours, delta_relax_minutes, _  = cn.seconds_to_time(relax)
        
        st.write("#### :blue[ストレス度]")
        st.write("##### " + display_stress_status(today_data["day_summary"].values[0]))
        stress_time.metric("StressFull Time", f"{st_hours}h {st_minutes}m", f"{delta_stress_hours}h{delta_stress_minutes}m")
        relax_time.metric("Relax Time", f"{re_hours}h {re_minutes}m", f"{delta_relax_hours}h{delta_relax_minutes}m")
