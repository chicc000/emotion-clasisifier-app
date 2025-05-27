import csv

def load_songs(csv_file):
    songs = []
    with open(csv_file, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 確保每筆資料有 emotion 欄位，沒有就設空字串
            if 'emotion' not in row:
                row['emotion'] = ''
            songs.append(row)
    return songs

def filter_songs_by_emotion(songs, emotion):
    return [song for song in songs if song['emotion'] == emotion]

def main():
    csv_file = "songs.csv"  # 確認你的檔案名稱
    songs = load_songs(csv_file)

    print("請輸入您想搜尋的情緒（例如：愉悅、悲傷、憤怒、平靜、煩躁）或自訂情緒：")
    user_emotion = input().strip()

    filtered = filter_songs_by_emotion(songs, user_emotion)

    if not filtered:
        print(f"抱歉，找不到情緒為『{user_emotion}』的歌曲。")
    else:
        print(f"情緒為『{user_emotion}』的歌曲清單：")
        for s in filtered:
            print(f" - {s['title']} by {s['artist']} [{s.get('genre','未知曲風')}]")

if __name__ == "__main__":
    main()
