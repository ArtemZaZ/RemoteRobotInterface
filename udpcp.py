import struct

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


def pack(functionName, args, argsTypes, packageNumber, checksum):
    packageFormat = "iii%dsc%dsc" % (len(argsTypes), len(functionName)) + argsTypes
    return struct.pack(packageFormat, struct.calcsize(packageFormat), checksum, packageNumber,
                       bytes(bytearray(argsTypes, "utf-8")), b'/',
                       bytes(bytearray(functionName, "utf-8")), b'/', *args)


def unpack(package):
    return struct.unpack("iii", package[0:12])


if __name__ == "__main__":
    package = pack("move", (1, 2.0, b's'), "ifc", 0, 16)
    print(unpack(package))
