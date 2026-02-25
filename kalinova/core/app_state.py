class AppState:
    def __init__(self):
        self.mode = "Beginner"
        self.global_risk = "LOW"
        self.open_ports = []
        self.suggestion = "No suggestions yet."

    def reset_scan(self):
        self.open_ports.clear()
        self.global_risk = "LOW"
        self.suggestion = "No suggestions yet."


app_state = AppState()