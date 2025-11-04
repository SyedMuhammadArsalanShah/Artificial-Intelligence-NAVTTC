import requests
from bs4 import BeautifulSoup
import json 





url="https://sunnah.com/hisn"


response = requests.get(url)


html_content =response.content


# print(html_content)


soup=BeautifulSoup(html_content, 'html.parser')

sorted_hadiths={}

chapters  = soup.find_all('div', class_="chapter")


print(chapters)
for chapter in chapters:
    chapter_number = chapter.find('div', class_='echapno').text.strip()
    chapter_title = chapter.find('div', class_='englishchapter').text.strip()
    arabic_chapter = chapter.find('div', class_='arabicchapter').text.strip()
    if chapter_number not in sorted_hadiths:
        sorted_hadiths[chapter_number] = {
            'chapter_title': chapter_title,
            'arabic_chapter': arabic_chapter,
            'hadiths': []
        }

    hadith_containers = chapter.find_next_siblings('div', class_='actualHadithContainer')
    for hadith in hadith_containers:
        english_hadith = hadith.find('div', class_='english_hadith_full')
        arabic_hadith = hadith.find('div', class_='arabic_hadith_full arabic')
        transliteration = hadith.find('span', class_='transliteration')
        reference = hadith.find('span', class_='hisn_english_reference')

        # Safely extract text if element exists
        english_text = english_hadith.find('span', class_='translation').text.strip() if english_hadith and english_hadith.find('span', class_='translation') else None
        arabic_text = arabic_hadith.find('span', class_='arabic_text_details arabic').text.strip() if arabic_hadith and arabic_hadith.find('span', class_='arabic_text_details arabic') else None
        transliteration_text = transliteration.text.strip() if transliteration else None
        reference_text = reference.text.strip() if reference else None

        if english_text and arabic_text and transliteration_text and reference_text:
            sorted_hadiths[chapter_number]['hadiths'].append({
                'arabic_hadith': arabic_text,
                'english_hadith': english_text,
                'transliteration': transliteration_text,
                'reference': reference_text
            })

# Step 4: Save sorted Hadiths to JSON
with open('hisn_ul_muslim.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_hadiths, f, ensure_ascii=False, indent=4)

print("Hadiths sorted by chapter with transliteration saved to sorted_hadiths_by_chapter_with_transliteration.json")







