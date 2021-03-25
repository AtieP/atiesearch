import atexit
from flask import Flask, render_template

from db import sql_close
from admin import admin
from results import results
from register import register

app = Flask(__name__, template_folder="../templates")
app.register_blueprint(results)
app.register_blueprint(admin)

def _atexit():
    with app.app_context():
        sql_close()

atexit.register(_atexit)

@app.route("/")
def main():
    return render_template("main.html")
