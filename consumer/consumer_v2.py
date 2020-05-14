import configparser

from flask import Flask, jsonify, request

import mysql
import mongo
import util

app = Flask(__name__)

DEFAULT_CONFIG = "consumer.conf"

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

@app.route('/report_data', methods=['POST'])
def receiveData():
    doc = util.parseDocument(request.get_json())
    mysql.insertDoc(doc)
    mysql.commit()
    mongo.insertDoc(doc)
    return '', 204

if __name__ == "__main__":
    startup()
    app.run()
    shutdown()