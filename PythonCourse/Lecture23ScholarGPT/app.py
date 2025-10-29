import os
from flask import Flask, render_template, request
from core.pipeline import run_chatbot

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    answer = None
    if request.method == "POST":
        question = request.form["question"]
        answer = run_chatbot(question)
    return render_template("index.html", answer=answer)

if __name__ == "__main__":
    # app.run(debug=True)
    # for hosting ----
    # Render assigns PORT=10000 by default
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
