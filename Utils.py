from AESTables import hex_translate, sbox


def padd(data):
    pad_len = 16 - (len(data) % 16)
    return data + bytes(pad_len * chr(00), 'utf-8')


def depadd(data):
    if data.endswith(b'\x00'):
        return data.replace(b'\x00', b'')
    else:
        return data
    # return data[:-ord(data[-1])]


def split_bytes(text: bytes, size: int):
    # return [list(text[:4]), list(text[4:8]), list(text[8:12]), list(text[12:16])]
    return [text[i:i + size] for i in range(0, len(text), size)]


def substitute_bytes(text):
    # s_table = [sbox[hex_translate[bytes(char, 'utf-8').hex()[0]]][hex_translate[bytes(char, 'utf-8').hex()[1]]] for char
    #            in text]
    # return ''.join(chr(char) for char in s_table)
    return ''.join(
        [chr(sbox[hex_translate[bytes(char, 'utf-8').hex()[0]]][hex_translate[bytes(char, 'utf-8').hex()[1]]]) for char
         in text])
    # return ''.join(chr(char) for char in s_table)

# def shift_rows(text: list) -> list:
#     text[1] = text[1][1:]+text[1][0]
#     for i in range(2):
#         text[2] = text[2][1:]+text[2][0]
#     for i in range(3):
#         text[3] = text[3][1:]+text[3][0]
#     return text
