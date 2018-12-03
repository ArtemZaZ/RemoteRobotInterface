import socket

from . receiver import Receiver, UdpcpReceiver
from . sender import Sender
from . eventmaster import Event, EventMaster
from . import udpcp


class RemoteClass:
    """ Удаленный класс, который ставится на робота """
    def __init__(self):
        self._receiver = Receiver()     # приемник  # TODO: сделать так, чтоб они не подрубались изначально,т.е.None или др
        self._eventMaster = EventMaster()
        self._eventDict = {}
        self.exceptionNames = ['connect', 'exceptionNames', 'register']     # методы, которые н будут вызываться с
        # удалленного интерфейса

    def connect(self, host):
        """ подключение к удаленному интерфейсу """
        self._receiver.connect(host)

    def register(self):
        """ регистрация вызываемых с удаленного интерфейса методов """
        for attr in self.__dir__():      # пробегаем по всем не защищенным аттрибутам класса
            if (attr[0] == '_') or (attr in self.exceptionNames):
                continue
            event = Event(attr)
            event.connect(self.__getattribute__(attr))
            self._eventDict.update({attr: event})     # добавляем новое событие по названию ф-ии
            self._eventMaster.append(event)
        self._eventMaster.start()

        def subs(data):     # TODO: сделать какую-нибудь привязку, чтоб тут этого не было
            pass

        self._receiver.subscribe("onReceive", subs)


class RemoteClassInterface(object):
    """ Интерфейс удаленного класса, который ставится на пульт """
    def __init__(self):
        object.__init__(self)
        self._sender = Sender()     # передатчик # TODO: сделать так, чтоб они не подрубались изначально,т.е.None или др
        self.exceptionNames = ['connect', 'exceptionNames']  # методы, которые н будут вызываться с
        self.pack = udpcp.pack  # метод упаковки - по дефолту udpcp     # TODO: сделать другой

    def connect(self, host):
        self._sender.connect(host)

    def __getattr__(self, item):    # выдает те аттрибуты, которых не было при инициализации
        if item in self.__dict__:
            return self.__dict__[item]
        if item in self.exceptionNames:     # если аттрибут есть в списке исключений
            return self.__dict__[item]

        def __pack(*args):
            self._sender.sendPackage(self.pack(item, *args))

        return __pack


class UdpcpRemoteClass(RemoteClass):
    def __init__(self):
        RemoteClass.__init__(self)
        self._receiver = UdpcpReceiver()

    def register(self):
        RemoteClass.register(self)

        def subs(data):
            self._eventDict[data[2]].push(*data[3:])

        self._receiver.subscribe("onReceive", subs)


class UdpcpRemoteClassInterface(RemoteClassInterface):
    """ Интерфейс удаленного класса, который ставится на пульт и общается по протоколу udpcp """
    def __init__(self):
        RemoteClassInterface.__init__(self)
        self._sender = Sender(type=socket.SOCK_DGRAM)
        self.pack = udpcp.pack







