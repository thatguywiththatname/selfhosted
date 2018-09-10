from flask import Flask, redirect

app = Flask(__name__)
app.config["SERVER_NAME"] = "simonjenner.gq"

@app.route("/")
def mainpage():
    # Redirect to my Github page
    return redirect("https://github.com/thatguywiththatname", code=302)
