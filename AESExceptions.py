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
