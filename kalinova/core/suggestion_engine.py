from core.app_state import app_state

class SuggestionEngine:

    @staticmethod
    def generate():
        ports = app_state.open_ports

        suggestions = []

        if 80 in ports or 443 in ports:
            suggestions.append("Web service detected → Run Nikto")

        if 22 in ports:
            suggestions.append("SSH detected → Consider Hydra")

        if 21 in ports:
            suggestions.append("FTP detected → Try brute force")

        if not suggestions:
            suggestions.append("No high-risk services detected")

        app_state.suggestion = " | ".join(suggestions)