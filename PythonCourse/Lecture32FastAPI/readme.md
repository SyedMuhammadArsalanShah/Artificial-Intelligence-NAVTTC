
# FastAPI + Firebase CRUD Project

**Author:** Syed Muhammad Arsalan Shah  
**Repository:** [https://github.com/SyedMuhammadArsalanShah/FastAPI](https://github.com/SyedMuhammadArsalanShah/FastAPI)

---

## Project Overview

This repository demonstrates **FastAPI CRUD applications** in **three progressive stages**, suitable for learning and production-ready use cases:

1. **Stage 1 – FastAPI without Database:**  
   - Uses in-memory Python data structures (list/dict).  
   - Focuses on learning FastAPI routing and CRUD logic.

2. **Stage 2 – FastAPI with Firebase Firestore:**  
   - Backend connected to **Firebase Firestore**.  
   - Implements real database CRUD operations.  
   - Demonstrates API design, input validation, and secure data handling.

3. **Stage 3 – FastAPI + Firebase + Server-Side Rendered Web (No JS):**  
   - Fully HTML form-based web interface using **Jinja2 templates**.  
   - No JavaScript required; server handles all CRUD operations.  
   - Safe, modular, and beginner-friendly structure.

---

## Features

- Clean FastAPI architecture
- Progressive learning from in-memory to database-backed API
- Server-side rendered forms (no JS)
- Firebase Firestore integration
- Modular and scalable for future enhancements
- Beginner-friendly with clear project structure

---

## Project Structure



FastAPI/
│
├── stage1-no-db/
│   ├── main.py
│   └── models.py
│
├── stage2-firebase/
│   ├── main.py
│   ├── database.py
│   └── models.py
│
└── stage3-web-no-js/
├── main.py
├── database.py
├── models.py
└── templates/
├── index.html
├── add_item.html
└── edit_item.html


---

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/SyedMuhammadArsalanShah/FastAPI.git
cd FastAPI
````

2. **Create a virtual environment and install dependencies**

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows
pip install fastapi uvicorn firebase-admin jinja2 python-multipart
```

3. **Firebase Setup (for Stage 2 & 3)**

   * Create a Firebase project
   * Enable Firestore and create a `items` collection
   * Download the Service Account JSON file and save it as `serviceAccount.json` in the project root

---

## Running the Application

* **Stage 1 (No DB)**

```bash
uvicorn stage1-no-db.main:app --reload
```

* **Stage 2 (Firebase API)**

```bash
uvicorn stage2-firebase.main:app --reload
```

* **Stage 3 (Web Forms, No JS)**

```bash
uvicorn stage3-web-no-js.main:app --reload
```

* **Access**

  * Stage 1 & 2 APIs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
  * Stage 3 Web UI: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Why FastAPI + Firebase

* Secure backend: Firebase keys are not exposed to client
* Supports server-side rendering (HTML forms) without JS
* Input validation and business logic handled server-side
* Scalable and modular architecture for future enhancements

---

## Contributing

* Fork the repository and create a new branch for features or bug fixes
* Follow **PEP8** coding standards
* Submit a pull request with clear description

---

## License

MIT License

---

## Contact

**Syed Muhammad Arsalan Shah**
GitHub: [SyedMuhammadArsalanShah](https://github.com/SyedMuhammadArsalanShah)

