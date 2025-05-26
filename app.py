import streamlit as st
import json
import random

# 載入歌曲資料
with open("songs.json", "r", encoding="utf-8") as f:
    songs = json.load(f)

# 過濾掉缺欄位的歌曲資料
required_keys = ["title", "artist", "emotion", "language", "genre", "era", "lyrics", "youtube"]
songs = [s for s in songs if all(k in s for k in required_keys)]

# 定義預設情緒
emotions = ["愉悅", "憤怒", "煩躁", "悲傷"]

st.set_page_config(page_title="音樂情緒分類器", layout="centered")
st.title("音樂情緒分類器")
st.markdown("依據你的情緒或情境，推薦合適的歌曲\n支援：中文、日文、英文、韓文")

# 選擇輸入方式
mode = st.radio("請選擇輸入方式：", ["從選單選擇情緒", "輸入生活情境"])

user_emotion = None

if mode == "從選單選擇情緒":
    user_emotion = st.selectbox("請選擇你目前的情緒", emotions)

else:
    situation = st.text_input("請輸入你目前的情境（例如：今天功課寫不完好煩躁）")
    if situation:
        # 簡易情緒偵測邏輯
        if any(word in situation for word in ["開心", "快樂", "喜歡", "幸福", "開胃", "期待"]):
            user_emotion = "愉悅"
        elif any(word in situation for word in ["生氣", "氣死", "爆炸", "火大", "罵人", "衝突"]):
            user_emotion = "憤怒"
        elif any(word in situation for word in ["煩", "煩躁", "壓力", "緊張", "焦慮", "厭世"]):
            user_emotion = "煩躁"
        elif any(word in situation for word in ["難過", "悲傷", "委屈", "哭", "崩潰", "失落", "孤單"]):
            user_emotion = "悲傷"
        else:
            user_emotion = "煩躁"  # fallback 預設為煩躁
        st.success(f"系統判斷你的情緒為：**{user_emotion}**")

# 推薦邏輯
if user_emotion:
    language = st.selectbox("選擇歌曲語言", ["中文", "日文", "英文", "韓文"])
    genre = st.selectbox("選擇曲風", ["流行", "搖滾", "嘻哈", "電子", "民謠", "爵士", "其他"])
    era = st.selectbox("選擇年代", ["80年代", "90年代", "2000年代", "2010年代至今"])

    # 篩選歌曲資料
    filtered_songs = [
        s for s in songs
        if s.get("emotion") == user_emotion
        and s.get("language") == language
        and s.get("genre") == genre
        and s.get("era") == era
    ]

    # 顯示推薦結果
    if filtered_songs:
        st.subheader("為你推薦的歌曲：")
        for song in random.sample(filtered_songs, min(5, len(filtered_songs))):
            st.markdown(f"**{song['title']}** - *{song['artist']}*  \n"
                        f"風格：{song['genre']} | 年代：{song['era']}  \n"
                        f"歌詞片段：{song['lyrics']}")
            st.video(song["youtube"])
    else:
        st.warning("找不到符合條件的歌曲，請試試其他選項～")

