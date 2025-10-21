from flask import Flask, jsonify, render_template, request, url_for
import requests

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_world():
    return render_template("index.html")


@app.route("/api/save/", methods=["POST", "GET"])
def saveapi():
    if request.method == "POST":
        username = request.form["username"]
        useremail = request.form["useremail"]
        userpassword = request.form["userpassword"]

        response_Data = {
            "user": username,
            "useremail": useremail,
            "userpass": userpassword,
        }
        return jsonify(response_Data)
    return jsonify({})


app.run(debug=True)
