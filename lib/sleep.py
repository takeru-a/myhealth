import streamlit as st
import pandas as pd
import requests

import lib.common as cn

# 睡眠スコアデータを取得
@st.cache_data(ttl=5 * 60)
def get_sleep_score_data(headers, params):
    sleep_endpoint_url = 'https://api.ouraring.com/v2/usercollection/daily_sleep'
    response = requests.get(sleep_endpoint_url, headers=headers, params=params)
    data = response.json()
    sleep_data = pd.DataFrame(data['data'])
    return sleep_data

# 睡眠データを取得
@st.cache_data(ttl=5 * 60)
def get_sleep_data(headers, params):
    sleep_endpoint_url = 'https://api.ouraring.com/v2/usercollection/sleep'
    response = requests.get(sleep_endpoint_url, headers=headers, params=params)
    data = response.json()
    sleep_data = pd.DataFrame(data['data'])
    return sleep_data

# 睡眠スコアの表示
@st.cache_data(ttl=5 * 60)
def sleep_score_display(data, today, yesterday):
    
    today_data = data[data['day'] == today]
    yesterday_data = data[data['day'] == yesterday]

    if today_data.empty:
        st.write('')
    else:
        st.write("#### 本日の睡眠スコア")
        st.progress(int(today_data['score'].iloc[0]), text=f"Score {int(today_data['score'].iloc[0])}")
        
        deep_sleep, rem_sleep, total_sleep = st.columns(3)
        today_data = today_data["contributors"].values[0]
        yesterday_data = yesterday_data["contributors"].values[0]
        
        # 深い睡眠時間スコア
        delta_deep_sleep = int(today_data['deep_sleep']) - int(yesterday_data['deep_sleep'])
        deep_sleep.metric("深い睡眠時間スコア", today_data['deep_sleep'], delta_deep_sleep)
            
        # REM睡眠時間スコア
        delta_rem_sleep = int(today_data['rem_sleep']) - int(yesterday_data['rem_sleep'])
        rem_sleep.metric("REM睡眠時間スコア", today_data['rem_sleep'], delta_rem_sleep)
        
        # 総睡眠時間スコア
        delta_total_sleep = int(today_data['total_sleep']) - int(yesterday_data['total_sleep'])
        total_sleep.metric("総睡眠時間スコア", today_data['total_sleep'], delta_total_sleep)
    
