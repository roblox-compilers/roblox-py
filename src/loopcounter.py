"""Label counter for the loops continue"""

class LoopCounter:
    """Loop counter"""
    COUNTER = 0

    @staticmethod
    def get_next():
        """Return next loop continue label name"""
        LoopCounter.COUNTER += 1
        return "continue {}".format(LoopCounter.COUNTER)
