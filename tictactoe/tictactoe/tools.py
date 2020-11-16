class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InvalidActionError(Error):
    """Exception for when an invalid move is made on the tic tac toe board

    Attributes:
        message -- explanation of the error
        action -- action tried that was invalid
    """

    def __init__(self, action):
        self.action = action
        self.message = f"You cannot move into the box at location {action}"