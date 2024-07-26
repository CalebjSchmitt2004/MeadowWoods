import gspread

connector = gspread.service_account("../../key.json")
DataBase = connector.open("Fertilizer List").get_worksheet(0)
Data_Flags = ["", "NAME", "Prepay letter"]
raw_client_list = []


def get_clients():
    global raw_client_list

    raw_client_list = DataBase.col_values(1)
    client_list = []

    for clients in raw_client_list:
        if clients not in Data_Flags:
            client_list.append(clients)

    return client_list


def get_services():
    global raw_service_list

    raw_service_list = DataBase.row_values(2)
    service_list = []

    for services in raw_service_list:
        if services not in Data_Flags and services not in service_list:
            service_list.append(services)

    return service_list


def add_data():
    pass


if __name__ == "__main__":
    print(get_clients())
    print(get_services())
