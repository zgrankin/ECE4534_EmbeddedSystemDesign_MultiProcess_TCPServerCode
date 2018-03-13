import multiprocessing
from multiprocessing import Process, Lock
import socket
import json
import os
import random
import logging
import pymongo
from pymongo import MongoClient

client_info = "mongodb://" + "zack" + ":" + "password" + "@" + "localhost" + ":" + "27017" + "/" + "admin"
dbclient = MongoClient('localhost')
db = dbclient["team3"]

DATA_F = 'data.json'
FALSIFY_RESPONSES = False

def main():
    logging.basicConfig(level=logging.DEBUG)
    server = Server("0.0.0.0", 2000)
    db.milestone4.drop()

    try:
        logging.info("Listening")
        server.start()
    except:
        logging.exception("Unexpected exception")
    finally:
        logging.info("Shutting down")
        for process in multiprocessing.active_children():
            logging.info("Shutting down process %r", process)
            process.terminate()
            process.join()
    logging.info("All done")

def get_data_store():
    if not os.path.exists(DATA_F):
        return {}

    with open(DATA_F, 'r') as f:
        return json.load(f)



def parse(string):
    if (string[:1] != b'~'):
        return "Not a message"
    message_id = int(string[1:9], 16)
    payload_len = int(string[9:13], 16)
    payload_str = string[13:]
    payload_str = payload_str[0:-1]

    if payload_len != len(payload_str):
        return "Message length mismatch"

    payload = json.loads(payload_str.decode())
    data_type = payload.pop('Type')
    if data_type == 'Request':
        request = payload.pop('Request')
        print("Request is: ", request)
        if 'map' in request:
            data = requestMapFromDatabase(request['map']['xcoord'],request['map']['ycoord'])
            #print ("Data requested from mongodb: ", data)
        elif 'testcase' in request:
            data = requestTestcaseFromDatabase()
        elif 'BookDestination' in request:
            data = requestBookDestinationFromDatabase()
        elif 'Destination' in request:
            data = requestDestinationFromDatabase()
        elif 'BookRequest' in request:
            data = requestBookRequestFromDatabase()
        elif 'USData' in request:
            data = requestUSDataFromDatabase()
        elif 'RoverOneDone' in request:
            data = requestRoverOneDoneFromDatabase()
        elif 'LocBook' in request:
            data = requestLocBookFromDatabase(request)
        elif 'PathRequest' in request:
            data = requestPathRequestFromDatabase()
        elif 'RoverLoc2' in request:
            data = requestRetrievalLocFromDatabase()
        elif 'RoverLoc' in request:
            data = requestRoverLocFromDatabase()
        elif 'EncoderTicks' in request:
            data = requestEncoderTicksFromDatabase()
        elif 'ZackNav' in request:
            data = requestZackNavFromDatabase()
        data = str(data)
        if data is None or data == "None":
            return "Requested JSON object not found"

        len(data)
        if (FALSIFY_RESPONSES and random.randint(1, 3) == 1):
            return '~{}{}{}%'.format(
                '{0:08x}'.format(0),
                '{0:04x}'.format(len(data) + 1).upper(),
                data)
        return '~{}{}{}%'.format(
            '{0:08x}'.format(0),
            '{0:04x}'.format(len(data)).upper(),
            data)

    elif data_type == 'Store':
        if "map" in payload:
            sendMapToDatabase(payload)
        elif "testcase" in payload:
            sendTestcaseToDatabase(payload)
        elif "currentmap" in payload:
            sendPicMapToDatabase(payload)
        elif "PathRequest" in payload:
            sendPathRequestToDatabase(payload)
        elif "USFront" in payload:
            sendUSToDatabase(payload)
        elif "USRetrieval" in payload:
            sendRetrievalUSToDatabase(payload)
        elif "BookDestination" in payload:
            sendBookDestinationToDatabase(payload)
        elif "Destination" in payload:
            sendDestinationToDatabase(payload)
        elif "BookRequest" in payload:
            sendBookRequestToDatabase(payload)
        elif "LocBook" in payload:
            sendLocBookToDatabase(payload)
        elif "RoverOneDone" in payload:
            sendRoverOneDoneToDatabase(payload)
        elif "ZackNav" in payload:
            sendZackNavToDatabase(payload)
        return "Good"
    else:
        return "Type must be Store or Request"


