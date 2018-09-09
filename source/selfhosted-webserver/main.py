from flask import Flask, render_template, redirect

app = Flask(__name__)
app.config["SERVER_NAME"] = "simonjenner.gq"

@app.route("/")
def mainpage():
    return render_template("index.html")