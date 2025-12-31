import struct
import re
import json
import unicodedata

def decode_message(buffer: bytes) -> dict:
    """
    Decodifica un buffer binario en un diccionario con claves específicas.
    Equivalente a buffer.readInt32LE en Node.js.
    """
    my_json = {}
    my_json["low_voltage_battery"] = struct.unpack_from("<i", buffer, 0)[0]
    my_json["low_voltage_solar"] = struct.unpack_from("<i", buffer, 4)[0]
    my_json["door_opened"] = struct.unpack_from("<i", buffer, 8)[0]
    my_json["object_close"] = struct.unpack_from("<i", buffer, 12)[0]
    my_json["high_temperature"] = struct.unpack_from("<i", buffer, 16)[0]
    my_json["dropped"] = struct.unpack_from("<i", buffer, 20)[0]
    my_json["kicked"] = struct.unpack_from("<i", buffer, 24)[0]
    my_json["error_extern_gpio"] = struct.unpack_from("<i", buffer, 28)[0]
    my_json["diagnostico"] = struct.unpack_from("<i", buffer, 32)[0]
    return my_json

def stringjson(texto):
    texto_normalizado = re.sub(r'\s+', ' ', texto).strip()
    texto_normalizado = texto_normalizado.replace(" ","")
    texto_normalizado = quitar_acentos(texto_normalizado)
    my_json=json.loads(texto_normalizado)
    print (my_json)
    return my_json

def quitar_acentos(texto):
    # Normaliza a NFD (Canonical Decomposition)
    nfkd_form = unicodedata.normalize('NFD', texto)
    # Filtra los caracteres que no son marcas diacríticas (Mn)
    return "".join([c for c in nfkd_form if not unicodedata.category(c) == 'Mn'])

