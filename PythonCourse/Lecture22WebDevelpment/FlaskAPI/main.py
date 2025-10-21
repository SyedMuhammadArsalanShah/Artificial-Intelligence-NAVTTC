from flask import Flask ,request, jsonify ,render_template

app = Flask(__name__)

@app.route("/api/predict", methods=["GET"])
def predict():
    value= request.args.get("value")
    if value is None:
        return jsonify({"error": "404 not found | missing values"})
    

    result= int(value)**2
    return jsonify({

        "input":value,
        "predicts":result
    })




@app.route("/")
def hello_world():
    name="MUK"
    return render_template("about.html",name=name)




app.run(debug=True)