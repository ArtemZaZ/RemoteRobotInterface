import udpcp
import sender

send = sender.Sender()
send.connect(("127.0.0.1", 5000))


print(udpcp.__doc__)
