import struct
import pickle

"""
UDP Control Protocol - UDP Протокол управления
    :package format: <<package len | checksum | package number | args types*\* | function name*\* | args >>
    :field package len(4 байта): длина пакета в байтах
    :field checksum(4 байта): избыточный код для проверки сообщения на ошибки
    :field package number(4 байта): номер пакета(каждый новый пакет +1 к номеру, после переполнения 4 байт обнуляется)
    :field args types(var): типы аргументов ф-ий(следуют друг за другом(прим. ffif)). *\* - разделитель сообщения
    :field function name(var): имя ф-ии, которая вызовется на роботе
    :field args(var): поле параметров ф-ии(следуют друг за другом)
"""

_protocolHeadConfig = {
    "start": b'\xAA\xAA',   # стартовые байты
    "formatPackageLen": 'i',  # 4 байта
    "formatPackageNum": 'i',  # 4 байта
    "formatChecksum": 'i',    # 4 байта
    "checksum": "crc8"      # хеш сумма crc8
}

_headFormat = _protocolHeadConfig["formatPackageLen"]\
            + _protocolHeadConfig["formatPackageNum"]\
            + _protocolHeadConfig["formatChecksum"]

_headSize = len(_protocolHeadConfig["start"]) + struct.calcsize(_headFormat)


def pack(packageNumber, functionName, *args):
    data = pickle.dumps((functionName, *args), 3)
    packageLen = len(data) + _headSize
    checksum = 0
    head = _protocolHeadConfig["start"] + struct.pack(_headFormat, packageLen, checksum, packageNumber)
    return head + data


def unpack(package):
    return struct.unpack("iii", package[0:12])


if __name__ == "__main__":
    package = pack(10, "move", "ifc", 0, 16)
    print(package)
