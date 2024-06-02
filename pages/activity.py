import streamlit as st
import datetime

import lib.activity as ac

st.set_page_config(
    page_title="My health", page_icon="♥", layout="centered"
)

# ヘッダー
headers = { 
  'Authorization': 'Bearer ' + st.secrets['token'],
}

# 画面表示
st.title('_Health_ is :blue[important] :sunglasses:')

# 設定値
now = datetime.date.today()

date = st.date_input("日付を入力してね！", now)
end_date = str(date)
ed = end_date + " 00:00:00"
end_datetime = datetime.datetime.strptime(ed, '%Y-%m-%d %H:%M:%S')
start_date = (end_datetime + datetime.timedelta(days=-2)).strftime("%Y-%m-%d")
yesterday = (end_datetime + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")

date_params = { 
    'start_date': start_date, 
    'end_date': end_date, 
}

st.subheader('活動量:running:', divider='rainbow')
data = ac.get_activity_data(headers, date_params)
if data.empty:
    st.write('データがありません')
else:
    ac.activity_display(data, end_date, yesterday)
