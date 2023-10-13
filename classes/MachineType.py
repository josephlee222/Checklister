from classes.ChecklistItem import ChecklistItem
from time import time

class MachineType:
    def __init__(self, name, description):
        self.id = int(time() * 1000)
        self.name = name
        self.description = description
        self.checklist: [ChecklistItem] = []

    def createChecklistItem(self, question: str, type: str, options: [str]):
        item = ChecklistItem(question, type, options)

        self.checklist.append(item)