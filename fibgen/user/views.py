# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, current_app, render_template, request
from flask.helpers import flash, url_for
from flask_login import login_required
from werkzeug.utils import redirect

from fibgen.books import download_book, scrape

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
        if len(books) != 0:
            current_app.logger.info("found {} books".format(len(books)))
        else:
            current_app.logger.info("couldnt find any books")
            flash("Couldnt find any books", category="warning")

    return render_template(
        "users/members.html", title="Search book", form=form, books=books
    )


@blueprint.route("/download/<int:book_no>")
@login_required
def download(book_no):
    global books
    current_app.logger.info(
        f"downloading book {books[book_no]} with link {books[book_no].links}"
    )
    download_book(books[book_no].links, dest=f"/watch/")
    flash(f"Successfully downloaded {books[book_no]}", category="success")
    return redirect(url_for(".members"))
