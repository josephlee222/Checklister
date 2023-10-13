from time import time

class Machine:
    def __init__(self, name: str, notes: str, machineType: int = 0, room: int = 0):
        self.id = int(time() * 1000)
        self.name: str = name
        self.machineType: int = machineType
        self.notes: str = notes
        self.room = room
