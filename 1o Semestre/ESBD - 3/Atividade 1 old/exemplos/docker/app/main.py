from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Web App with Python Flask! (pelo Docker 🐳)\n"


app.run(host="0.0.0.0", port=80)
