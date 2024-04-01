class RecordNotFoundException(Exception):

    """This exception is raised if no SQL table records
    matching the WHERE condition are found."""
    
    def __init__(self, message):
        """PARAMETERS
        message - The message that will be raised.
        """
        self.message = message

