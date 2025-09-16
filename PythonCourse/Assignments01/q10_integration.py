# Q10: Integration – Fetch Surah by number & play audio surah 

import requests
from playsound import playsound
surahNum= int(input("Enter Your Surah Number "))

response= requests.get(f"https://api.alquran.cloud/v1/surah/{surahNum}/ar.alafasy")

if response.status_code==200:
    surah_data=response.json()["data"]
    # Fetch Surah name
    print(surah_data["englishName"])
    
    audioVerses=surah_data["ayahs"]
    for i in audioVerses:
        # Play audio verses
        playsound(i["audio"])