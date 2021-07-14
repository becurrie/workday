class ValidationError(Exception):
    """Custom ``ValidationError`` to allow passing a title and message into the error.
    """
    def __init__(self, *args, title, message):
        self.title = title
        self.message = message
        # Perform super call.
        super().__init__(*args)
