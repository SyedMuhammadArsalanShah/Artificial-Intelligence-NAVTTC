from bs4 import BeautifulSoup
import json

file_path = "fbpost.html"

with open(file_path, "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")
posts = soup.find_all("div", class_="_2pin")

data = []
for idx, post in enumerate(posts, start=1):
    data.append({"post": idx, "content": post.get_text(strip=True)})

with open("facebook_posts.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Extracted {len(data)} posts")