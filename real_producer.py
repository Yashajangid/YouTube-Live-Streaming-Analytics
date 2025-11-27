import pandas as pd
import requests
import time

file_path = 'C:\Users\Dell\Downloads\USvideos.csv'  # update this path if needed

print("📥 Loading YouTube data from local CSV...")
df = pd.read_csv(r"C:\Users\DELL\Downloads\archive (8)\USvideos.csv")

youtube_data = df[['video_id', 'title', 'views', 'likes', 'dislikes']].head(20).to_dict('records')

print(f"🚀 Streaming {len(youtube_data)} YouTube videos!")

for msg in youtube_data:
    requests.post('http://localhost:5000/send', json=msg)
    print(f"📤 REAL: {msg['title'][:40]} | Views: {msg['views']:,}")
    time.sleep(1)

print("🎉 Streaming COMPLETE!")