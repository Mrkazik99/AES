from AES import AES
from datetime import datetime
import argparse
import pathlib

from Utils import hex_transform
from AESExceptions import NotEnoughArgsException, FileOutputException, NoKeyForDecryptionException

if __name__ == '__main__':
    # aes = AES(key=b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f')
    # print(aes.encrypt(b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xaa\xbb\xcc\xdd\xee\xff'))
    start = datetime.now()

    parser = argparse.ArgumentParser(description='Encrypt or Decrypt some text with 128, 192 or 256 bit key, this implementation does not provide support for ')

    parser.add_argument('-k', metavar='Key', type=str, help='Use your key')
    parser.add_argument('-d', action='store_true', help='Use for decryption (default: encryption)')
    parser.add_argument('-f', metavar='Input file name/file path', type=open, help='Pass a file to encrypt or decrypt')
    parser.add_argument('-out', metavar='Output file name', type=str, help='Pass a file name to save cryptogram or plain text')
    parser.add_argument('-hex', action='store_true',
                        help='Use if your input is hexadecimal for example: ab121d02 (default: normal text input)')
    parser.add_argument('-text', metavar='message', type=str,
                        help='Input for plain text or cryptogram in str (your message or crypogram)')

    args = parser.parse_args()

    if args.f is None and args.k is None and args.text is None:
        raise NotEnoughArgsException(0)
    elif args.f is None and args.text is None:
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
            if args.out is None:
                raise FileOutputException()
            else:
                f_out = open(args.out+'.txt', 'w+')
                f_out_hex = open(args.out+'_hex.txt', 'w+')
                with args.f as f:
                    index = 0
                    file_length = sum([len(line) for line in f])
                    f.seek(0)
                    print(f'Your file contain {int(file_length / 16)} blocks')
                    while True:
                        if args.hex:
                            block = f.read((aes.nb ** 2) * 2)
                        else:
                            block = f.read(aes.nb ** 2)
                        if not block:
                            break
                        if args.hex:
                            temp = aes.decrypt(hex_transform(block))
                        else:
                            temp = aes.decrypt(bytes('block', 'utf-8'))





    # if not args.d:
    #     if args.f is not None:
    #         f1 = open('output4.txt', 'w+')
    #         with args.f as f:
    #             index = 0
    #             file_length = sum([len(line) for line in f])
    #             f.seek(0)
    #             print(f'Your file contain {int(file_length/16)} blocks')
    #             while True:
    #                 if args.hex:
    #                     block = f.read((aes.nb ** 2) * 2)
    #                 else:
    #                     block = f.read(aes.nb ** 2)
    #                 if not block:
    #                     break
    #                 if args.hex:
    #                     f1.write(aes.encrypt(hex_transform(block)))
    #                     print(f'Encrypted {index} out of {int(file_length / 16)} blocks')
    #                     index += 1
    #                 else:
    #                     f1.write(aes.encrypt(bytes(block, 'utf-8')))
    #                     print(f'Encrypted {index} out of {int(file_length / 16)} blocks')
    #                     index += 1
    #             print(aes.pretty_key(aes.key))
    #
    #     #     for block in text_blocks:
    #     #         print(aes.encrypt(block))
    #     #     print(aes.pretty_key(aes.key))
    #     # print('encrypt')
    #     # aes.encrypt()
    # else:
    #     if args.f is not None:
    #         text_blocks = list()
    #         with args.f as f:
    #             while True:
    #                 if args.hex:
    #                     block = f.read((aes.nb ** 2) * 2)
    #                 else:
    #                     block = f.read(aes.nb ** 2)
    #                 if not block:
    #                     break
    #                 if args.hex:
    #                     text_blocks.append((hex_transform(block)))
    #                 else:
    #                     text_blocks.append(bytes(block, 'utf-8'))
    #
    #         for block in text_blocks:
    #             print(aes.decrypt(block))
    #         print(aes.pretty_key(aes.key))
    #     print('decrypt')
    #     # aes.decrypt()

    print('Time of running: ', datetime.now() - start)
