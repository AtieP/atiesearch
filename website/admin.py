from hashlib import sha256
from flask import abort, Blueprint, render_template, request
from db import sql_execute

admin = Blueprint("admin", __name__, template_folder="../templates")

@admin.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "GET":
        return render_template("admin/admin_login.html")
    else:
        if (admin_user := request.form.get("admin_user")) and (admin_password := request.form.get("admin_password")):
            user_data = sql_execute("SELECT * FROM users WHERE name = ?;", (admin_user,)).fetchone()
            if not user_data:
                return render_template("admin/admin_login.html", error_message="User does not exist")
            else:
                user_data = list(user_data)
                if sha256(admin_password.encode("utf-8")).hexdigest() != user_data[3]:
                    return render_template("admin/admin_login.html", error_message="Invalid password provided")
                if not user_data[4]:
                    return render_template("admin/admin_login.html", error_message="User is not admin")
                else:
                    return render_template("admin/admin_page.html")
        else:
            return render_template("admin/admin_login.html", error_message="Username or password not provided")
