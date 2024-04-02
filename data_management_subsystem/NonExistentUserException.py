class NonExistentUserException(Exception):

    """This exception is raised if the userID does not exist."""
    
    def __init__(self, userId):
        """PARAMETERS
        message - The message that will be raised.
        """
        super().__init__("userID " + str(userId) + "does not exist.")
