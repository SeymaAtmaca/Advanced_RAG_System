class ChatMemory:
    def __init__(self, max_turns=5):
        self.history = []
        self.max_turns = max_turns

    def add(self, user, assistant):
        self.history.append((user, assistant))
        self.history = self.history[-self.max_turns:]

    def build(self):
        text = ""
        for u, a in self.history:
            text += f"User: {u}\nAssistant: {a}\n"
        return text