def handle(connection, address, lock):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("process-%r" % (address,))

    try:
        logger.debug("Connected %r at %r", connection, address)
        messageID = -1
        downstreamMessageID = 0
        good = False
        buffer = ""
        while True:
            data = connection.recv(1)
            if good:
                if (data == b'%'):
                    buffer += data.decode()
                    logger.debug("Received data: %r", buffer)
                    lock.acquire()
                    try:
                        result = parse(buffer.encode("utf-8"))
                    except:
                        good = False
                        result = "\0"
                        pass
                    lock.release()
                    if (result[0:1] == "~"):
                        result = '~{0:08x}'.format(downstreamMessageID).upper() + result[9:]
                        downstreamMessageID += 1
                        if (FALSIFY_RESPONSES and random.randint(1,3) == 1):
                            downstreamMessageID += 1
                        connection.send(result.encode())
                        print(result)

                        thisMessageID = int(buffer[1:9], 16)
                        if (thisMessageID - messageID > 1):
                            logger.debug("Result: Good, sent request result, but missed %i message(s)", thisMessageID - messageID - 1)
                        else:
                            logger.debug("Result: Good, sent request result")
                        messageID = thisMessageID
                    elif (result == "Good"):
                        thisMessageID = int(buffer[1:9], 16)
                        if (thisMessageID - messageID > 1):
                            logger.debug("Result: Good, but missed %i message(s)", thisMessageID - messageID - 1)
                        else:
                            logger.debug("Result: Good")
                        messageID = thisMessageID
                    elif (result != "Not a message"):
                        logger.debug("Result: %r", result)
                    good = False
                elif (data == b'~'):
                    good = True
                    buffer = "~"
                else:
                    buffer += data.decode()
            else:
                if (data == b'~'):
                    good = True
                    buffer = "~"
    except:
        logger.exception("Problem handling request")
    finally:
        ...
        # connection.close()


class Server(object):

    def __init__(self, hostname, port):
        import logging
        self.logger = logging.getLogger("server")
        self.hostname = hostname
        self.port = port

    def start(self):
        lock = Lock()
        self.logger.debug("listening")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)
        while True:
            conn, address = self.socket.accept()
            self.logger.debug("Got connection")
            process = multiprocessing.Process(target=handle, args=(conn, address, lock))
            process.daemon = True
            process.start()
            self.logger.debug("Started process %r", process)


def sendMapToDatabase(jsonTx):
    collection = "milestone4"
    if 'map' in jsonTx:
        db[collection].replace_one({'map.xcoord': jsonTx['map']['xcoord'], 'map.ycoord': jsonTx['map']['ycoord']},
                                   {'map': {'xcoord': jsonTx['map']['xcoord'], "ycoord": jsonTx['map']['ycoord'],
                                            "conf": jsonTx['map']['conf']}}, True)
def sendTestcaseToDatabase(jsonTx):
    collection = "milestone4"
    if 'testcase' in jsonTx:
        db[collection].replace_one({'testcase': { '$exists': 'true' }},
                                   {'testcase': jsonTx['testcase']}, True)

def sendPathRequestToDatabase(jsonTx):
    collection = "milestone4"
    if 'PathRequest' in jsonTx:
        db[collection].replace_one({'PathRequest': { '$exists': 'true' }},
                                   {'PathRequest': [jsonTx['PathRequest'][0], jsonTx['PathRequest'][1]]}, True)

def sendDestinationToDatabase(jsonTx):
    collection = "milestone4"
    if 'Destination' in jsonTx:
        db[collection].replace_one({'Destination': { '$exists': 'true' }},
                                   {'Destination': [jsonTx['Destination'][0], jsonTx['Destination'][1]]}, True)

def sendUSToDatabase(jsonTx):
    collection = "milestone4"
    if 'USFront' in jsonTx:
        db[collection].replace_one({'USFront': { '$exists': 'true' }},
                                   {'USFront': jsonTx['USFront'], 'USRight': jsonTx['USRight'], 'USLeft': jsonTx['USLeft'],
                                    'RoverLoc': [jsonTx['RoverLoc'][0], jsonTx['RoverLoc'][1]], 'TicksLeft': jsonTx['TicksLeft'], 'TicksRight': jsonTx['TicksRight']}, True)

def sendRetrievalUSToDatabase(jsonTx):
    collection = "milestone4"
    db[collection].replace_one({'USRetrieval': { '$exists': 'true' }},
                                   {'USRetrieval': jsonTx['USRetrieval'],
                                    'RoverLoc2': [jsonTx['RoverLoc2'][0], jsonTx['RoverLoc2'][1]]}, True)

def requestRetrievalLocFromDatabase():
    collection = "milestone4"
    return db[collection].find_one({'RoverLoc2': { '$exists': 'true' }}, {'RoverLoc2':1, '_id': 0})

def sendPicMapToDatabase(jsonTx):
    collection = "milestone4"
    if 'currentmap' in jsonTx:
        db[collection].replace_one({'currentmap': jsonTx['currentmap'], 'x': jsonTx['x'], 'y': jsonTx['y']},
                                   {'currentmap': jsonTx['currentmap'], 'x': jsonTx['x'], 'y': jsonTx['y'], 'conf': jsonTx['conf']}, True)

def requestMapFromDatabase(x, y):
    collection = "milestone4"
    newDict = {}
    num = 0
    if y == 0:
        sect = range(0, 5)
    elif y == 1:
        sect = range(5, 10)
    elif y == 2:
        sect = range(10, 15)
    elif y == 3:
        sect = range(15, 20)
    if y == 4:
        sect = range(20, 25)
    elif y == 5:
        sect = range(25, 30)
    elif y == 6:
        sect = range(30, 35)
    elif y == 7:
        sect = range(35, 40)

    for i in sect:
        newKey = 'map%i' % num
        dict = db[collection].find_one({'map.xcoord' : x, 'map.ycoord': i}, {'map.xcoord' : 1, 'map.ycoord': 1, 'map.conf':1, '_id': 0})
        dict[newKey] = dict.pop('map')
        # dict = json.dumps(dict)
        # dict = dict[1:-1]
        newDict.update(dict)
        num+=1
    return newDict

