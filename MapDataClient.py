import socket
from random import randint
import time
from time import sleep
from pymongo import *
setting = '12'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 2000))
messageID = 0
# must be at  7 < x < 32 and 7 < y < 32, all boxes must be 8 grid spaces away from any other box in least one axis
boxes = [[8, 30]]

client_info = "mongodb://" + "zack" + ":" + "password" + "@" + "localhost" + ":" + "27017" + "/" + "admin"
dbclient = MongoClient('localhost')
db = dbclient["team3"]
collection = "milestone4"

Book1 = [20,20]
Book2 = [25,25]
Book3 = [28,28]

def main():
    if setting == '0':
        resetMap()
    elif setting == '1':
        resetMap()
        insertConfGivenPath(4,4,4,35)
        insertConfGivenPath(4,35,35,35)
        insertConfGivenPath(35,35,35,4)
        insertConfGivenPath(35,4,4,4)
    elif setting == '2':
        insertSingleGrid()
    elif setting == '3':
        insertTestCase()
    elif setting == '4':
        requestTestCaseRequest()
    elif setting == '5':
        insertBookRequest(1)
    elif setting == '6':
        insertBookDestination(4, 20)
    elif setting == '7':
        insertDestination(4, 4)
    elif setting == '8':
        insertRoverOneDone(1)
    elif setting == '9':
        insertBookLocation(1, 20, 20)
    elif setting == '10':
        requestLocBookFromDatabase(1)
    elif setting == '11':
        insertRoverLoc2()
    elif setting == '12':
        insertZackNav()

    time.sleep(1)

    sock.close()

def insertZackNav():
    payload = '{"Type": "Store", "ZackNav":1}'
    messageID = 0
    # while 1:
    id = hex(messageID)
    id = id[2:]
    while len(id) < 8:
        id = "0" + id

    length = hex(len(payload))
    length = length[2:]
    while len(length) < 4:
        length = "0" + length

    data = '~' + id.upper() + length.upper() + payload + '%'
    sock.sendall(data.encode(encoding='utf_8'))
    messageID += 1

def insertRoverLoc2():
    payload = '{"Type": "Store", "USRetrieval":%i, "RoverLoc2":[1,1]}'
    messageID = 0
    # while 1:
    id = hex(messageID)
    id = id[2:]
    while len(id) < 8:
        id = "0" + id

    length = hex(len(payload))
    length = length[2:]
    while len(length) < 4:
        length = "0" + length

    data = '~' + id.upper() + length.upper() + payload + '%'
    sock.sendall(data.encode(encoding='utf_8'))
    messageID += 1


def insertRoverOneDone(done):
    payload = '{"Type": "Store", "RoverOneDone":%i}' % done
    messageID = 0
    # while 1:
    id = hex(messageID)
    id = id[2:]
    while len(id) < 8:
        id = "0" + id

    length = hex(len(payload))
    length = length[2:]
    while len(length) < 4:
        length = "0" + length

    data = '~' + id.upper() + length.upper() + payload + '%'
    sock.sendall(data.encode(encoding='utf_8'))
    messageID += 1

def insertBookRequest(num):
    payload = '{"Type": "Store", "BookRequest": %i}' % num
    messageID = 0
    # while 1:
    id = hex(messageID)
    id = id[2:]
    while len(id) < 8:
        id = "0" + id

    length = hex(len(payload))
    length = length[2:]
    while len(length) < 4:
        length = "0" + length

    data = '~' + id.upper() + length.upper() + payload + '%'
    sock.sendall(data.encode(encoding='utf_8'))
    messageID += 1

def insertBookLocation(num, x, y):
    payload = '{"Type": "Store", "LocBook": [%i, %i,%i]}' % (num, x, y)
    messageID = 0
    # while 1:
    id = hex(messageID)
    id = id[2:]
    while len(id) < 8:
        id = "0" + id

    length = hex(len(payload))
    length = length[2:]
    while len(length) < 4:
        length = "0" + length

    data = '~' + id.upper() + length.upper() + payload + '%'
    sock.sendall(data.encode(encoding='utf_8'))
    messageID += 1

