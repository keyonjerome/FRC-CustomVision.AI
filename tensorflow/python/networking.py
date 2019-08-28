import threading
import time
from networktables import NetworkTables
import math

# Robot networking code, makes program wait until network connection is confirmed to continue
cond = threading.Condition()
notified = [False]
visionTable = NetworkTables.getTable("SmartDashboard")

# listen for a connection to the robot
def connectionListener(connected, info):
    global cond
    global notified
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

def initialize():
    global visionTable
    # Initialize NetworkTables and add a listener for until the connection has been established
    NetworkTables.initialize(server='10.52.88.2')
    NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)
    visionTable = NetworkTables.getTable("SmartDashboard")
  
def wait_for_connection():
    global cond
    # as long as the Raspberry Pi has not connected to the roboRIO, wait for a connection
    with cond:
        print("Waiting")
        if not notified[0]:
            cond.wait()

    # At this point, the Raspberry Pi has connected.
    print("Connected!")
    #visionTable.putNumber("Connected!",0)

def putNumber(key,value):
    global visionTable
    visionTable.putNumber(key,value)

# print out every item in an array, instead of using an ellipsis to shorten it.
#np.set_printoptions(threshold=np.inf)

#def setTableNumber(table,key,value):
#    table.putNumber(key, value)

