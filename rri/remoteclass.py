from .receiver import Receiver
from .eventmaster import Event, EventMaster


class RemoteClass:
    """ Удаленный класс, который ставится на робота """
    def __init__(self):
        self._receiver = Receiver()     # приемник
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
            self._eventDict.update({attr: event})     # добавляем новое событие по названию ф-ии
            self._eventMaster.append(event)
        self._eventMaster.start()


class RemoteClassInterface:
    def __init__(self):
        pass


if __name__ == "__main__":
    rc = RemoteClass()
    rc.register()
