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