def insertPathRequest(x,y):
    payload = '{"Type": "Store", "PathRequest": [%i,%i]}' % (x, y)
    messageID = 0
    # while 1:
    id = hex(messageID)
    id = id[2:]
    while len(id) < 8:
        id = "0" + id

    length = hex(len(payload))
    length = length[2:]
    while len(length) < 4:
        length = "0" + length

    data = '~' + id.upper() + length.upper() + payload + '%'
    sock.sendall(data.encode(encoding='utf_8'))
    messageID += 1

def insertDestination(x,y):
    payload = '{"Type": "Store", "Destination": [%i,%i]}' % (x, y)
    messageID = 0
    # while 1:
    id = hex(messageID)
    id = id[2:]
    while len(id) < 8:
        id = "0" + id

    length = hex(len(payload))
    length = length[2:]
    while len(length) < 4:
        length = "0" + length

    data = '~' + id.upper() + length.upper() + payload + '%'
    sock.sendall(data.encode(encoding='utf_8'))
    messageID += 1

def insertBookDestination(x,y):
    payload = '{"Type": "Store", "BookDestination": [%i,%i]}' % (x, y)
    messageID = 0
    # while 1:
    id = hex(messageID)
    id = id[2:]
    while len(id) < 8:
        id = "0" + id

    length = hex(len(payload))
    length = length[2:]
    while len(length) < 4:
        length = "0" + length

    data = '~' + id.upper() + length.upper() + payload + '%'
    sock.sendall(data.encode(encoding='utf_8'))
    messageID += 1

def requestDestinationFromDatabase():
    payload = '{"Type": "Request", "Request": "Destination"}'
    messageID = 0
    # while 1:
    id = hex(messageID)
    id = id[2:]
    while len(id) < 8:
        id = "0" + id

    length = hex(len(payload))
    length = length[2:]
    while len(length) < 4:
        length = "0" + length

    data = '~' + id.upper() + length.upper() + payload + '%'
    sock.sendall(data.encode(encoding='utf_8'))
    messageID += 1

def requestLocBookFromDatabase(num):
    payload = '{"Type": "Request", "Request": "LocBook%i"}' % num
    messageID = 0
    # while 1:
    id = hex(messageID)
    id = id[2:]
    while len(id) < 8:
        id = "0" + id

    length = hex(len(payload))
    length = length[2:]
    while len(length) < 4:
        length = "0" + length

    data = '~' + id.upper() + length.upper() + payload + '%'
    sock.sendall(data.encode(encoding='utf_8'))
    messageID += 1

def insertTestCase():
    payload = '{"Type": "Store", "testcase":1}'
    messageID = 0
    # while 1:
    id = hex(messageID)
    id = id[2:]
    while len(id) < 8:
        id = "0" + id

    length = hex(len(payload))
    length = length[2:]
    while len(length) < 4:
        length = "0" + length

    data = '~' + id.upper() + length.upper() + payload + '%'
    sock.sendall(data.encode(encoding='utf_8'))
    messageID += 1

def requestTestCaseRequest():
    payload = '{"Type": "Request", "Request": "testcase"}'
    messageID = 0
    # while 1:
    id = hex(messageID)
    id = id[2:]
    while len(id) < 8:
        id = "0" + id

    length = hex(len(payload))
    length = length[2:]
    while len(length) < 4:
        length = "0" + length

    data = '~' + id.upper() + length.upper() + payload + '%'
    sock.sendall(data.encode(encoding='utf_8'))
    messageID += 1

def insertSingleGrid():
    payload = '{"Type":"Store","map":{"xcoord":12, "ycoord":8, "conf":0}}'
    messageID = 0
    # while 1:
    id = hex(messageID)
    id = id[2:]
    while len(id) < 8:
        id = "0" + id

    length = hex(len(payload))
    length = length[2:]
    while len(length) < 4:
        length = "0" + length

    data = '~' + id.upper() + length.upper() + payload + '%'
    sock.sendall(data.encode(encoding='utf_8'))
    messageID += 1

