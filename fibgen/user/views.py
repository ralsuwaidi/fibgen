# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, current_app, render_template, request
from flask_login import login_required

from fibgen.books import scrape

from .forms import LibgenForm

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def members():
    """List members."""
    form = LibgenForm(request.form)
    books = []
    if request.method == "POST":
        books = scrape(form.book.data)
        current_app.logger.info(books[0])

    return render_template(
        "users/members.html", title="Search book", form=form, books=books
    )
