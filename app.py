# =============================================================================
# imports
# =============================================================================

import os
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

# =============================================================================
# constants
# =============================================================================

app = Flask(__name__)

api_data = None

# =============================================================================
# routes
# =============================================================================

@app.route("/")
def index():
   print("Request for index page received")
   return render_template("index.html")

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico", mimetype="image/vnd.microsoft.icon"
    )

@app.route("/hello", methods=["POST"])
def hello():
   name = request.form.get("name")

   if name:
       print("Request for hello page received with name=%s" % name)
       return render_template("hello.html", name = name)
   else:
       print("Request for hello page received with no name or blank name -- redirecting")
       return redirect(url_for("index"))

@app.route("/webhook/payload", methods=["POST"])
def webhook_payload():
    if request.method != "POST":
        return "POST only"
    global api_data
    api_data = request.get_data(as_text=True)
    return api_data

@app.route("/webhook/data", methods=["GET"])
def webhook_data():
    global api_data
    response = app.response_class(
        response=api_data,
        status=200,
        mimetype="application/json"
    )
    return response


# =============================================================================
# main
# =============================================================================

if __name__=="__main__":
    app.debug = True
    app.run()
