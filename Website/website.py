#!/usr/bin/env python3

from flask import Flask
from DataViews.pages import pages
from DataViews.database_gather import data
from DataBase import get_clients, new_weekly_report
from threading import Thread
import schedule, time

app = Flask(__name__)
app.register_blueprint(pages, url_prefix="/")
app.register_blueprint(data, url_prefix="/Database")


def weekly_reports():
    def new_report():
        get_clients()
        new_weekly_report()

    schedule.every().friday.at("01:00").do(new_report)
    schedule.run_pending()
    time.sleep(43200)

    
if __name__ == "__main__":
    Thread(target=weekly_reports).start()
    app.run(host="0.0.0.0", port=8000, debug=True)
