from DataBase import *
from flask import Blueprint, request, redirect, render_template, send_file

data = Blueprint("data", __name__)
Submitted = {}

@data.route("/submit", methods=['POST'])
def submit_data():
    global Submitted

    App = False
    Grub = False
    BL = False

    if request.form.get("App"):
        App = True
    if request.form.get("Grub"):
        Grub = True
    if request.form.get("BL"):
        BL = True

    result = None

    for items in request.form.getlist("client"):

        Submitted = {
            "Client": items,
            "App": App,
            "Grub": Grub,
            "BL": BL
        }

        holder = add_data(Submitted)

        if holder is not None and result is None:
            result = []
            result.append(holder)
        elif holder is not None and result is not None:
            result.append(holder)

    if not result:
        return redirect("/", code=302, Response=None)
    else:
        if result in ["App", "Grub", "BL"]:
            return render_template("Service_Error.html", result=result)
        else:
            return render_template("Generic_Error.html")


@data.route("/get-clients")
def gather_clients():
    return get_clients()


@data.route("/get-services")
def gather_services():
    pass
