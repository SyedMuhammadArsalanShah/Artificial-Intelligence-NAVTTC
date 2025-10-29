from flask import Flask, jsonify, render_template ,request

app = Flask(__name__)

@app.route("/" ,methods=["POST", "GET"])
def hello_world():
    email="Guest Email "
    password="Guest Password"
    congrats="<p>thanks for submitting</p>"
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        return render_template("index.html", emailaddress=email,passw=password,tag=congrats)
    return render_template("index.html", emailaddress=email,passw=password)




@app.route("/signup/api/")
def about():
    return render_template("about.html")



@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/home")
def home():
    return "<p>Hello, Home!</p>"


app.run(debug=True)