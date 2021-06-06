class KeyLengthException(Exception):
    """Exception raised for wrong AES key length

    Attributes:
        length -- key length
        message -- message for user
    """

    def __init__(self, length: int, message="Key must be length of 128, 192 or 256 bits"):
        self.length = length
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.length} -> {self.message}'


class HexCodeException(Exception):
    """Exception raised for wrong Hexadecimal code format

    Attributes:
        code -- given code
        message -- message for user
    """

    def __init__(self, code: str, message="Hex code must be in format 0x00 or \\x00"):
        self.code = code
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.code} -> {self.message}'
