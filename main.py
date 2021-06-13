from AES import AES
from datetime import datetime
import argparse

from Utils import hex_transform, padd
from AESExceptions import NotEnoughArgsException, FileOutputException, NoKeyForDecryptionException, \
    InlineMessageLengthException


def open_hex_file(name):
    return open(name + '_hex.txt', 'w+')


def open_str_file(name):
    return open(name + '.txt', 'w+')


if __name__ == '__main__':
    # aes = AES(key=b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f')
    # print(aes.encrypt(b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xaa\xbb\xcc\xdd\xee\xff'))
    start = datetime.now()

    parser = argparse.ArgumentParser(description='Encrypt or Decrypt some text with 128, 192 or 256 bit key')

    parser.add_argument('-k', metavar='Key', type=str, help='Use your key')
    parser.add_argument('-d', action='store_true', help='Use for decryption (default: encryption)')
    parser.add_argument('-f', metavar='Input file name/file path', type=open, help='Pass a file to encrypt or decrypt')
    parser.add_argument('-o', metavar='Output file name', type=str,
                        help='Pass a file name to save cryptogram or plain text')
    parser.add_argument('-hex', action='store_true',
                        help='Use if your input is hexadecimal for example: ab121d02 (default: normal text input)')
    parser.add_argument('-t', metavar='message', type=str,
                        help='Input for plain text or cryptogram in str (your message or crypogram). This can handle only one block (16 charaters).')

    args = parser.parse_args()

    if args.f is None and args.k is None and args.t is None:
        raise NotEnoughArgsException(0)
    elif args.f is None and args.t is None:
        raise NotEnoughArgsException(1)

    aes = AES()

    if args.k is not None:
        if args.hex:
            aes.set_key(hex_transform(args.k))
        else:
            aes.set_key(bytes(args.k))

    if args.d:
        if args.k is None:
            raise NoKeyForDecryptionException()
        if args.f is not None:
            if args.o is None:
                raise FileOutputException()
            else:
                f_out = open_str_file(args.o)
                f_out_hex = open_hex_file(args.o)
                with args.f as f:
                    index = 0
                    file_length = int(sum([len(line) for line in f])/16)
                    file_length = int(file_length/2) if args.f else file_length
                    f.seek(0)
                    while True:
                        if args.hex:
                            block = hex_transform(f.read((aes.nb ** 2) * 2))
                        else:
                            block = bytes(f.read(aes.nb ** 2), 'utf-8')
                        if not block:
                            break
                        if index == file_length:
                            temp = aes.decrypt(block, True)
                        else:
                            temp = aes.decrypt(block, False)
                        print(f'Decrypted {index} out of {file_length} blocks')
                        index += 1
                        f_out.write(temp['str'])
                        f_out_hex.write(temp['hex'])
                    print('Key: ', aes.pretty_key())
        else:
            if args.t is not None:
                if args.o is not None:
                    f_out = open_str_file(args.o)
                    f_out_hex = open_hex_file(args.o)
                    if args.hex:
                        if 1 <= len(args.t) <= (aes.nb ** 2) * 2:
                            temp = aes.decrypt(hex_transform(args.t), True)
                        else:
                            raise InlineMessageLengthException(int(len(args.t) / 2))
                    else:
                        if 1 <= len(args.t) <= aes.nb ** 2:
                            temp = aes.decrypt(bytes(args.t, 'utf-8'), True)
                        else:
                            raise InlineMessageLengthException(len(args.t))
                    f_out.write(temp['str'])
                    f_out_hex.write(temp['hex'])
                    print('key: ', aes.pretty_key())
                else:
                    if args.hex:
                        if 1 <= len(args.t) <= (aes.nb ** 2) * 2:
                            temp = aes.decrypt(hex_transform(args.t), True)
                        else:
                            raise InlineMessageLengthException(int(len(args.t) / 2))
                    else:
                        if 1 <= len(args.t) <= aes.nb ** 2:
                            temp = aes.decrypt(bytes(args.t, 'utf-8'), True)
                        else:
                            raise InlineMessageLengthException(len(args.t))
                    print('Str output: ', temp['str'])
                    print('Hex output: ', temp['hex'])
                    print('key: ', aes.pretty_key())
    else:
        if args.f is not None:
            if args.o is None:
                raise FileOutputException()
            else:
                f_out = open_hex_file(args.o)
                with args.f as f:
                    index = 0
                    file_length = int(sum([len(line) for line in f])/16)
                    file_length = int(file_length/2) if args.hex else file_length
                    f.seek(0)
                    while True:
                        if args.hex:
                            block = hex_transform(f.read((aes.nb ** 2) * 2))
                        else:
                            block = bytes(f.read(aes.nb ** 2), 'utf-8')
                        if not block:
                            break
                        if index == file_length and len(block) < 16:
                            block = padd(block)
                        temp = aes.encrypt(block)
                        print(f'Encrypted {index} out of {file_length} blocks')
                        index += 1
                        f_out.write(temp)
                    print('Key: ', aes.pretty_key())
        else:
            if args.t is not None:
                if args.o is not None:
                    f_out_hex = open_hex_file(args.o)
                    if len(args.t) < 16:
                        args.t = padd(args.t)
                    if args.hex:
                        if 1 <= len(args.t) <= (aes.nb ** 2) * 2:
                            temp = aes.encrypt(hex_transform(args.t))
                        else:
                            raise InlineMessageLengthException(int(len(args.t) / 2))
                    else:
                        if 1 <= len(args.t) <= aes.nb ** 2:
                            temp = aes.encrypt(bytes(args.t, 'utf-8'))
                        else:
                            raise InlineMessageLengthException(len(args.t))
                    f_out_hex.write(temp)
                    print('key: ', aes.pretty_key())
                else:
                    if len(args.t) < 16:
                        args.t = padd(args.t)
                    if args.hex:
                        if 1 <= len(args.t) <= (aes.nb ** 2) * 2:
                            temp = aes.encrypt(hex_transform(args.t))
                        else:
                            raise InlineMessageLengthException(int(len(args.t) / 2))
                    else:
                        if 1 <= len(args.t) <= aes.nb ** 2:
                            temp = aes.encrypt(bytes(args.t, 'utf-8'))
                        else:
                            raise InlineMessageLengthException(len(args.t))
                    print('Hex output: ', temp)
                    print('key: ', aes.pretty_key())

    print('Time of running: ', datetime.now() - start)
