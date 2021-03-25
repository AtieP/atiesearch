from hashlib import sha256
from flask import Blueprint, render_template, request
from db import sql_commit, sql_execute

register = Blueprint("register", __name__, template_folder="../templates")

@register.route("/register", methods=["GET", "POST"])
def register_():
    if request.method == "GET":
        return render_template("register.html")
    
    # POST
    if not (user_name := request.form.get("user_name")) or not (user_password := request.form.get("user_password")):
        return render_template("register.html", error_message="Username or password missing")
    
    # Check if user is already registered
    user_data = sql_execute("SELECT * FROM users WHERE name = ?;", (user_name,)).fetchone()
    if user_data:
        return render_template("register.html", error_message="User is already registered!")

    sql_execute(
        "INSERT INTO users (name, password, admin) VALUES (?, ?, ?)",
        (user_name, sha256(user_password.encode("utf-8")).hexdigest(), False)
    )
    sql_commit()
    return "Success!"
