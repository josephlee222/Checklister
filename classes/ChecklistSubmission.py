from datetime import datetime
from time import time

class ChecklistSubmission:
    def __init__(self, userId, machineId, path):
        self.id = int(time() * 1000)
        self.path = path
        self.userId = userId
        self.machineId = machineId
        self.updatedOn = datetime.timestamp(datetime.now())
        self.createdOn = datetime.timestamp(datetime.now())

    def timeToString(self):
        return datetime.fromtimestamp(self.updatedOn).strftime("%Y-%m-%d, %H:%M:%S")