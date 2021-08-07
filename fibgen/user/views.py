# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, current_app, render_template, request
from flask.helpers import url_for
from flask_login import login_required
from werkzeug.utils import redirect


from fibgen.books import scrape, download_book

from .forms import LibgenForm

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")

books = []


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def members():
    """List members."""
    global books
    form = LibgenForm(request.form)
    books = []
    if request.method == "POST":
        books = scrape(form.book.data)
        current_app.logger.info(books[0].links[0])

    return render_template(
        "users/members.html", title="Search book", form=form, books=books
    )


@blueprint.route("/download/<int:book_no>")
@login_required
def download(book_no):
    global books
    current_app.logger.info(f"downloading book {books[book_no]}")
    current_app.logger.info(books[book_no].links[0])
    download_book(books[book_no].links[0], dest=f"/watch/")
    return redirect(url_for(".members"))
