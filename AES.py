import os

from AESExceptions import KeyLengthException
from AESTables import sbox, hex_translate
from Utils import padd

key_combinations = {128: {'nk': 4, 'nb': 4, 'nr': 10}, 192: {'nk': 6, 'nb': 4, 'nr': 12},
                    256: {'nk': 8, 'nb': 4, 'nr': 14}}


class AES:
    def __init__(self, length=128, key=os.urandom(16)):
        self.__key = key if len(key) * 8 in key_combinations.keys() else os.urandom(16)
        self.__plain_text = None
        self.__cryptogram = None
        self.length = length if length in key_combinations.keys() else 128

    def generate_key(self, length: int) -> None:
        if length in key_combinations.keys():
            self.length = length
            self.__key = os.urandom(int(length / 8))
        else:
            raise KeyLengthException(length=length)

    def split_bytes(self, text):
        return [list(text[:4]), list(text[4:8]), list(text[8:12]), list(text[12:16])]

    def encrypt(self, plain_text: str, key=None) -> None:
        self.__plain_text = plain_text
        self.__cryptogram = bytes(plain_text, 'utf-8')
        if len(plain_text) < 16:
            self.__cryptogram = padd(self.__cryptogram)
        self.__cryptogram = self.split_bytes(self.__cryptogram)
        self.__key = key if key else self.__key
        self.length = self.length = len(self.__key * 8)
        self.add_round_key()
        for i in range(key_combinations[self.length]['nr']):
            self.__cryptogram = self.substitute_bytes(self.__cryptogram)

    def substitute_bytes(self, text: str) -> str:
        return ''.join([chr(sbox[hex_translate[bytes(char, 'utf-8').hex()[0]]][hex_translate[bytes(char, 'utf-8').hex()[1]]]) for char in text])
        # hex_table = [bytes(char, 'utf-8').hex() for char in text]
        # s_table = [sbox[hex_translate[hex_char[0]]][hex_translate[hex_char[1]]] for hex_char in hex_table]
        # s_table = [sbox[hex_translate[bytes(char, 'utf-8').hex()[0]]][hex_translate[bytes(char, 'utf-8').hex()[1]]] for char in text]
        # return ''.join(chr(char) for char in s_table)

    def mix_columns(self):
        ...

    def add_round_key(self):
        ...

    def shift_rows(self, text: list) -> list:
        text[1] = text[1][1:] + text[1][0]
        for i in range(2):
            text[2] = text[2][1:] + text[2][0]
        for i in range(3):
            text[3] = text[3][1:] + text[3][0]
        return text

    def decrypt(self, ciphered_text, key):
        self.__key = key
        self.length = len(key)
        ...

    def inv_substitute_bytes(self):
        ...

    def inv_mix_columns(self):
        ...

    def inv_shift_rows(self):
        ...

    def inv_sub_bytes(self):
        ...
