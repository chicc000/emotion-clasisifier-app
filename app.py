import streamlit as st
import pandas as pd
import json
import os
import random

st.set_page_config(page_title="簡易音樂推薦", layout="centered")
st.title("情緒音樂推薦系統 🎧")

# 嘗試載入檔案
data = None
filename = None

if os.path.exists("songs.csv"):
    try:
        data = pd.read_csv("songs.csv", encoding="utf-8")
        filename = "songs.csv"
    except Exception as e:
        st.error(f"讀取 CSV 失敗：{e}")
elif os.path.exists("songs.json"):
    try:
        with open("songs.json", "r", encoding="utf-8") as f:
            data = pd.DataFrame(json.load(f))
        filename = "songs.json"
    except Exception as e:
        st.error(f"讀取 JSON 失敗：{e}")
else:
    st.error("找不到 songs.csv 或 songs.json，請確認檔案是否存在")
    st.stop()

# 驗證欄位
required_cols = {"title", "artist", "emotion"}
if not required_cols.issubset(set(data.columns)):
    st.error(f"資料格式錯誤，檔案 {filename} 缺少必要欄位：title, artist, emotion")
    st.stop()

# 使用者選擇情緒
emotions = sorted(data["emotion"].dropna().unique().tolist())
user_emotion = st.selectbox("請選擇你的情緒：", emotions)

if user_emotion:
    filtered = data[data["emotion"] == user_emotion]
    if not filtered.empty:
        st.subheader("為你推薦的歌曲：")
        for _, row in filtered.sample(min(5, len(filtered))).iterrows():
            st.markdown(f"- 🎵 **{row['title']}** - *{row['artist']}*")
    else:
        st.warning("找不到符合此情緒的歌曲")

