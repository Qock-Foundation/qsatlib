class SuckError(Exception):
    def __init__(self, message):
        self.message = f'{message}, and you suck'
        super().__init__(self.message)
