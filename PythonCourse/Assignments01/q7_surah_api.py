# Q7: Fetch Surah 1 name using requests
import requests

url = "https://api.alquran.cloud/v1/surah/1"
response = requests.get(url)
data = response.json()

print("Surah Name:", data["data"]["englishName"])
