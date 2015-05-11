class InvalidGuessError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        message = "Invalid Guess character: {0}"
        return repr(message.format(self.value))
