from DataBase import *
from flask import Blueprint, render_template

data = Blueprint("data", __name__)


@data.route("/submit", methods=['POST'])
def submit_data():
    pass


@data.route("/get-clients")
def gather_clients():
    return get_clients()


@data.route("/get-services")
def gather_services():
    pass
