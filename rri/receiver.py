import socket
import threading
import struct
from rri import eventmaster, udpcp


class Receiver(threading.Thread):
    """ Класс принимающий сообщения """
    def __init__(self, **kwargs):
        threading.Thread.__init__(self, daemon=True)
        self._sock = socket.socket(**kwargs)
        self._host = None  # (ip, port)
        self.__exit = False  # метка выхода
        self._connected = False
        self._eventDict = {"onReceive": eventmaster.Event("onReceive")}  # создаем словарь событий
        self._eventMaster = eventmaster.EventMaster()  # создаем мастера событий
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
                self._connect(host)
                self._connected = True
            except:
                raise ConnectionError("Не удалось подключиться к " + str(host))

    def _connect(self, host):
        """ метод для перегрузки классом наследником """

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

    def subscribe(self, event, handler):
        ev = self._eventDict[event]
        if not ev:
            raise eventmaster.EventError("Такого события нет")
        ev.connect(handler)


class UdpcpReceiver(Receiver):
    def __init__(self, **kwargs):
        Receiver.__init__(self, type=socket.SOCK_DGRAM, **kwargs)
        self.__headFormat = udpcp.protocolHeadConfig["formatPackageNum"] \
                            + udpcp.protocolHeadConfig["formatChecksum"]
        self.__headSize = struct.calcsize(self.__headFormat)  # размер заголовка
        self.bufferSize = 65527     # буффер данных на прием пакета

    def _connect(self, host):
        self._sock.bind(host)  # пытаемся подключиться

    def _readPackage(self):
        return udpcp.unpack(self._sock.recv(self.bufferSize))

