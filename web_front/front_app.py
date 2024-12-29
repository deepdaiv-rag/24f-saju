from flask import (
    Flask,
    render_template,
    request,
    jsonify,
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/result")
def result():
    return render_template("result.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001, host="0.0.0.0")
