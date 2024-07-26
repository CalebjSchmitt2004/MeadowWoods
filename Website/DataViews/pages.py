from flask import Blueprint, render_template

pages = Blueprint("pages", __name__)


@pages.route("/")
def UserDataInput():
    return render_template("base.html")
