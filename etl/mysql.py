import datetime

import pymysql.cursors

conn = None
def createConnection(config):
    global conn
    conn =  pymysql.connect(
        host=config["MySQL"]["Host"],
        port=int(config["MySQL"]["Port"]),
        user=config["MySQL"]["User"],
        password=config["MySQL"]["Pass"],
        db=config["MySQL"]["Database"],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

def close():
    conn.close()

def findOlder(date):
    sql = """
    SELECT
        COUNT(*) AS count
    FROM
        files
    WHERE
        created < %s"""
    openCursor = conn.cursor()
    openCursor.execute(sql, date)
    count = openCursor.fetchone()
    openCursor.close()
    return int(count['count'])

curCursor = None
def getFirstDoc(date):
    global conn, curCursor
    # Query for files / patients
    sql = """
    SELECT 
        files.fileId as fileId,
        files.created as created,
        patients.patientId as patientId,
        patients.name as name,
        patients.address as address,
        patients.city as city,
        patients.state as state,
        patients.zip as zip,
        patients.id as pId
    FROM 
        files
    LEFT JOIN
        (patients)
    ON
        (patients.fileId=files.id)
    WHERE 
        files.created<%s
    ORDER BY 
        created DESC"""
    curCursor = conn.cursor()
    curCursor.execute(sql, date)
    res = curCursor.fetchone()
    if None != res:
        services = findServices(res["pId"])
        return {
            "fileId": res["fileId"],
            "created": res["created"],
            "patient": {
                "name": res["name"],
                "address": res["address"],
                "city": res["city"],
                "state": res["state"],
                "zip": res["zip"]
            },
            "services": services
        }

def getNextDoc():
    global curCursor
    res = curCursor.fetchone()
    if None != res:
        services = findServices(res["pId"])
        return {
            "fileId": res["fileId"],
            "created": res["created"],
            "patient": {
                "name": res["name"],
                "address": res["address"],
                "city": res["city"],
                "state": res["state"],
                "zip": res["zip"]
            },
            "services": services
        }

def findServices(pId):
    global conn
    # Query for services
    sql = """
    SELECT 
        date,
        name,
        code,
        description,
        cost
    FROM 
        services
    WHERE 
        pId=%s
    ORDER BY 
        date"""
    openCursor = conn.cursor()
    openCursor.execute(sql, pId)
    res = openCursor.fetchone()
    services = []
    while res != None:
        services.append({
            "date": res["date"],
            "name": res["name"],
            "code": res["code"],
            "description": res["description"],
            "cost": float(res["cost"])
        })
        res = openCursor.fetchone()
    return services
