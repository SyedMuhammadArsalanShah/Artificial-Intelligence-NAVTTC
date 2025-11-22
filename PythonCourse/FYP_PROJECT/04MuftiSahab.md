
# ✅ **Personalized Learning Recommendation Engine (For Mufti Sahab)**

---

# 🎯 AI-Based Personalized Learning Resource Recommender

A hybrid machine learning recommendation system that suggests lectures, readings, and videos tailored to each student.

---

## 🌟 **Key Features**

* **Content-Based Filtering** (topic similarity)
* **Collaborative Filtering** (user behavior patterns)
* **External API Integration** (YouTube, EdX, MIT OCW)
* **User Feedback Loop** to improve recommendations
* **Insights Dashboard**
* **Database Storage** for history, favorites, preferences

---

## 🧠 **Tech Stack**

* Python
* Scikit-Learn
* FastAPI / Flask
* YouTube Data API
* SQLite / PostgreSQL

---

## 📂 **Structure**

```
/recommender_core
    content_filtering.py
    collaborative_filtering.py
    ranking_engine.py
    api_connector.py
/backend
    main.py
    routes/
    db/
```

---

## 🚀 **How It Works**

1. Student selects interests
2. System fetches content metadata
3. Content & collaborative filtering models generate recommendations
4. Ranking engine scores relevance
5. Dashboard displays recommendations
6. Student feedback improves personalization

---

## 🔧 **Setup**

```
pip install -r requirements.txt
python main.py
```

---

## 📈 **Future Scope**

* Deep Learning recommendation model
* Mobile App version
* Real-time recommendation updates
* User clusters based on behavior