# 睡眠データの表示
def sleep_data_display(data, today, yesterday):

    today_data = data[data['day'] == today]
    yesterday_data = data[data['day'] == yesterday]
    
    if today_data.empty:
        st.write('データがありません')
    else:
        # 表示睡眠データ項目
        time_in_bed, total_sleep_duration, efficiency = st.columns(3)
        deep_sleep_duration, rem_sleep_duration, light_sleep_duration = st.columns(3)
        bedtime_start, bedtime_end = st.columns(2)
        average_breath, average_heart_rate = st.columns(2)
        awake_time, latency = st.columns(2)
        
        # 平均呼吸数
        delta_average_breath = int(today_data['average_breath'].iloc[0]) - int(yesterday_data['average_breath'].iloc[0])
        average_breath.metric("平均呼吸数", today_data['average_breath'].iloc[0], delta_average_breath)
        
        # 平均心拍数
        delta_average_heart_rate = int(today_data['average_heart_rate'].iloc[0]) - int(yesterday_data['average_heart_rate'].iloc[0])
        average_heart_rate.metric("平均心拍数", today_data['average_heart_rate'].iloc[0], delta_average_heart_rate)
        
        # 就寝時間
        time = today_data['bedtime_start'].iloc[0].split('T')[1]
        bedtime_start.metric("就寝時間", (time.split(':')[0] + ':' + time.split(':')[1]))
        # 起床時間
        time = today_data['bedtime_end'].iloc[0].split('T')[1]
        bedtime_end.metric("起床時間", (time.split(':')[0] + ':' + time.split(':')[1]))
        
        # ベットに入っていた時間
        delta_time_in_bed = int(today_data['time_in_bed'].iloc[0]) - int(yesterday_data['time_in_bed'].iloc[0])
        hours, minutes, _ = cn.seconds_to_time(int(today_data['time_in_bed'].iloc[0]))
        delta_hours, delta_minutes, _ = cn.seconds_to_time(delta_time_in_bed)
        time_in_bed.metric("ベットにいた時間", f"{hours}h {minutes}m", f"{delta_hours}h{delta_minutes}m")
        
        # 総睡眠時間
        delta_total_sleep_duration = int(today_data['total_sleep_duration'].iloc[0]) - int(yesterday_data['total_sleep_duration'].iloc[0])
        hours, minutes, _ = cn.seconds_to_time(int(today_data['total_sleep_duration'].iloc[0]))
        delta_hours, delta_minutes, _ = cn.seconds_to_time(delta_total_sleep_duration)
        total_sleep_duration.metric("総睡眠時間", f"{hours}h {minutes}m", f"{delta_hours}h{delta_minutes}m")
        
        # 睡眠効率
        delta_efficiency = int(today_data['efficiency'].iloc[0]) - int(yesterday_data['efficiency'].iloc[0])
        efficiency.metric("睡眠効率", f"{today_data['efficiency'].iloc[0]}%", delta_efficiency)
        
        # 深い睡眠時間
        delta_deep_sleep_duration = int(today_data['deep_sleep_duration'].iloc[0]) - int(yesterday_data['deep_sleep_duration'].iloc[0])
        hours, minutes, _ = cn.seconds_to_time(int(today_data['deep_sleep_duration'].iloc[0]))
        delta_hours, delta_minutes, _ = cn.seconds_to_time(delta_deep_sleep_duration)
        deep_sleep_duration.metric("深い睡眠時間", f"{hours}h {minutes}m", f"{delta_hours}h{delta_minutes}m")
        
        # REM睡眠時間
        delta_rem_sleep_duration = int(today_data['rem_sleep_duration'].iloc[0]) - int(yesterday_data['rem_sleep_duration'].iloc[0])
        hours, minutes, _ = cn.seconds_to_time(int(today_data['rem_sleep_duration'].iloc[0]))
        delta_hours, delta_minutes, _ = cn.seconds_to_time(delta_rem_sleep_duration)
        rem_sleep_duration.metric("REM睡眠時間", f"{hours}h {minutes}m", f"{delta_hours}h{delta_minutes}m")
        
        # 浅い睡眠時間
        delta_light_sleep_duration = int(today_data['light_sleep_duration'].iloc[0]) - int(yesterday_data['light_sleep_duration'].iloc[0])
        hours, minutes, _ = cn.seconds_to_time(int(today_data['light_sleep_duration'].iloc[0]))
        delta_hours, delta_minutes, _ = cn.seconds_to_time(delta_light_sleep_duration)
        light_sleep_duration.metric("浅い睡眠時間", f"{hours}h {minutes}m", f"{delta_hours}h{delta_minutes}m")
        
        # 覚醒時間
        delta_awake_time = int(today_data['awake_time'].iloc[0]) - int(yesterday_data['awake_time'].iloc[0])
        hours, minutes, _ = cn.seconds_to_time(int(today_data['awake_time'].iloc[0]))
        delta_hours, delta_minutes, _ = cn.seconds_to_time(delta_awake_time)
        awake_time.metric("覚醒時間", f"{hours}h {minutes}m", f"{delta_hours}h{delta_minutes}m")
        
        # 寝るまでの時間
        delta_latency = int(today_data['latency'].iloc[0]) - int(yesterday_data['latency'].iloc[0])
        hours, minutes, _ = cn.seconds_to_time(int(today_data['latency'].iloc[0]))
        delta_hours, delta_minutes, _ = cn.seconds_to_time(delta_latency)
        latency.metric("寝るまでの時間", f"{hours}h {minutes}m", f"{delta_hours}h {delta_minutes}m")
    