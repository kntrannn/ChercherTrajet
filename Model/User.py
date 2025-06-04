class User:
    """User class to represent a user in the application."""

    __slots__ = ["id", "username", "password"]   # propose by AI

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
