from flask import Flask, render_template

app = Flask(__name__)
app.config["SERVER_NAME"] = "simonjenner.gq"

@app.route("/")
def dashboard():
    return render_template("index.html")
