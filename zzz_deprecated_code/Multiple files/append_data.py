import datetime

def append_weight(weight=[]):
    weight_list["Weight"].append(weight_data)
    weight_list["Time"].append(datetime.datetime.now().time())
    weight_list["Date"].append(datetime.datetime.now().date())
    
def append_event(cycles_str=[],event_type=[]):
    event_list["Rotation amount"].append(cycles_str)
    event_list["Type"].append(event_type)
    event_list["Time"].append(datetime.datetime.now().time())
    event_list["Date"].append(datetime.datetime.now().date())

weight_list = {
    "Weight": [],
    "Time": [],
    "Date": []
}

event_list = {
    "Rotation amount": [],
    "Type" : [],
    "Time": [],
    "Date": []
}