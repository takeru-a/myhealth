import streamlit as st
import datetime

import lib.sleep as sl
import lib.heartbeat as hb
import lib.activity as ac
import lib.stress as stress

st.set_page_config(
    page_title="My health", page_icon="♥", layout="centered"
)

# 設定値
now = datetime.datetime.now(datetime.timezone.utc)
end_date = now.strftime("%Y-%m-%d")
start_date = (now + datetime.timedelta(days=-2)).strftime("%Y-%m-%d")

end_date_time = now.strftime("%Y-%m-%dT%H:%M:%S")
start_date_time = (now + datetime.timedelta(days=-1)).strftime("%Y-%m-%dT%H:%M:%S")
date_params = { 
    'start_date': start_date, 
    'end_date': end_date, 
}

datetime_params = { 
    'start_datetime': start_date_time, 
    'end_datetime': end_date_time, 
}

# ヘッダー
headers = { 
  'Authorization': 'Bearer ' + st.secrets['token'],
}

# 画面表示
st.title('_Health_ is :blue[important] :sunglasses:')
st.write('# :orange[Health Information of the Day]')

# 睡眠
st.subheader('睡眠:bed:', divider='rainbow')
data = sl.get_sleep_score_data(headers, date_params)
if data.empty:
    st.write('')
else:
    today = now.strftime("%Y-%m-%d")
    yesterday = (now + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    sl.sleep_score_display(data, today, yesterday)

data = sl.get_sleep_data(headers, date_params)
if data.empty:
    st.write('データがありません')
else:
    today = now.strftime("%Y-%m-%d")
    yesterday = (now + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    sl.sleep_data_display(data, today, yesterday)

# 心拍数
st.subheader('心拍数:heartbeat:', divider='rainbow')
data = hb.get_heartbeat(headers, datetime_params)
if data.empty:
    st.write('データがありません')
else:
    hb.heartbeat_display(data)
    hb.heartbeat_chart(data)

# 活動量
st.subheader('活動量:running:', divider='rainbow')
data = ac.get_activity_data(headers, date_params)
if data.empty:
    st.write('データがありません')
else:
    today = now.strftime("%Y-%m-%d")
    yesterday = (now + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    ac.activity_display(data, today, yesterday)
    

# ストレス値
st.subheader('ストレス値:scream:', divider='rainbow')
data = stress.get_stress_data(headers, date_params)
if data.empty:
    st.write('データがありません')
else:
    today = now.strftime("%Y-%m-%d")
    yesterday = (now + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    stress.stress_display(data, today, yesterday)
