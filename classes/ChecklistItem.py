from datetime import datetime
from time import time

class ChecklistItem:
    def __init__(self, name):
        self.id = int(time() * 1000)
        self.filename = name
        self.path = ""
        self.updatedOn = datetime.timestamp(datetime.now())
        self.createdOn = datetime.timestamp(datetime.now())