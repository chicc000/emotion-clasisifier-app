import streamlit as st
import pandas as pd
import tempfile
import librosa
import numpy as np

# 歌詞情緒分析（簡易示範）
def analyze_lyrics_emotion(lyrics_text):
    lyrics_lower = lyrics_text.lower()
    if any(w in lyrics_lower for w in ['happy', 'joy', 'love', 'smile']):
        return '愉悅'
    if any(w in lyrics_lower for w in ['sad', 'cry', 'hurt', 'alone']):
        return '悲傷'
    if any(w in lyrics_lower for w in ['angry', 'hate', 'mad']):
        return '憤怒'
    if any(w in lyrics_lower for w in ['calm', 'peace', 'quiet']):
        return '平靜'
    if any(w in lyrics_lower for w in ['frustrate', 'annoy', 'nervous']):
        return '煩躁'
    return '平靜'

# 音訊情緒分析（示範）：根據節奏、音調簡單判斷
def analyze_audio_emotion(y, sr):
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    
    # 計算平均基頻 (pitch)
    pitch_vals = pitches[magnitudes > np.median(magnitudes)]
    if len(pitch_vals) == 0:
        avg_pitch = 0
    else:
        avg_pitch = np.mean(pitch_vals)

    # 簡單規則判斷情緒
    # 節奏快且音調高 -> 愉悅
    # 節奏慢且音調低 -> 悲傷
    # 節奏快且音調低 -> 煩躁
    # 節奏慢且音調高 -> 平靜
    # 其他為憤怒

    if tempo > 120 and avg_pitch > 150:
        return "愉悅"
    elif tempo <= 120 and avg_pitch <= 150:
        return "悲傷"
    elif tempo > 120 and avg_pitch <= 150:
        return "煩躁"
    elif tempo <= 120 and avg_pitch > 150:
        return "平靜"
    else:
        return "憤怒"

def load_songs(csv_path='songs.csv'):
    df = pd.read_csv(csv_path, encoding='utf-8')
    return df

def recommend_songs(songs_df, emotion, top_n=5):
    filtered = songs_df[songs_df['emotion'] == emotion]
    return filtered.head(top_n)

def main():
    st.title("音樂情緒分類與推薦系統")

    st.markdown("""
    步驟：
    1. 上傳音訊檔（可選）或輸入歌詞文字  
    2. 系統分析歌詞與音訊情緒  
    3. 顯示情緒分類結果，並推薦同情緒歌曲  
    4. 或者直接輸入情緒，快速推薦  
    """)

    songs_df = load_songs()

    audio_file = st.file_uploader("請上傳音訊檔（mp3/wav 等，選擇性）", type=['mp3', 'wav'])
    lyrics_input = st.text_area("或直接輸入歌詞文字")

    st.markdown("---")
    st.subheader("快速輸入情緒推薦")
    user_emotion = st.text_input("或直接輸入想要搜尋的情緒（如：愉悅、悲傷、憤怒、平靜、煩躁）")

    # 音訊分析結果變數
    audio_emotion = None

    if audio_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(audio_file.read())
            tmp_path = tmp.name
        
        st.audio(tmp_path)
        st.info(f"音訊檔已暫存於：{tmp_path}")

        # 讀取音訊並分析
        try:
            y, sr = librosa.load(tmp_path, sr=None)
            audio_emotion = analyze_audio_emotion(y, sr)
            st.success(f"音訊分析預測情緒：**{audio_emotion}**")
        except Exception as e:
            st.error(f"音訊分析失敗: {e}")

    # 按鈕：分析歌詞情緒並綜合推薦
    if st.button("分析歌詞情緒並推薦"):
        if not lyrics_input.strip():
            st.warning("請先輸入歌詞文字！")
        else:
            lyrics_emotion = analyze_lyrics_emotion(lyrics_input)
            st.success(f"歌詞情緒判斷為：**{lyrics_emotion}**")

            # 綜合判斷
            if audio_emotion:
                st.info(f"結合音訊情緒：**{audio_emotion}**")
                # 兩者簡單合併：若一致，使用該情緒，不同則標示「混合情緒」
                if lyrics_emotion == audio_emotion:
                    final_emotion = lyrics_emotion
                else:
                    final_emotion = f"{lyrics_emotion} / {audio_emotion}"
                st.success(f"綜合判斷情緒：**{final_emotion}**")
                recs = recommend_songs(songs_df, lyrics_emotion)  # 以歌詞情緒推薦，或可改用 final_emotion
            else:
                final_emotion = lyrics_emotion
                recs = recommend_songs(songs_df, lyrics_emotion)

            if not recs.empty:
                st.markdown("### 推薦相同情緒歌曲：")
                for _, row in recs.iterrows():
                    st.write(f"- {row['title']} by {row['artist']} [{row['genre']}]")
            else:
                st.info("找不到符合該情緒的歌曲。")

    # 直接輸入情緒推薦按鈕
    if st.button("直接推薦該情緒歌曲"):
        if not user_emotion.strip():
            st.warning("請輸入欲搜尋的情緒！")
        else:
            recs = recommend_songs(songs_df, user_emotion)
            if not recs.empty:
                st.markdown(f"### 推薦情緒為 **{user_emotion}** 的歌曲：")
                for _, row in recs.iterrows():
                    st.write(f"- {row['title']} by {row['artist']} [{row['genre']}]")
            else:
                st.info("找不到符合該情緒的歌曲。")

if __name__ == "__main__":
    main()