def resetMap():
    conf = 0
    for x in range(0, 40):
        for y in range(0, 40):
            messageID = 0;
            if x <= 7 or x >= 32 or y <= 7 or y >= 32 :
                conf = -10
            else:
                conf = 0

            payload = '{"Type":"Store","map":{"xcoord":%i, "ycoord":%i, "conf":%i}}' %(x,y, conf)

            # while 1:
            id = hex(messageID)
            id = id[2:]
            while len(id) < 8:
                id = "0" + id

            length = hex(len(payload))
            length = length[2:]
            while len(length) < 4:
                length = "0" + length

            data = '~' + id.upper() + length.upper() + payload + '%'
            sock.sendall(data.encode(encoding='utf_8'))
            messageID += 1

# for the sake of simplicity will follow straight line paths at 90 degree angles
def insertConfGivenPath(startX, startY, endX, endY):
    if endX - startX == 0:
        endX = startX + 1
    for x in range(8, 32):
        for y in range(8, 32):
            messageID = 0;
            jsonTx = db[collection].find_one({'map.xcoord': x, 'map.ycoord': y})
            payload = '{"Type":"Store","map":{"xcoord":%i, "ycoord":%i, "conf":%i}}' % (
                x, y, jsonTx['map']['conf'] - randint(1, 2))
            id = hex(messageID)
            id = id[2:]
            while len(id) < 8:
                id = "0" + id
            length = hex(len(payload))
            length = length[2:]
            while len(length) < 4:
                length = "0" + length
            data = '~' + id.upper() + length.upper() + payload + '%'
            sock.sendall(data.encode(encoding='utf_8'))
            sleep(.1)
            messageID += 1
    for x in range(startX, endX):
        for y in range(startY, endY):
            for box in boxes:

                #to left or right
                if (y == box[1] or y == box[1] - 1):
                    boxGrid = [ [box[0], box[1]], [box[0], box[1] - 1] ]
                    for gridbox in boxGrid:
                        jsonTx = db[collection].find_one({'map.xcoord': gridbox[0], 'map.ycoord': gridbox[1]})
                        payload = '{"Type":"Store","map":{"xcoord":%i, "ycoord":%i, "conf":%i}}' % (
                        gridbox[0], gridbox[1], jsonTx['map']['conf'] + randint(5, 6))
                        id = hex(messageID)
                        id = id[2:]
                        while len(id) < 8:
                            id = "0" + id
                        length = hex(len(payload))
                        length = length[2:]
                        while len(length) < 4:
                            length = "0" + length
                        data = '~' + id.upper() + length.upper() + payload + '%'
                        sock.sendall(data.encode(encoding='utf_8'))
                        sleep(.1)
                        messageID += 1
                #below or above
                elif (x == box[0] or x == box[0] + 1):
                    boxGrid = [[box[0], box[1]-1], [box[0]+1, box[1]-1]]
                    for gridbox in boxGrid:
                        jsonTx = db[collection].find_one({'map.xcoord': gridbox[0], 'map.ycoord': gridbox[1]})
                        payload = '{"Type":"Store","map":{"xcoord":%i, "ycoord":%i, "conf":%i}}' % (
                            gridbox[0], gridbox[1], jsonTx['map']['conf'] + randint(4,6))
                        id = hex(messageID)
                        id = id[2:]
                        while len(id) < 8:
                            id = "0" + id
                        length = hex(len(payload))
                        length = length[2:]
                        while len(length) < 4:
                            length = "0" + length
                        data = '~' + id.upper() + length.upper() + payload + '%'
                        sock.sendall(data.encode(encoding='utf_8'))
                        sleep(.1)
                        messageID += 1


if __name__ == "__main__":
    main()