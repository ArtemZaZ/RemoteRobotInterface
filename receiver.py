import socket
import threading
import eventmaster
import udpcp


class Receiver(threading.Thread):
    """ Класс принимающий сообщения """
    def __init__(self, **kwargs):
        threading.Thread.__init__(self, daemon=True, **kwargs)
        self._sock = socket.socket(**kwargs)
        self._host = None   # (ip, port)
        self._sender = None     # отсюда будем читать сообщения
        self.__exit = False     # метка выхода
        self._connected = False
        self._eventDict = {"onReceive": eventmaster.Event("onReceive")}     # создаем словарь событий
        self._eventMaster = eventmaster.EventMaster()   # создаем мастера событий
        self._eventMaster.append(self._eventDict["onReceive"])  # добавляем событие в мастер событий
        self._eventMaster.start()
        self.start()

    def connect(self, host):
        """ метод подключения к хосту """
        if self._connected:
            raise ConnectionError("Receiver уже подключен")
        else:
            try:
                self._host = host
                self._sock.bind(host)   # пытаемся
                self._sock.listen(1)    # слушаем только одного
                self._sender, _ = self._sock.accept()   # пробуем подключиться
                self._connected = True
            except:
                raise ConnectionError("Не удалось подключиться к " + str(host))

    def disconnect(self):
        """ метод отключения от хоста """
        self._connected = False
        self._sock.close()

    def exit(self):
        """ метод выхода из потока """
        self.__exit = True

    def _readPackage(self):
        """ метод для перегрузки классом наследником """
        pass

    def run(self):
        while not self.__exit:
            if self._connected:
                try:
                    package = self._readPackage()
                    self._eventDict["onReceive"].push(package)  # вызываем событие приема пакета
                except:
                    pass


class UdpcpReceiver(Receiver):
    def __init__(self, **kwargs):
        Receiver.__init__(self, **kwargs)

    def _readPackage(self):
        temp = bytearray(len(udpcp.protocolHeadConfig["start"]))
        while temp != udpcp.protocolHeadConfig["start"]:
            temp.pop(0)
            temp.append(self._sender.recv(1))
