import streamlit as st
import pandas as pd
import random

# 讀取 CSV（假設檔名是 songs.csv，請根據實際修改）
try:
    df = pd.read_csv("songs.csv", encoding="utf-8")
except FileNotFoundError:
    st.error("找不到 songs.csv 檔案，請確認檔案是否存在於專案目錄中")
    st.stop()
except Exception as e:
    st.error(f"讀取 CSV 發生錯誤：{e}")
    st.stop()

# 驗證欄位
required_columns = {"title", "artist", "emotion"}
if not required_columns.issubset(set(df.columns)):
    st.error("CSV 檔案缺少必要欄位：title, artist, emotion")
    st.stop()

# 頁面設定
st.set_page_config(page_title="簡易音樂推薦", layout="centered")
st.title("情緒音樂推薦")
st.markdown("根據你的情緒，推薦合適的歌曲 🎧")

# 情緒選單
emotions = df["emotion"].dropna().unique().tolist()
user_emotion = st.selectbox("請選擇你的情緒：", emotions)

# 推薦歌曲
if user_emotion:
    filtered = df[df["emotion"] == user_emotion]

    if not filtered.empty:
        st.subheader("推薦歌曲：")
        for _, row in filtered.sample(min(5, len(filtered))).iterrows():
            st.markdown(f"- 🎵 **{row['title']}** - *{row['artist']}*")
    else:
        st.warning("沒有符合此情緒的歌曲，請試試其他情緒喔～")
