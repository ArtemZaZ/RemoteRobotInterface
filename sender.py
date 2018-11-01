import threading
import socket
import queue


class Sender(threading.Thread):
    """ класс, отправляющий пакеты """
    def __init__(self, **kwargs):
        threading.Thread.__init__(self, daemon=True, **kwargs)
        self._sock = socket.socket(**kwargs)
        self._queue = queue.Queue()     # очередь пакетов
        self._host = None   # (ip, port)
        self._connected = False     # подключен sender или нет
        self.__exit = False      # метка выхода
        self.start()

    def connect(self, host):
        """ метод подключения к хосту """
        if self._connected:
            raise ConnectionError("Sender уже подключен")
        else:
            try:
                self._host = host
                self._sock.connect(host)    # пробуем подключиться
                self._connected = True
            except:
                raise ConnectionError("Не удалось подключиться к " + str(host))

    def disconnect(self):
        """ ф-ия отключения от хоста """
        self._connected = False
        self._sock.close()

    def sendPackage(self, package):
        """ ф-ия отправки пакета """
        if self._connected:
            self._queue.put(package)    # добавляем пакет в очередь на отправку
        else:
            raise IOError("Sender не подключен")

    def exit(self):
        """ метод выхода из потока """
        self.__exit = True

    def run(self):
        while not self.__exit:
            try:
                self._sock.send(self._queue.get())  # ждем пока придет пакет и отправляем его
            except:
                pass

