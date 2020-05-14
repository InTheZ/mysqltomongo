import pymongo

conn = None
database = None
collection = None

def createConnection(config):
    global conn, database, collection
    conn = pymongo.MongoClient(config["Mongo"]["MongoURI"])
    collection = config["Mongo"]["Collection"]
    database = config["Mongo"]["Database"]

def close():
    global conn
    conn.close()

def findOldest():
    global conn, database, collection
    return list(conn[database][collection].find().sort([("created", pymongo.ASCENDING)]).limit(1))[0]["created"]

def insertDoc(doc):
    global conn, database, collection
    # Insert document into collection
    conn[database][collection].insert_one(doc)
