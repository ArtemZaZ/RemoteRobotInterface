import socket

from rri import receiver, sender, udpcp
import time

rec = receiver.UdpcpReceiver()
rec.subscribe("onReceive", lambda x: print(x))
rec.connect(("127.0.0.1", 5000))

sen = sender.Sender(type=socket.SOCK_DGRAM)
sen.connect(("127.0.0.1", 5000))
sen.sendPackage(udpcp.pack(11, "adw", 1, 2, 3))
sen.sendPackage(udpcp.pack(123, "sw", 3, 1, 6))

while True:
    time.sleep(1)

