import socket
from random import randint
import time
from time import sleep
from pymongo import *
setting = '1'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 2000))
messageID = 0
# must be at  7 < x < 32 and 7 < y < 32, all boxes must be 8 grid spaces away from any other box in least one axis
boxes = [[8, 30]]

client_info = "mongodb://" + "zack" + ":" + "password" + "@" + "localhost" + ":" + "27017" + "/" + "admin"
dbclient = MongoClient('localhost')
db = dbclient["team3"]
collection = "milestone4"

def main():
    if setting == '0':
        resetMap()
    elif setting == '1':
        input("Press enter to insert the map for Testcase 1")
        insertMapTestCase1()
        input("Press enter to insert the centroids for the books.")
        insertCentroidsTestCase1()
        input("Press enter to insert a book request for Book1")
        insertBookRequest(1)
    elif setting == '2':
        input("Press enter to insert the map for Testcase 2")
        insertMapTestCase2()
        input("Press enter to insert the centroids for the books.")
        insertCentroidsTestCase2()
        input("Press enter to insert a book request for Book1")
        insertBookRequest(1)
        input("Press enter to insert a book request for Book2")
        insertBookRequest(2)
    elif setting == '3':
        input("Press enter to insert the map for Testcase 3")
        insertMapTestCase3()
        input("Press enter to update the data in the center portion that the rover has now explored.")
        insertSingleGrid(20,20, 5)
        input("Press enter to update the data in the center portion that the rover has now explored.")
        insertSingleGrid(28, 14, 5)
        input("Press enter to insert the centroids for the books.")
        insertCentroidsTestCase3()
        input("Press enter to insert a book request for Book3")
        insertBookRequest(3)
        input("Press enter to insert a book request for Book1")
        insertBookRequest(1)
        input("Press enter to insert a book request for Book2")
        insertBookRequest(2)
        input("Press enter to insert a book request for Book4")
        insertBookRequest(4)
    elif setting == '4':
        resetMap()
        insertConfGivenPath(5,5,5,35)
        insertConfGivenPath(5,35,35,35)
        insertConfGivenPath(35,35,35,5)
        insertConfGivenPath(35,5,5,5)
    elif setting == '5':
        insertTestCase()
    elif setting == '7':
        insertRoverOneDone(1)

    time.sleep(1)

    sock.close()


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

def insertSingleGrid(x,y,c):
    payload = '{"Type":"Store","map":{"xcoord":%i, "ycoord":%i, "conf":%i}}' % (x, y, c)
    messageID = 0
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


def insertMapTestCase1():
    # testcase 1
    Book1 = [20, 20]
    xStart = Book1[0]-1
    xEnd = Book1[0]+2
    yStart = Book1[1] - 1
    yEnd = Book1[1] + 2
    resetMap()
    fillInMiddleWithHighNegConf()
    fillInConfForBoxHighPosConf(xStart, xEnd, yStart, yEnd)

def insertCentroidsTestCase1():
    Book1 = [20,20]
    insertBookLocation(1, Book1[0], Book1[1])

def insertMapTestCase2():
    # testcase 2
    Book1 = [20, 28]
    Book2 = [20, 20]
    xStart = Book1[0] - 1
    xEnd = Book1[0] + 2
    yStart = Book1[1] - 1
    yEnd = Book1[1] + 2
    resetMap()
    fillInMiddleWithHighNegConf()
    fillInConfForBoxHighPosConf(xStart, xEnd, yStart, yEnd)
    xStart = Book2[0] - 1
    xEnd = Book2[0] + 2
    yStart = Book2[1] - 1
    yEnd = Book2[1] + 2
    fillInConfForBoxHighPosConf(xStart, xEnd, yStart, yEnd)

def insertCentroidsTestCase2():
    Book1 = [20, 28]
    Book2 = [20, 20]
    insertBookLocation(1, Book1[0], Book1[1])
    insertBookLocation(2, Book2[0], Book2[1])

def insertMapTestCase3():
    # testcase 3
    Book1 = [12, 20]
    Book2 = [28, 20]
    Book3 = [20, 14]
    Book4 = [20, 28]
    xStart = Book1[0] - 1
    xEnd = Book1[0] + 2
    yStart = Book1[1] - 1
    yEnd = Book1[1] + 2
    resetMap()
    fillInMiddleWithHighNegConf()
    fillInConfForBoxHighPosConf(xStart, xEnd, yStart, yEnd)
    xStart = Book2[0] - 1
    xEnd = Book2[0] + 2
    yStart = Book2[1] - 1
    yEnd = Book2[1] + 2
    fillInConfForBoxHighPosConf(xStart, xEnd, yStart, yEnd)
    xStart = Book3[0] - 1
    xEnd = Book3[0] + 2
    yStart = Book3[1] - 1
    yEnd = Book3[1] + 2
    fillInConfForBoxHighPosConf(xStart, xEnd, yStart, yEnd)
    xStart = Book4[0] - 1
    xEnd = Book4[0] + 2
    yStart = Book4[1] - 1
    yEnd = Book4[1] + 2
    fillInConfForBoxHighPosConf(xStart, xEnd, yStart, yEnd)
    insertSingleGrid(20,20,0)
    insertSingleGrid(28,14,0)

def insertCentroidsTestCase3():
    Book1 = [12, 20]
    Book2 = [28, 20]
    Book3 = [20, 14]
    Book4 = [20, 28]
    insertBookLocation(1, Book1[0], Book1[1])
    insertBookLocation(2, Book2[0], Book2[1])
    insertBookLocation(3, Book3[0], Book3[1])
    insertBookLocation(4, Book4[0], Book4[1])


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



def fillInMiddleWithHighNegConf():
    for x in range(8,32):
        for y in range(8,32):
            payload = '{"Type":"Store","map":{"xcoord":%i, "ycoord":%i, "conf":-9}}' % (x, y)
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

def fillInConfForBoxHighPosConf(xStart, xEnd, yStart, yEnd):
    for x in range(xStart, xEnd):
        for y in range(yStart, yEnd):
            payload = '{"Type":"Store","map":{"xcoord":%i, "ycoord":%i, "conf":8}}' % (x, y)
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

if __name__ == "__main__":
    main()