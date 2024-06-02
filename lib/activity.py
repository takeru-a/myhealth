import streamlit as st
import pandas as pd
import requests 

import lib.common as cn

# 活動データを取得
@st.cache_data(ttl=60 * 60 * 24)
def get_activity_data(headers, params):
    activity_endpoint_url = 'https://api.ouraring.com/v2/usercollection/daily_activity'
    response = requests.get(activity_endpoint_url, headers=headers, params=params)
    data = response.json()
    activity_data = pd.DataFrame(data['data'])
    return activity_data

# 活動データの表示
@st.cache_data(ttl=60 * 60 * 24)
def activity_display(data, today, yesterday):
        
    today_data = data[data['day'] == today]
    yesterday_data = data[data['day'] == yesterday]

    if today_data.empty:
        today_data = yesterday_data
    st.write("#### 本日の活動スコア")
    st.progress(int(today_data['score'].iloc[0]), text=f"Score {int(today_data['score'].iloc[0])}")
    active_calories, total_calories = st.columns(2)
    equivalent_walking_distance , steps, sedentary_time ,non_wear_time = st.columns(4)
    
    # 活動による消費カロリー
    delta_active_calories = int(today_data['active_calories'].iloc[0]) - int(yesterday_data['active_calories'].iloc[0])
    active_calories.metric("Active Calories", f"{int(today_data['active_calories'].iloc[0])}kcal", f"{delta_active_calories}kcal")
    # 総カロリー
    delta_total_calories = int(today_data['total_calories'].iloc[0]) - int(yesterday_data['total_calories'].iloc[0])
    total_calories.metric("Total Calories", f"{int(today_data['total_calories'].iloc[0])}kcal", f"{delta_total_calories}kcal")
    
    # 歩行距離
    delta_equivalent_walking_distance = (int(today_data['equivalent_walking_distance'].iloc[0]) - int(yesterday_data['equivalent_walking_distance'].iloc[0])) / 1000
    equivalent_walking_distance.metric("歩行距離", f"{int(today_data['equivalent_walking_distance'].iloc[0])/1000}km", f"{delta_equivalent_walking_distance}km")
    
    # 歩数
    delta_steps = int(today_data['steps'].iloc[0]) - int(yesterday_data['steps'].iloc[0])
    steps.metric("歩数", f"{int(today_data['steps'].iloc[0])}", f"{delta_steps}")
    
    # 座っていた時間
    delta_sedentary_time = int(today_data['sedentary_time'].iloc[0]) - int(yesterday_data['sedentary_time'].iloc[0])
    hours, minutes, _ = cn.seconds_to_time(int(today_data['sedentary_time'].iloc[0]))
    delta_hours, delta_minutes, _ = cn.seconds_to_time(delta_sedentary_time)
    sedentary_time.metric("座っていた時間", f"{hours}h {minutes}m", f"{delta_hours}h{delta_minutes}m")
    
    # 非着用時間
    hours, minutes, _ = cn.seconds_to_time(int(today_data['non_wear_time'].iloc[0]))
    non_wear_time.metric("非着用時間", f"{hours}h {minutes}m")
    