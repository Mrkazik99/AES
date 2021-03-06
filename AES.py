import os

from AESExceptions import KeyLengthException
from AESTables import sbox, inv_sbox, rcon, galois_field, inverse_galois_field
from Utils import g_mul, xor_bytes, hex_translate, hex_translate2, depadd

key_combinations = {128: {'nk': 4, 'nb': 4, 'nr': 10}, 192: {'nk': 6, 'nb': 4, 'nr': 12},
                    256: {'nk': 8, 'nb': 4, 'nr': 14}}


class AES:
    def __init__(self, key=bytes(os.urandom(16))):
        if len(key) * 8 in key_combinations.keys():
            self.key = bytes(key)
            self.length = len(key) * 8

        else:
            raise KeyLengthException(len(key) * 8)

        self.key_schedule = None
        self.plain_text = None
        self.cryptogram = None

        self.nk = key_combinations[self.length]['nk']
        self.nb = key_combinations[self.length]['nb']
        self.nr = key_combinations[self.length]['nr']

    def set_key_params(self) -> None:
        self.nk = key_combinations[self.length]['nk']
        self.nb = key_combinations[self.length]['nb']
        self.nr = key_combinations[self.length]['nr']

    def set_key(self, key: bytes) -> None:
        if len(key) * 8 in key_combinations.keys():
            self.key = bytes(key)
            self.length = len(key) * 8

        else:
            raise KeyLengthException(len(key) * 8)

        self.key_schedule = None
        self.set_key_params()

    def generate_key(self, length: int) -> None:
        if length in key_combinations.keys():
            self.set_key(os.urandom(int(length/8)))

    def key_schedule_generator(self) -> None:
        keys = [bytearray()] * self.nb * (self.nr + 1)

        for i in range(self.nk):
            temp = bytearray()
            temp.extend([self.key[4 * i], self.key[4 * i + 1], self.key[4 * i + 2], self.key[4 * i + 3]])
            keys[i] = temp

        for i in range(self.nk, self.nb * (self.nr + 1)):
            temp = keys[i - 1]
            word = keys[i - self.nk]

            if i % self.nk == 0:
                x = bytearray(self.rot_word(temp))
                y = bytearray(self.sub_word(x))
                rcon_arr = rcon[int(i / self.nk)]
                temp = xor_bytes(y, rcon_arr)

            elif self.nk > 6 and i % self.nk == 4:
                temp = bytearray(self.sub_word(temp))

            keys[i] = bytearray(xor_bytes(word, temp))

        self.key_schedule = keys

    def rot_word(self, word: bytearray) -> bytearray:
        return word[1:] + word[:1]

    def sub_word(self, word: bytes) -> bytes:
        new_word = b''
        for char in word:
            new_word += int.to_bytes(sbox[hex_translate(hex(char))[0]][hex_translate(hex(char))[1]], 1, 'little')

        return new_word

    def split_bytes(self, plain_text: bytes) -> None:
        self.cryptogram = [bytearray(plain_text[i:i + self.nb]) for i in range(0, len(plain_text), self.nb)]

    def encrypt(self, plain_text):
        self.plain_text = plain_text

        self.split_bytes(plain_text)

        self.key_schedule_generator()
        self.add_round_key(self.key_schedule[0:self.nb])

        for i in range(1, self.nr, 1):
            self.substitute_bytes(False)
            self.shift_rows()
            self.mix_columns(False)
            self.add_round_key(self.key_schedule[i * self.nb:(i + 1) * self.nb])

        self.substitute_bytes(False)
        self.shift_rows()
        self.add_round_key(self.key_schedule[self.nr * self.nb:(self.nr + 1) * self.nb])

        return self.pretty_output()

    def decrypt(self, ciphered_text, pad):
        self.split_bytes(ciphered_text)
        self.key_schedule_generator()
        self.add_round_key(self.key_schedule[self.nr * self.nb:(self.nr + 1) * self.nb])
        for i in range(self.nr - 1, 0, -1):
            self.inv_shift_rows()
            self.substitute_bytes(True)
            self.add_round_key(self.key_schedule[i * self.nb: (i + 1) * self.nb])
            self.mix_columns(True)

        self.inv_shift_rows()
        self.substitute_bytes(True)
        self.add_round_key(self.key_schedule[0:self.nb])

        self.plain_text = self.cryptogram

        if pad:
            self.plain_text = depadd(self.plain_text)

        return {'str': self.str_output(), 'hex': self.pretty_output()}

    def substitute_bytes(self, inverse) -> None:

        for i, col in enumerate(self.cryptogram):

            for j, byte in enumerate(col):
                if not inverse:
                    self.cryptogram[i][j] = sbox[hex_translate(hex(byte))[0]][hex_translate(hex(byte))[1]]
                else:
                    self.cryptogram[i][j] = inv_sbox[hex_translate(hex(byte))[0]][hex_translate(hex(byte))[1]]

    def mix_columns(self, inverse):
        new_matrix = list()

        for i in range(self.nb):
            temp = bytearray()

            for j in range(self.nb):
                if not inverse:
                    temp.append(g_mul(self.cryptogram[i][0], galois_field[j][0]) ^ \
                                g_mul(self.cryptogram[i][1], galois_field[j][1]) ^ \
                                g_mul(self.cryptogram[i][2], galois_field[j][2]) ^ \
                                g_mul(self.cryptogram[i][3], galois_field[j][3]))
                else:
                    temp.append(g_mul(self.cryptogram[i][0], inverse_galois_field[j][0]) ^ \
                                g_mul(self.cryptogram[i][1], inverse_galois_field[j][1]) ^ \
                                g_mul(self.cryptogram[i][2], inverse_galois_field[j][2]) ^ \
                                g_mul(self.cryptogram[i][3], inverse_galois_field[j][3]))

            new_matrix.append(temp)

        self.cryptogram = new_matrix

    def add_round_key(self, rkey):
        for i, col in enumerate(self.cryptogram):
            for j, char in enumerate(col):
                self.cryptogram[i][j] = self.cryptogram[i][j] ^ rkey[i][j]

    def shift_rows(self):
        self.cryptogram = [
            bytearray([self.cryptogram[0][0], self.cryptogram[1][1], self.cryptogram[2][2], self.cryptogram[3][3]]),
            bytearray([self.cryptogram[1][0], self.cryptogram[2][1], self.cryptogram[3][2], self.cryptogram[0][3]]),
            bytearray([self.cryptogram[2][0], self.cryptogram[3][1], self.cryptogram[0][2], self.cryptogram[1][3]]),
            bytearray([self.cryptogram[3][0], self.cryptogram[0][1], self.cryptogram[1][2], self.cryptogram[2][3]])
        ]

    def inv_shift_rows(self):
        self.cryptogram = [
            bytearray([self.cryptogram[0][0], self.cryptogram[3][1], self.cryptogram[2][2], self.cryptogram[1][3]]),
            bytearray([self.cryptogram[1][0], self.cryptogram[0][1], self.cryptogram[3][2], self.cryptogram[2][3]]),
            bytearray([self.cryptogram[2][0], self.cryptogram[1][1], self.cryptogram[0][2], self.cryptogram[3][3]]),
            bytearray([self.cryptogram[3][0], self.cryptogram[2][1], self.cryptogram[1][2], self.cryptogram[0][3]])
        ]

    def pretty_output(self):
        out = ''
        for col in self.cryptogram:
            for char in col:
                out += str(hex_translate2(hex(char))[0]) + str(hex_translate2(hex(char))[1])
        return out

    def pretty_key(self):
        out = ''
        for char in self.key:
            out += str(hex_translate2(hex(char))[0]) + str(hex_translate2(hex(char))[1])
        return out

    def str_output(self):
        out = ''
        for col in self.cryptogram:
            for char in col:
                out += chr(char)
        return out
