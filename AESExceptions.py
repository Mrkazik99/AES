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


class NotEnoughArgsException(Exception):
    """Exception raised when there is not enough args to run AES

    Attributes:
        amount -- amount of args
        message -- message for user
    """

    def __init__(self, amount, message="Not enough parameters given. You need at least 1 source of text (text or file) to run"):
        self.amount = amount
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.amount} -> {self.message}'


class FileOutputException(Exception):
    """Exception raised when user try to use file as input and got no file as output

    Attributes:
        message - message for user
    """

    def __init__(self, message="If you use file as an input, you have to use file as an output"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class NoKeyForDecryptionException(Exception):
    """Exception raised when user try to decrypt message with no key

    Attributes:
        message - message for user
    """

    def __init__(self, message="You have to use your key to decrypt message"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'