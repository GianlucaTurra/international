class TournamentIsCompleted(Exception):
    """
    Custom Exception raised to explicitly tell api methods the operation is
    not valid for completed tournaments.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TournamentIsOngoing(Exception):
    """
    Custom Exception raised to explicitly tell api methods the operation is
    not valid for ongoing tournaments.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
