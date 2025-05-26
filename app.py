import streamlit as st
import librosa
import pandas as pd

# --- 載入歌曲資料庫 ---
def load_song_database():
    try:
        df = pd.read_csv("songs.csv")  # 欄位：title, artist, emotion
        return df
    except:
        return pd.DataFrame(columns=["title", "artist", "emotion"])

song_db = load_song_database()

# --- UI ---
st.set_page_config(page_title="歌曲情緒分類器", layout="centered")
st.title("🎵 歌曲情緒分類器")
st.markdown("依據歌詞與音訊特徵，自動辨識歌曲情緒並推薦相似音樂。")

option = st.radio("請選擇輸入方式：", ("輸入歌詞", "上傳音訊檔"))

lyrics = ""
emotion_from_lyrics = None
emotion_from_audio = None
final_emotion = None

# --- 歌詞情緒分析（加否定詞判斷） ---
def analyze_lyrics_emotion(lyrics_text):
    keywords = {
        "快樂": ["happy", "sunshine", "joy", "笑", "快樂", "喜悅"],
        "悲傷": ["sad", "cry", "lonely", "哭", "淚", "傷心", "孤單"],
        "憤怒": ["angry", "rage", "hate", "憤怒", "生氣", "火"],
        "平靜": ["calm", "peace", "quiet", "平靜", "安靜", "寧靜"]
    }
    negations = ["不", "沒", "無", "沒有", "never", "no", "not"]

    lyrics_lower = lyrics_text.lower()
    score = {emotion: 0 for emotion in keywords}

    for emotion, words in keywords.items():
        for word in words:
            start = 0
            while True:
                idx = lyrics_lower.find(word.lower(), start)
                if idx == -1:
                    break
                neg_flag = False
                for neg in negations:
                    neg_idx = lyrics_lower.find(neg, max(0, idx-3), idx)
                    if neg_idx != -1:
                        neg_flag = True
                        break
                if not neg_flag:
                    score[emotion] += 1
                start = idx + len(word)

    predicted_emotion = max(score, key=score.get)
    return f"推測情緒為：{predicted_emotion}（依據詞彙出現頻率，考慮否定詞）"

# --- 音訊情緒分析 ---
def extract_audio_emotion(file):
    import numpy as np
    try:
        y, sr = librosa.load(file, sr=None)
        tempo = librosa.beat.tempo(y=y, sr=sr)[0]
        chroma = librosa.feature.chroma_stft(y=y, sr=sr).mean()
        zcr = librosa.feature.zero_crossing_rate(y).mean()

        if tempo > 120 and chroma > 0.5:
            return "快樂"
        elif tempo < 80 and zcr < 0.1:
            return "悲傷"
        elif zcr > 0.2:
            return "憤怒"
        else:
            return "平靜"
    except Exception as e:
        return f"[錯誤] 音訊分析失敗：{str(e)}"

# --- 推薦歌曲 ---
def recommend_songs(emotion_label, db):
    results = db[db["emotion"] == emotion_label]
    return results.sample(n=min(5, len(results))) if not results.empty else pd.DataFrame()

# --- 主流程 ---
if option == "輸入歌詞":
    lyrics = st.text_area("請貼上歌詞：", height=200)
    if st.button("分析歌詞情緒") and lyrics:
        with st.spinner("分析中..."):
            emotion_from_lyrics = analyze_lyrics_emotion(lyrics)
            st.success("分析完成！")
            st.markdown(f"**🎤 歌詞情緒：**\n\n{emotion_from_lyrics}")
            for label in ["快樂", "悲傷", "憤怒", "平靜"]:
                if label in emotion_from_lyrics:
                    final_emotion = label
                    break

elif option == "上傳音訊檔":
    uploaded_file = st.file_uploader("請上傳音訊檔案（mp3/wav）")
    if uploaded_file is not None:
        with st.spinner("分析音訊中..."):
            emotion_from_audio = extract_audio_emotion(uploaded_file)
            st.success("分析完成！")
            st.markdown(f"**🎧 音訊情緒：** {emotion_from_audio}")
            final_emotion = emotion_from_audio

if final_emotion:
    st.markdown("---")
    st.subheader("🎯 綜合分析結果：")
    st.markdown(f"**預測情緒分類： `{final_emotion}`**")

    st.markdown("---")
    st.subheader("🎵 推薦相似情緒歌曲：")
    recs = recommend_songs(final_emotion, song_db)
    if recs.empty:
        st.info("目前資料庫中無相符歌曲，請補充 songs.csv")
    else:
        for idx, row in recs.iterrows():
            st.markdown(f"- 🎶 **{row['title']}** by *{row['artist']}*")
