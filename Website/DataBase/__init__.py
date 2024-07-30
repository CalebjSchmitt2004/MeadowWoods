import datetime
from datetime import date, timedelta
import gspread
import json

connector = gspread.service_account("./Website/key.json")
data_writer = gspread.service_account("./Website/writer1.json")
DataBase = connector.open("Fertilizer List").get_worksheet(0)
Data_Flags = ["", "NAME", "Prepay letter"]
raw_client_list = []

Formatting_List = {
    "App 1": 3,
    "App 2": 4,
    "Grub": 6,
    "App 3": 7,
    "App 4": 8,
    "App 5": 9,
    "BL 1": 10,
    "BL 2": 12
}


def get_clients():
    global raw_client_list

    raw_client_list = DataBase.col_values(1)
    client_list = []

    for clients in raw_client_list:
        if clients not in Data_Flags:
            client_list.append(clients)

    return json.dumps(client_list)


def get_services(client):
    global raw_service_list

    row = raw_client_list.index(client)
    raw_service_list = list(DataBase.row_values(row+1))

    while len(raw_service_list) != 12:
        raw_service_list.append("")

    print(raw_service_list)

    App = 0
    Grub = 0
    BL = 0

    for items in range(len(raw_service_list)):
        if not raw_service_list[items] and items in [2, 3, 6, 7, 8] and App == 0:
            App = items+1
        elif not raw_service_list[items] and items in [5] and Grub == 0:
            Grub = items+1
        elif not raw_service_list[items] and items in [9, 11] and BL == 0:
            BL = items+1

    FormData = {
        "Client Row": row + 1,
        "App": App,
        "Grub": Grub,
        "BL": BL
    }

    return FormData


def add_data(Data):
    service = get_services(Data["Client"])

    print(Data)
    print(service)

    for items in Data:
        if Data[items] and items != "Client":
            if service[items] != 0:
                print(f"{items} : {service[items]}")

                today = date.today()
                submitted_value = f"{today.month}/{today.day}"
                DataBase.update_cell(service["Client Row"], service[items], submitted_value)
            else:
                print(f"ERROR: Unable to apply product: {items}")
                return items


def new_weekly_report():
    def previous_week_range(date):
        start_date = date + timedelta(-date.weekday())
        return [f"{start_date.month}/{start_date.day} - {date.today().month}/{date.today().day}", start_date]

    def create_title(report):
        y_val = 1
        report.update_cell(y_val, 1, "NAME")
        report.update_cell(y_val, 3, "1ST APP")
        report.update_cell(y_val, 4, "2ND APP")
        report.update_cell(y_val, 5, "GRUB")
        report.update_cell(y_val, 6, "3RD APP")
        report.update_cell(y_val, 7, "4TH")
        report.update_cell(y_val, 8, "5TH")
        report.update_cell(y_val, 9, "#1 BL")
        report.update_cell(y_val, 10, "#1 BL")
        report.update_cell(y_val, 11, "#2 BL")

    def populate_data(report, week):
        reportWeekStart = week[1].day
        reportWeekStop = date.today().day

        reportWeek = []
        exportList = {}

        for i in range(0, 5):
            day = date.today() - datetime.timedelta(days=i)
            reportWeek.append(f"{day.month}/{day.day}")

        for days in reportWeek:
            for items in DataBase.findall(str(days)):
                if items.row not in exportList:
                    exportList[items.row] = DataBase.row_values(items.row)

        print(sorted(exportList))
        print(exportList)

        index = 2

        for items in sorted(exportList):
            for dates in range(len(exportList[items])):
                if dates == 0:
                    report.update_cell(index, 1, exportList[items][dates])
                elif exportList[items][dates] in reportWeek:
                    report.update_cell(index, dates+1, exportList[items][dates])
            index += 1

        report.format(f"C2:K{index-1}", {
            "backgroundColor": {
                "red": 40.0,
                "green": 40.0,
                "blue": 40.0
            },
            "horizontalAlignment": "CENTER",
            "textFormat": {
                "fontSize": 10,
                "bold": True
            }})
        report.format(f"A2:B{index-1}", {
            "backgroundColor": {
                "red": 40.0,
                "green": 40.0,
                "blue": 40.0
            },
            "textFormat": {
                "fontSize": 10
            }})
        report.format("A1:K1", {
            "backgroundColor": {
                "red": 238.0,
                "green": 185.0,
                "blue": 201.0
            },
            "horizontalAlignment": "CENTER",
            "textFormat": {
                "foregroundColor": {
                    "red": 1.0,
                    "green": 1.0,
                    "blue": 1.0
                },
                "fontSize": 12,
                "bold": True
            }})

    week = previous_week_range(date.today())
    connector.create(title=f"Weekly Report: {week[0]}", folder_id="1zavI3Wbq836bT9V4FGZzx7mTbE9E8fXs")
    report = connector.open(f"Weekly Report: {week[0]}").get_worksheet(0)
    writer = data_writer.open(f"Weekly Report: {week[0]}").get_worksheet(0)

    create_title(report)
    populate_data(writer, week)