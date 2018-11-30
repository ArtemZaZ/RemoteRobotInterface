import struct
import pickle
import crc16

"""
UDP Control Protocol - UDP Протокол управления
    :package format: << checksum | package number ||| function name | args >>
    :field checksum(2 байта): избыточный код для проверки сообщения на ошибки
    :field package number(4 байта): номер пакета(каждый новый пакет +1 к номеру, после переполнения 4 байт обнуляется)
    :field function name(var): имя ф-ии, которая вызовется на роботе
    :field args(var): поле параметров ф-ии(следуют друг за другом)
"""

protocolHeadConfig = {
    "formatPackageNum": 'i',  # 4 байта
    "formatChecksum": 'H',    # 2 байта
    "checksum": "crc16"      # хеш сумма crc16
}

_headFormat = protocolHeadConfig["formatPackageNum"] \
              + protocolHeadConfig["formatChecksum"]

_headSize = struct.calcsize(_headFormat)


def pack(packageNumber, functionName, *args):
    """ Упаковка пакета данных в пакет UDPCP """
    data = pickle.dumps((functionName, *args), 3)   # сами данные
    packageLen = len(data) + _headSize  # суммарная длина пакета
    checksum = crc16.crc16xmodem(data)  # контрольная сумма
    head = struct.pack(_headFormat, checksum, packageNumber)     # заголовок
    return head + data


def unpack(package):
    """ Распаковка пакета UDPCP """
    head = struct.unpack(_headFormat, package[:_headSize])     # кортеж заголовка
    data = package[_headSize:]  # сырые данные
    return (*head, *(pickle.loads(data)))   # распаковываем кортежи и запаковываем в кортеж


def check(package):
    """ Проверка контрольной суммы """
    checksum, _ = struct.unpack(_headFormat, package[:_headSize])   # получаем
    #  контрольную сумму
    data = package[_headSize:]  # сырые данные
    hesh = crc16.crc16xmodem(data)  # считаем контрольную сумму
    return hesh == checksum     # возвращаем результат


if __name__ == "__main__":
    package = pack(10, "move", 0, 16)
    if check(package):
        data = unpack(package)
        print(data)
