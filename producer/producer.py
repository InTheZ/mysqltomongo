import configparser
import datetime
import json
import requests
import time

import util

QUEUE = []
DEFAULT_CONFIG = "producer.conf"

def genData():
    services = []
    for i in range(0,util.randomInt(2)):
        services.append({
            "date": util.randomDate(afterDate="03/01/2020 8:00 AM",toDate="05/15/2020 05:00 PM"),
            "name": util.randomString(util.randomInt(2)),
            "code": util.randomInt(4),
            "description": util.randomString(util.randomInt(3)),
            "cost": round(util.randomMoney(min=100.00, max=900.00), 2)
        })
    return {
        "patient": {
            "patientId": util.randomInt(12),
            "name": util.generateName(),
            "address": util.randomStreetAddress(),
            "city": util.randomCity(),
            "state": util.randomState(),
            "zip": util.randomZipCode()
        },
        "fileId": util.randomInt(6),
        "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "services": services
    }

def produceData(conf):
    endpoint = conf["GENERAL"]["Endpoint"]
    interval = int(conf["GENERAL"]["Interval"])
    batch = int(conf["GENERAL"]["Batch"])
    while True:
        for i in range(0,batch):
            QUEUE.append(genData())
        error = False
        while len(QUEUE)>0 and not error:
            item = QUEUE.pop()
            try:
                requests.post(endpoint, data=json.dumps(item), headers={"Content-Type": "application/json"})
            except Exception as e:
                # Issue connecting to server, put this item back in the queue
                QUEUE.append(item)
                error = True
                pass
        
        # Wait the interval until we try again
        print("Current Queue Length: " + str(len(QUEUE)))
        time.sleep(interval)

def main():
    # Read configuration
    config = configparser.ConfigParser()
    config.read(DEFAULT_CONFIG)
    produceData(config)

if __name__ == "__main__":
    main()