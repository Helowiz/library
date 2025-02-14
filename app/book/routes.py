from flask import render_template, request, url_for, redirect
from app.book import bp
from app.models.db.select import select_all_from_table

@bp.route("/")
def index():
    books = select_all_from_table("Books")
    print(books)
    return render_template("book/index.html", books=books)


@bp.route("/add/", methods=("GET", "POST"))
def add():
    if request.method == "POST":

        return redirect(url_for("book.index"))

    return render_template("book/add.html")


@bp.route("/delete/")
def delete():
    return render_template("book/delete.html")


@bp.route("/update/")
def update():
    return render_template("book/update.html")
