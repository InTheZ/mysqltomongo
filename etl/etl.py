import configparser
from signal import signal, SIGINT
from sys import exit

import mysql
import mongo
import util

DEFAULT_CONFIG = "etl.conf"

def startup():
    # Read configuration
    config = configparser.ConfigParser()
    config.read(DEFAULT_CONFIG)

    # Create necessary database connections to use
    mysql.createConnection(config)
    mongo.createConnection(config)

def shutdown():
    # Create necessary database connections to use
    mysql.close()
    mongo.close()

def etlMain():
    # Find the oldest document inside MongoDB
    date = mongo.findOldest()

    # Determine how many documents we need to transfer
    numDocs = mysql.findOlder(date)
    transferedDocs = 0
    doc = mysql.getFirstDoc(date)
    while doc != None:
        mongo.insertDoc(doc)
        doc = mysql.getNextDoc()
        transferedDocs += 1
        util.printProgressBar(transferedDocs, numDocs)


def handler(signal_received, frame):
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    shutdown()
    exit(0)

if __name__ == "__main__":
    signal(SIGINT, handler)
    startup()
    etlMain()
    shutdown()
    print("Finished ETL Job!")