import streamlit as st
import pandas as pd
import json
import os

def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"讀取 JSON 失敗: {e}")
        return pd.DataFrame()

def load_csv(file_path):
    try:
        return pd.read_csv(file_path, encoding="utf-8")
    except Exception as e:
        st.error(f"讀取 CSV 失敗: {e}")
        return pd.DataFrame()

json_df = load_json("full_songs.json") if os.path.exists("full_songs.json") else pd.DataFrame()
csv_df = load_csv("songs.csv") if os.path.exists("songs.csv") else pd.DataFrame()

# 合併時保持所有欄位，欄位不齊全用 NaN 補齊
df = pd.concat([json_df, csv_df], ignore_index=True)

# 移除 title, artist, emotion 欄位是空的資料
df = df.dropna(subset=["title", "artist", "emotion"])

st.title("音樂情緒推薦器")

emotions = sorted(df["emotion"].dropna().unique())
user_emotion = st.selectbox("請選擇你的情緒", emotions)

if user_emotion:
    filtered = df[df["emotion"] == user_emotion]
    st.write(f"找到 {len(filtered)} 首符合「{user_emotion}」的歌曲")

    for _, row in filtered.sample(min(5, len(filtered))).iterrows():
        st.markdown(f"**{row['title']}** － {row['artist']}")
        # 顯示其他欄位可以自行加，以下示範完整顯示歌詞、語言、年代等
        if "lyrics" in row and pd.notna(row["lyrics"]):
            st.write(f"歌詞片段：{row['lyrics']}")
        if "language" in row and pd.notna(row["language"]):
            st.write(f"語言：{row['language']}")
        if "decade" in row and pd.notna(row["decade"]):
            st.write(f"年代：{row['decade']}")
        if "genre" in row and pd.notna(row["genre"]):
            st.write(f"曲風：{row['genre']}")
        if "preview_url" in row and pd.notna(row["preview_url"]):
            st.video(row["preview_url"])
        st.markdown("---")
