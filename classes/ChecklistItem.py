types = ["check", "multi_check", "option", "field"]

class ChecklistItem:
    def __init__(self, question, type, options):
        self.question: str = question
        self.options: [str] = options
        if type in types:
            self.type: str = type

