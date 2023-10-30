from time import time

class MachineType:
    def __init__(self, name, description):
        self.id = int(time() * 1000)
        self.name = name
        self.description = description
        self.checklist = []

    def createChecklistItem(self, item):
        self.checklist.append(item)