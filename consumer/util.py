import datetime

def parseDocument(doc):
    services = []
    for i in doc["services"]:
        services.append({
            "date": datetime.datetime.strptime(i["date"], "%m/%d/%Y %I:%M %p"),
            "name": i["name"],
            "code": i["code"],
            "description": i["description"],
            "cost": i["cost"]
        })
    
    newDoc = {
            "patient": {
                "patientId": doc["patient"]["patientId"],
                "name": doc["patient"]["name"],
                "address": doc["patient"]["address"],
                "city": doc["patient"]["city"],
                "state": doc["patient"]["state"],
                "zip": doc["patient"]["zip"]
        },
        "created": datetime.datetime.strptime(doc["created"], "%Y-%m-%d %H:%M:%S"),
        "services": services,
        "fileId": int(doc["fileId"])
    }
    return newDoc