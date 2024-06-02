# Description: 共通関数を定義するモジュール

# 秒数から時間を計算する関数
def seconds_to_time(seconds: int):
    # 時間を計算
    hours, remainder = divmod(seconds, 3600)
    # 分を計算
    minutes, seconds = divmod(remainder, 60)
    # 時間、分、秒を返す
    return hours, minutes, seconds
