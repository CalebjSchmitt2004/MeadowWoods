#!/usr/bin/env python3

from flask import Flask
from DataViews.pages import pages
from DataViews.database_gather import data

app = Flask(__name__)
app.register_blueprint(pages, url_prefix="/")
app.register_blueprint(data, url_prefix="/Database")

if __name__ == "__main__":
    app.run(port=8000, debug=True)
