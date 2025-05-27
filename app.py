import streamlit as st
import openai

# 請先在 Streamlit Secrets 裡設定 OPENAI_API_KEY
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("歌詞情緒分析器")

lyrics = st.text_area("請輸入歌詞文本:")

if st.button("分析情緒"):
    if not lyrics.strip():
        st.warning("請輸入歌詞才能分析喔！")
    else:
        with st.spinner("AI 分析中..."):
            prompt = f"請分析以下歌詞，判斷主要情緒（愉悅、悲傷、憤怒、平靜、煩躁），並只回傳情緒詞：\n\n{lyrics}"
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0,
            )
            emotion = response.choices[0].message.content.strip()
            st.success(f"判斷結果：{emotion}")
