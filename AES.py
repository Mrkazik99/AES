import os

from AESExceptions import KeyLengthException
from AESTables import sbox, hex_translate
from Utils import padd


nr = {128: 10, 192: 12, 256: 14}


class AES:
    def __init__(self, length=128, key=os.urandom(16)):
        self.__key = key
        self.__plain_text = None
        self.length = length

    def generate_key(self, length: int) -> None:
        if length in [128, 192, 256]:
            self.length = length
            self.__key = os.urandom(int(length / 8))
        else:
            raise KeyLengthException(length=length)

    def split_bytes(self, text):
        return [text[:4], text[4:8], text[8:12], text[12:16]]

    def encrypt(self, plain_text: str, key=None) -> None:
        if len(plain_text) < 16:
            plain_text += padd(plain_text)
        self.__plain_text = self.split_bytes(plain_text)
        self.__key = key if key else self.__key
        self.length = self.length = len(self.__key*8)
        self.add_round_key()
        for i in range(nr[self.length]):
            pass

    def substitute_bytes(self, text: str) -> str:
        hex_table = [bytes(char, 'utf-8').hex() for char in text]
        s_table = [sbox[hex_translate[hex_char[0]]][hex_translate[hex_char[1]]] for hex_char in hex_table]
        return ''.join(chr(char) for char in s_table)

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
