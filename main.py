from AES import AES
from datetime import datetime


if __name__ == '__main__':
    start = datetime.now()
    aes = AES(key=b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f')
    # aes = AES()
    print(aes.decrypt(b'\x69\xc4\xe0\xd8\x6a\x7b\x04\x30\xd8\xcd\xb7\x80\x70\xb4\xc5\x5a'))
    print('Time of running: ', datetime.now() - start)
