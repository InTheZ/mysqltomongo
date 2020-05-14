import configparser

from flask import Flask, jsonify, request

import mongo
import util

app = Flask(__name__)

DEFAULT_CONFIG = "consumer.conf"

def startup():
    # Read configuration
    config = configparser.ConfigParser()
    config.read(DEFAULT_CONFIG)

    # Create necessary database connections to use
    mongo.createConnection(config)

def shutdown():
    # Create necessary database connections to use
    mongo.close()

@app.route('/report_data', methods=['POST'])
def receiveData():
    doc = util.parseDocument(request.get_json())
    mongo.insertDoc(doc)
    return '', 204

if __name__ == "__main__":
    startup()
    app.run()
    shutdown()