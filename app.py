import streamlit as st
import pandas as pd

songs = pd.DataFrame([
    {"title": "晴天", "artist": "周杰倫", "emotion": "愉悅", "genre": "流行"},
    {"title": "怒放的生命", "artist": "五月天", "emotion": "憤怒", "genre": "搖滾"},
])

st.title("簡易歌曲推薦")

user_emotion_input = st.text_input("請輸入情緒 (愉悅、悲傷、憤怒、平靜、煩躁)")

if st.button("推薦歌曲"):
    if not user_emotion_input:
        st.warning("請輸入情緒")
    else:
        filtered = songs[songs['emotion'] == user_emotion_input]
        if not filtered.empty:
            for idx, row in filtered.iterrows():
                st.write(f"- {row['title']} by {row['artist']} [{row['genre']}]")
        else:
            st.write(f"找不到情緒為『{user_emotion_input}』的歌曲。")
