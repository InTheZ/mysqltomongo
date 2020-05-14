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
    global conn
    conn.close()

def commit():
    global conn
    conn.commit()

def insertPatient(fileId, patient):
    global conn
    sql = """
    INSERT INTO `patients` (`patientId`,`fileId`,`name`,`address`,`city`,`state`,`zip`) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    myCursor = conn.cursor()
    myCursor.execute(sql, 
        (patient["patientId"],
        fileId,
        patient["name"], 
        patient["address"], 
        patient["city"], 
        patient["state"],
        patient["zip"]
        ))
    return int(myCursor.lastrowid)

def insertFile(file):
    global conn
    sql = """
    INSERT INTO `files` (`fileId`,`created`) VALUES (%s, %s)
    """
    myCursor = conn.cursor()
    myCursor.execute(sql, 
        (file["fileId"], 
        file["created"]
        ))
    return int(myCursor.lastrowid)

def insertServices(services, fileId, pId):
    global conn
    myCursor = conn.cursor()
    for service in services:
        sql = """
        INSERT INTO `services` (`pId`,`fileId`,`date`,`name`,`code`,`description`,`cost`) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        myCursor.execute(sql, 
            (
                pId,
                fileId,
                service["date"].strftime("%Y-%m-%d %H:%M:%S"),
                service["name"],
                service["code"],
                service["description"],
                service["cost"]
            ))

def insertDoc(doc):
    global conn
    # Documents split into services, patient and file
    file = doc
    fileId = insertFile(file)
    
    patient = doc["patient"]
    patientId = insertPatient(fileId, patient)

    services = doc["services"]
    insertServices(services, fileId, patientId)

    conn.commit()
