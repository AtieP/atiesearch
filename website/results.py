from flask import Blueprint, redirect, render_template, request
from db import sql_execute

results = Blueprint("results", __name__, template_folder="../templates")

@results.route("/search", methods=["GET"])
def sites():
    if not request.args.get("query"):
        return redirect("/")

    results = sql_execute(
        "SELECT * FROM sites WHERE title LIKE ? OR url LIKE ? OR description LIKE ?;",
        (
            f"%{request.args['query'].strip()}%",
            f"%{request.args['query'].strip()}%",
            f"%{request.args['query'].strip()}%"
        )
    ).fetchall()
    return render_template("results/sites.html", query=request.args["query"], sites=list(results))