def sendBookRequestToDatabase(jsonTx):
    collection = "milestone4"
    if 'BookRequest' in jsonTx:
        db[collection].replace_one({'BookRequest': { '$exists': 'true' }},
                                   {'BookRequest': jsonTx['BookRequest']}, True)

def sendZackNavToDatabase(jsonTx):
    collection = "milestone4"
    if 'ZackNav' in jsonTx:
        db[collection].replace_one({'ZackNav': { '$exists': 'true' }},
                                   {'ZackNav': jsonTx['ZackNav']}, True)

def requestZackNavFromDatabase():
    collection = "milestone4"
    ZackNav = db[collection].find_one({'ZackNav': {'$exists': 'true'}},
                                   {'ZackNav':1, '_id': 0})
    return ZackNav

def sendBookDestinationToDatabase(jsonTx):
    collection = "milestone4"
    if 'BookDestination' in jsonTx:
        db[collection].replace_one({'BookDestination': { '$exists': 'true' }},
                                   {'BookDestination': [jsonTx['BookDestination'][0], jsonTx['BookDestination'][1]]}, True)

def sendRoverOneDoneToDatabase(jsonTx):
    collection = "milestone4"
    if 'RoverOneDone' in jsonTx:
        db[collection].replace_one({'RoverOneDone': { '$exists': 'true' }},
                                   {'RoverOneDone': jsonTx['RoverOneDone']}, True)

def sendLocBookToDatabase(jsonTx):
    collection = "milestone4"
    whichBook = 'LocBook' + str(jsonTx['LocBook'][0])
    var = db[collection].replace_one({whichBook : {'$exists': 'true'}},
                                { whichBook: [jsonTx['LocBook'][1], jsonTx['LocBook'][2]]}, True)
    var = 4

def requestTestcaseFromDatabase():
    collection = "milestone4"
    return db[collection].find_one({'testcase': { '$exists': 'true' }}, {'testcase':1, '_id': 0})

def requestUSDataFromDatabase():
    collection = "milestone4"
    return db[collection].find_one({'USRight': { '$exists': 'true' }}, {'USFront':1, 'USRight':1, 'USLeft':1, 'TicksLeft':1, 'TicksRight':1, '_id': 0})

def requestLocBookFromDatabase(request):
    collection = "milestone4"
    temp = db[collection].find_one({request: { '$exists': 'true' }},
                                   {request:1, '_id': 0})
    return temp

def requestDestinationFromDatabase():
    collection = "milestone4"
    return db[collection].find_one({'Destination': { '$exists': 'true' }},
                                   {'Destination':1, '_id': 0})

def requestBookDestinationFromDatabase():
    collection = "milestone4"
    bookDestination = db[collection].find_one({'BookDestination': { '$exists': 'true' }},
                                   {'BookDestination':1, '_id': 0})
    db[collection].delete_one({'BookDestination': {'$exists': 'true'}})
    return bookDestination

def requestBookRequestFromDatabase():
    collection = "milestone4"
    bookRequest = db[collection].find_one({'BookRequest': {'$exists': 'true'}},
                                   {'BookRequest':1, '_id': 0})
    db[collection].delete_one({'BookRequest': {'$exists': 'true'}})
    return bookRequest

def requestPathRequestFromDatabase():
    collection = "milestone4"
    pathRequest = db[collection].find_one({'PathRequest': {'$exists': 'true'}},
                                   {'PathRequest':1, '_id': 0})
    # db[collection].delete_one({'PathRequest': {'$exists': 'true'}})
    return pathRequest

def requestRoverLocFromDatabase():
    collection = "milestone4"
    roverLoc = db[collection].find_one({'RoverLoc': {'$exists': 'true'}},
                                   {'RoverLoc':1, '_id': 0})
    # db[collection].delete_one({'RoverLoc': {'$exists': 'true'}})
    return roverLoc

def requestEncoderTicksFromDatabase():
    collection = "milestone4"
    encoders = db[collection].find_one({'TicksLeft': {'$exists': 'true'}},
                                   {'TicksLeft':1, 'TicksRight': 1, '_id': 0})
    return encoders

def requestRoverOneDoneFromDatabase():
    collection = "milestone4"
    return db[collection].find_one({'RoverOneDone': {'$exists': 'true'}},
                                           {'RoverOneDone': 1, '_id': 0})

if __name__ == "__main__":
    main()


    # for x in db["milestone4"].find():
    #     print("Original: ", x)
    # print("[Checkpoint m-01] Stored document in collection '", jsonTx['Subject'], "' in MongoDB database '",
    #       jsonTx['Place'], "'")
    # data = db[collection].find()
    # dataList = list(data)
    # print("Last Document: ", dataList[-1])
    # '{"Type":"Store","map":{"xcoord":39, "ycoord":39, "conf":3}}'

            # for x in db["milestone4"].find():
    #     print("Final: ", x)