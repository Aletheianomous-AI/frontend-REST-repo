class ConnectionFailureException(Exception):

    """This exception is raised if the chat_data_module
        fails to connect to the SQL server
    ."""
    
    def __init__(self, message):
        """PARAMETERS
        message - The message that will be raised.
        """
        super().__init__(message)
