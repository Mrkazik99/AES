from AESTables import hex_translate, sbox


def padd(data):
    pad_len = 16 - (len(data) % 16)
    return pad_len * chr(pad_len)


def depadd(data):
    return data[:-ord(data[-1])]


def split_bytes(text):
    return [text[:4], text[4:8], str(text[8:12]), str(text[12:16])]


# def substitute_bytes(text):
#     hex_table = list()
#     s_table = list()
#     for char in text:
#         hex_table.append(bytes(char, 'utf-8').hex())
#     for hex in hex_table:
#         s_table.append(sbox[hex_translate[hex[0]]][hex_translate[hex[1]]])
#     return ''.join(chr(char) for char in s_table)


# def shift_rows(text: list) -> list:
#     text[1] = text[1][1:]+text[1][0]
#     for i in range(2):
#         text[2] = text[2][1:]+text[2][0]
#     for i in range(3):
#         text[3] = text[3][1:]+text[3][0]
#     return text
