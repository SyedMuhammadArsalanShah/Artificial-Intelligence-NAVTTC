from bs4 import BeautifulSoup
import json

# === Step 1: HTML file path ===
file_path = "profile_posts_1.html"  # change to your actual file

# === Step 2: Read the HTML content ===
with open(file_path, "r", encoding="utf-8") as file:
    html = file.read()

# === Step 3: Parse HTML using built-in parser ===
soup = BeautifulSoup(html, "html.parser")

# === Step 4: Find all posts by class ===
posts = soup.find_all("div", class_="_2pin")

# === Step 5: Extract post data ===
data = []
count=0
for post in posts:
    text = post.get_text(strip=True)
    count=count+1
    data.append({
        "post": count,
        "content": text
    })

# === Step 6: Save to JSON file ===
with open("facebook_posts.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

print(f"✅ Extracted {len(data)} posts and saved to facebook_posts.json")
