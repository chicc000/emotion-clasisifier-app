import streamlit as st
import csv
import random

# 讀取 CSV 資料
def load_songs(csv_file):
    songs = []
    with open(csv_file, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(row)
    return songs

songs = load_songs("song.csv")

st.set_page_config(page_title="音樂情緒分類器", layout="centered")
st.title("音樂情緒分類器")
st.markdown("依據你的情緒或情境，推薦合適的歌曲\n支援多種曲風與語言")

emotions = ["愉悅", "憤怒", "煩躁", "悲傷"]

mode = st.radio("請選擇輸入方式：", ["從選單選擇情緒", "輸入生活情境"])

user_emotion = None

if mode == "從選單選擇情緒":
    user_emotion = st.selectbox("請選擇你目前的情緒", emotions)
else:
    situation = st.text_input("請輸入你目前的情境（例如：今天功課寫不完好煩躁）")
    if situation:
        if any(word in situation for word in ["開心", "快樂", "喜歡", "幸福", "期待"]):
            user_emotion = "愉悅"
        elif any(word in situation for word in ["生氣", "氣死", "爆炸", "火大", "罵人", "衝突"]):
            user_emotion = "憤怒"
        elif any(word in situation for word in ["煩", "煩躁", "壓力", "緊張", "焦慮", "厭世"]):
            user_emotion = "煩躁"
        elif any(word in situation for word in ["難過", "悲傷", "委屈", "哭", "崩潰", "失落", "孤單"]):
            user_emotion = "悲傷"
        else:
            user_emotion = "煩躁"  # 預設煩躁
        st.success(f"系統判斷你的情緒為：**{user_emotion}**")

if user_emotion:
    # 只用情緒推薦歌曲，因為你說只用title、artist、emotion
    filtered_songs = [s for s in songs if s['emotion'] == user_emotion]

    if filtered_songs:
        st.subheader("為你推薦的歌曲：")
        for song in random.sample(filtered_songs, min(5, len(filtered_songs))):
            st.markdown(f"**{song['title']}** - *{song['artist']}*  \n情緒：{song['emotion']}")
    else:
        st.warning("找不到符合條件的歌曲，請試試其他選項～")
