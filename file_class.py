class File:
    def __init__(self, filename):
        self.filename = filename
        self.quantity = 0
        self.date = ""
        self.min_date = 10**100
        self.max_date = 0