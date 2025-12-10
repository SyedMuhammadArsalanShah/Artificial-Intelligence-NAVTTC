

# **Project: Flask CRUD App with PostgreSQL + Docker**

## **1. Why Docker is Necessary**

* **Environment consistency:** Ensures the app runs the same locally, on Railway, or any cloud.
* **Dependency management:** No need to install Python, PostgreSQL, or libraries manually on the server.
* **Isolation:** Each service (Python app, PostgreSQL) runs in its own container.
* **Ease of deployment:** With `docker-compose.yml`, one command can start everything.
* **Persistence & networking:** Containers can communicate securely and database persists with volumes.

---

## **2. Project Folder Structure**

```
docker_flask_crud_app/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── init.sql
├── .dockerignore
└── README.md
```

---

## **3. init.sql** – Initialize PostgreSQL with sample data

```sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

INSERT INTO users (name, email) VALUES
('Nawaira', 'nawaira@example.com'),
('Laiba', 'laiba@example.com'),
('Mufti Sahab', 'muftisahab@example.com'),
('Usman FAV Student', 'usman@example.com');
```

---

## **4. requirements.txt**

```
Flask==2.3.0
psycopg2-binary==2.9.9
```

---

## **5. Dockerfile**

```dockerfile
# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]
```

---

## **6. .dockerignore**

```
__pycache__
*.pyc
*.pyo
*.pyd
*.db
.env
```

---

## **7. docker-compose.yml** – Python + PostgreSQL setup

```yaml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - db
    environment:
      DB_HOST: db
      DB_NAME: mydb
      DB_USER: myuser
      DB_PASSWORD: mypassword

  db:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  pgdata:
```

---

## **8. app.py** – Full CRUD API

```
from flask import Flask, jsonify, request
import psycopg2
import os
import time
from urllib.parse import urlparse

app = Flask(__name__)

# Get DATABASE_URL from environment (Railway provides it automatically)
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set!")

# Parse DATABASE_URL
result = urlparse(DATABASE_URL)
db_name = result.path[1:]  # remove leading '/'
db_user = result.username
db_password = result.password
db_host = result.hostname
db_port = result.port or 5432

# Retry DB connection until it succeeds
while True:
    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        print("Connected to PostgreSQL successfully!")
        break
    except Exception as e:
        print(f"Waiting for DB to start... ({e})")
        time.sleep(2)

# Initialize DB (create table if it doesn't exist)
def init_db():
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE
    );
    """)
    conn.commit()
    cur.close()
    print("Database initialized successfully!")

init_db()

# -------------------------
# CRUD routes
# -------------------------

# Get all users
@app.route("/users", methods=["GET"])
def get_users():
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM users;")
    users = cur.fetchall()
    cur.close()
    return jsonify([{"id": u[0], "name": u[1], "email": u[2]} for u in users])

# Get single user
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM users WHERE id=%s;", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return jsonify({"id": user[0], "name": user[1], "email": user[2]})
    return jsonify({"error": "User not found"}), 404

# Create new user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;",
                (data["name"], data["email"]))
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return jsonify({"id": user_id, "name": data["name"], "email": data["email"]}), 201

# Update user
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    cur = conn.cursor()
    cur.execute("UPDATE users SET name=%s, email=%s WHERE id=%s RETURNING id;",
                (data["name"], data["email"], user_id))
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    if updated:
        return jsonify({"id": user_id, "name": data["name"], "email": data["email"]})
    return jsonify({"error": "User not found"}), 404

# Delete user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=%s RETURNING id;", (user_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    if deleted:
        return jsonify({"message": f"User {user_id} deleted"})
    return jsonify({"error": "User not found"}), 404

# -------------------------
# Run Flask app
# -------------------------
if __name__ == "__main__":
    # Railway uses dynamic PORT
    port = int(os.environ.get("PORT", 5000))
    # Disable strict slash matching
    app.url_map.strict_slashes = False
    app.run(host="0.0.0.0", port=port)
```
---

## **9. Run Project Locally with Docker**

1. **Build & start containers:**

```bash
docker-compose up --build
```

2. **Test Endpoints (Postman / Browser):**

* `GET /users` → list all users
* `GET /users/1` → get user with ID 1
* `POST /users` → create user with JSON body:

```json
{"name":"David","email":"david@example.com"}
```

* `PUT /users/1` → update user 1:

```json
{"name":"Alice Updated","email":"alice_new@example.com"}
```

* `DELETE /users/1` → delete user 1

3. **Stop containers:**

```bash
docker-compose down
```

---

## **10. Deploy on Railway**


### **Step 1 — Upload Your Project to GitHub**

All files including Dockerfile & docker-compose.yml.

### **Step 2 — Create New Railway Project**

Go to:
[https://railway.app](https://railway.app)

Click:

* New Project
* Deploy from GitHub

Railway auto-detects Dockerfile.

### **Step 3 — Add PostgreSQL**

Add → PostgreSQL
Railway creates a cloud database.

### **Step 4 — Add Environment Variables**

In Railway → Variables:

If using Railway Postgres URL, set it like this:

```
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

### **Step 5 — Deploy**

Railway builds the Docker image and starts your Flask server.

### **Step 6 — Test API**

Open:

```
https://your-app.up.railway.app/users
```

---



# **Visual Diagram & Explanation: Flask CRUD App on Docker + Railway**

```
                ┌───────────────────────┐
                │     User / Client      │
                │ (Browser / Postman)   │
                └─────────┬─────────────┘
                          │ HTTP Requests (GET, POST, PUT, DELETE)
                          │
                          ▼
                ┌───────────────────────┐
                │   Railway Hosted App   │
                │   Docker Environment  │
                └─────────┬─────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
        ▼                                   ▼
┌─────────────────────┐           ┌─────────────────────┐
│   Python Flask App  │           │   PostgreSQL DB     │
│  (web container)    │           │  (db container)     │
│  Port: 5000         │           │  Port: 5432         │
└─────────┬───────────┘           └─────────┬───────────┘
          │ CRUD Operations                │ Database Storage
          │ Queries / Transactions         │ (persistent volume)
          │                                 │
          ▼                                 ▼
    Responds with JSON                   Data stored persistently
```

---

## **Step-by-Step Flow**

1. **User sends request** via browser or Postman to Railway app (e.g., `GET /users`).
2. **Flask app container** inside Docker receives the request.
3. Flask app **connects to PostgreSQL container** using internal Docker networking (`DB_HOST=db`).
4. Flask executes SQL queries (`SELECT`, `INSERT`, `UPDATE`, `DELETE`).
5. PostgreSQL container responds with results.
6. Flask container formats data as **JSON** and sends back to user.
7. **Database persists data** in Docker volume, so even if containers restart, data is saved.

---

## **Why This Works Smoothly on Railway**

* Railway **supports Docker deployments**, so you push your repo with `Dockerfile` (and optionally `docker-compose.yml`).
* Docker ensures **your Python app + PostgreSQL run in isolated, consistent environments**.
* Environment variables in Railway configure DB connection dynamically without hardcoding credentials.
* Multiple services (web + db) can run in the same project with proper **networking inside Docker**.

---

## **Benefits of This Setup**

* Easy deployment anywhere without installing Python or PostgreSQL manually.
* Fully **portable**: local development mirrors production.
* Multiple developers can work on the project without dependency issues.
* CRUD API ready for extensions (e.g., authentication, frontend).

---

<img width="1024" height="1536" alt="Visual Flow" src="https://github.com/user-attachments/assets/af059a06-9194-4faf-8b7e-a33c67691145" />
