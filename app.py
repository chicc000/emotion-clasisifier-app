import streamlit as st
import pandas as pd
import random

# 讀取 CSV，並轉成 list of dicts
try:
    df = pd.read_csv("songs.csv", encoding="utf-8")
    songs = df.to_dict(orient="records")
except FileNotFoundError:
    st.error("找不到 songs.csv 檔案，請確認檔案是否存在。")
    st.stop()
except Exception as e:
    st.error(f"讀取 CSV 檔案失敗：{e}")
    st.stop()

st.set_page_config(page_title="音樂情緒分類器", layout="centered")
st.title("音樂情緒分類器")
st.markdown("依據你的情緒或情境，推薦合適的歌曲\n支援：中文、日文、英文、韓文")

st.write("歌曲資料類型:", type(songs))
if isinstance(songs, list):
    st.write("第一筆資料:", songs[0])
else:
    st.error("songs 不是 list，資料格式不正確！")

emotions = ["愉悅", "憤怒", "煩躁", "悲傷"]

mode = st.radio("請選擇輸入方式：", ["從選單選擇情緒", "輸入生活情境"])
user_emotion = None

if mode == "從選單選擇情緒":
    user_emotion = st.selectbox("請選擇你目前的情緒", emotions)
else:
    situation = st.text_input("請輸入你目前的情境（例如：今天功課寫不完好煩躁）")
    if situation:
        if any(word in situation for word in ["開心", "快樂", "喜歡", "幸福", "開胃", "期待"]):
            user_emotion = "愉悅"
        elif any(word in situation for word in ["生氣", "氣死", "爆炸", "火大", "罵人", "衝突"]):
            user_emotion = "憤怒"
        elif any(word in situation for word in ["煩", "煩躁", "壓力", "緊張", "焦慮", "厭世"]):
            user_emotion = "煩躁"
        elif any(word in situation for word in ["難過", "悲傷", "委屈", "哭", "崩潰", "失落", "孤單"]):
            user_emotion = "悲傷"
        else:
            user_emotion = "煩躁"
        st.success(f"系統判斷你的情緒為：**{user_emotion}**")

if user_emotion:
    language = st.selectbox("選擇歌曲語言", ["中文", "日文", "英文", "韓文"])
    genre = st.selectbox("選擇曲風", ["流行", "搖滾", "嘻哈", "電子", "民謠", "爵士", "其他"])
    era = st.selectbox("選擇年代", ["1980年代", "1990年代", "2000年代", "2010年代至今", "1960年代", "1970年代"])

    filtered_songs = []
    for s in songs:
        try:
            if (s.get("emotion") == user_emotion
                and s.get("language") == language
                and s.get("genre") == genre
                and s.get("decade") == era):  # 注意原欄位是 decade 不是 era
                filtered_songs.append(s)
        except Exception as e:
            st.write(f"資料錯誤，跳過該筆：{s}")
            st.write(f"錯誤訊息：{e}")

    if filtered_songs:
        st.subheader("為你推薦的歌曲：")
        for song in random.sample(filtered_songs, min(5, len(filtered_songs))):
            st.markdown(
                f"**{song.get('title', '未知標題')}** - *{song.get('artist', '未知歌手')}*  \n"
                f"風格：{song.get('genre', '未知')} | 年代：{song.get('decade', '未知')}  \n"
                f"歌詞片段：{song.get('lyrics', '無歌詞資料')}"
            )
            if song.get("preview_url"):
                st.video(song["preview_url"])
    else:
        st.warning("找不到符合條件的歌曲，請試試其他選項～")
