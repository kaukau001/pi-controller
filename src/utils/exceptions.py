class InvalidExtensionError(ValueError):
    def __init__(self, message="Extensão inválida"):
        self.message = message
        super().__init__(self.message)