import socket

from rri.receiver import Receiver, UdpcpReceiver
from rri.sender import Sender
from rri.remoteclass import UdpcpRemoteClass, UdpcpRemoteClassInterface
from rri import udpcp
import time

"""
rec = UdpcpReceiver()
rec.subscribe("onReceive", lambda x: print(x))
rec.connect(("127.0.0.1", 5000))

sen = Sender(type=socket.SOCK_DGRAM)
sen.connect(("127.0.0.1", 5000))
sen.sendPackage(udpcp.pack("adw", 11, 1, 2, 3))
sen.sendPackage(udpcp.pack("sw", 143, 3, 1, 6))
"""


class Robot(UdpcpRemoteClass):
    def __init__(self):
        UdpcpRemoteClass.__init__(self)

    def move(self, speed):
        print("speed", speed)


robot = Robot()
robot.connect(("127.0.0.1", 5000))
robot.register()

robotInterface = UdpcpRemoteClassInterface()
robotInterface.connect(("127.0.0.1", 5000))
robotInterface.move(1, 100)

while True:
    time.sleep(1)

