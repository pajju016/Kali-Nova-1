from core.app_state import app_state

class RiskEngine:

    @staticmethod
    def calculate():
        ports = app_state.open_ports

        if not ports:
            app_state.global_risk = "LOW"
            return

        if 21 in ports or 22 in ports:
            app_state.global_risk = "MEDIUM"

        if 80 in ports or 443 in ports:
            app_state.global_risk = "MEDIUM"

        if len(ports) >= 5:
            app_state.global_risk = "HIGH"