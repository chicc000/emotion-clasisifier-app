import streamlit as st
import pandas as pd
import librosa
import numpy as np
import openai
import io

# 你的 OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 載入歌曲資料
@st.cache_data
def load_songs(file):
    return pd.read_csv(file)

songs = load_songs("songs.csv")

def extract_audio_features(audio_bytes):
    y, sr = librosa.load(io.BytesIO(audio_bytes), sr=22050)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch = np.mean(pitches[magnitudes > np.median(magnitudes)])
    return tempo, pitch

def analyze_lyrics_emotion(lyrics_text):
    prompt = f"請分析以下歌詞，判斷主要情緒（愉悅、悲傷、憤怒、平靜、煩躁），並只回傳情緒詞：\n\n{lyrics_text}"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user", "content": prompt}],
        max_tokens=10,
        temperature=0
    )
    emotion = response.choices[0].message.content.strip()
    return emotion

st.title("音樂情緒分析與推薦系統")

uploaded_audio = st.file_uploader("上傳音訊檔 (wav/mp3)", type=["wav","mp3"])
input_lyrics = st.text_area("或輸入歌詞文本")

user_emotion_input = st.text_input("或手動輸入情緒 (愉悅、悲傷、憤怒、平靜、煩躁)")

if st.button("分析並推薦歌曲"):
    if uploaded_audio is None and not input_lyrics and not user_emotion_input:
        st.warning("請至少提供音訊檔、歌詞或情緒。")
    else:
        emotion_detected = None

        if user_emotion_input.strip():
            emotion_detected = user_emotion_input.strip()
            st.write(f"使用者手動輸入情緒：{emotion_detected}")
        else:
            if input_lyrics.strip():
                emotion_detected = analyze_lyrics_emotion(input_lyrics)
                st.write(f"AI 判斷歌詞情緒為：{emotion_detected}")
            elif uploaded_audio is not None:
                audio_bytes = uploaded_audio.read()
                tempo, pitch = extract_audio_features(audio_bytes)
                st.write(f"音訊特徵：節奏 {tempo:.2f}, 平均音高 {pitch:.2f}")

                # 根據節奏與音高簡單判斷情緒示例（可再優化）
                if tempo > 120:
                    emotion_detected = "愉悅"
                elif tempo < 80:
                    emotion_detected = "悲傷"
                else:
                    emotion_detected = "平靜"
                st.write(f"簡單音訊分析推測情緒：{emotion_detected}")

        if emotion_detected:
            filtered = songs[songs['emotion'] == emotion_detected]
            if not filtered.empty:
                st.write(f"推薦以下情緒為『{emotion_detected}』的歌曲：")
                for idx, row in filtered.iterrows():
                    st.write(f"- {row['title']} by {row['artist']} [{row.get('genre', '未知曲風')}]")
            else:
                st.write(f"抱歉，找不到情緒為『{emotion_detected}』的歌曲。")

