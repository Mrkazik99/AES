from AESTables import hex_values, sbox, inv_sbox
from AESExceptions import HexCodeException
from typing import Union


def padd(data):
    if len(data) % 16:
        pad_len = 16 - (len(data) % 16)
        return data + bytes(pad_len * chr(pad_len), 'utf-8')
    else:
        return data


def depadd(data):
    return data[:-ord(data[-1])]


# def split_blocks(plain_text: Union[str, bytes], size: int) -> list:
#     blocks = list()
#     blocks.extend([plain_text[i:i + size] for i in range(0, len(plain_text), size)])
#     return blocks


def xor_bytes(b1, b2):
    result = bytearray()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return bytes(result)


def xor(i1, i2):
    return i1 ^ i2


def g_mul(a, b):
    p = 0
    for c in range(8):
        if b & 1:
            p ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11b
        b >>= 1
    return p


def hex_translate(hex_code):
    x = ''
    y = ''
    if len(hex_code) == 4:
        x = int(hex_code[2] if hex_code[2].isdigit() else hex_values[hex_code[2]])
        y = int(hex_code[3] if hex_code[3].isdigit() else hex_values[hex_code[3]])
    elif len(hex_code) == 3:
        x = 0
        y = int(hex_code[2] if hex_code[2].isdigit() else hex_values[hex_code[2]])
    else:
        raise HexCodeException(hex_code)
    return [x, y]


def hex_translate2(hex_code):
    x = ''
    y = ''
    if len(hex_code) == 4:
        x = str(hex_code[2])
        y = str(hex_code[3])
    elif len(hex_code) == 3:
        x = str(0)
        y = str(hex_code[2])
    return ''.join([x, y])


def hex_transform(text):
    return bytes.fromhex(text)
