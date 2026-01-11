class ChatMemory:
    def __init__(self, max_turns=5):
        self.max_turns = max_turns
        self.history = []

    def add(self, user, assistant):
        self.history.append((user, assistant))
        if len(self.history) > self.max_turns:
            self.history.pop(0)

    def build(self):
        if not self.history:
            return "No previous conversation."

        return "\n".join(
            [f"User: {u}\nAssistant: {a}" for u, a in self.history]
        )

    def clear(self):
        self.history = []
