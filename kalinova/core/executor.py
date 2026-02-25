import subprocess
from PyQt6.QtCore import QThread, pyqtSignal

from core.log_manager import LogManager
from core.port_parser import PortParser
from core.risk_engine import RiskEngine
from core.suggestion_engine import SuggestionEngine
from core.app_state import app_state


class CommandThread(QThread):

    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        try:
            # Log command
            LogManager.log_command(self.command)

            process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            for line in process.stdout:
                clean = line.strip()
                self.output_signal.emit(clean)

                LogManager.log_output(clean)
                PortParser.extract_ports(clean)

                # ========================
                # 🔥 EVENT DETECTION
                # ========================

                lower_line = clean.lower()

                # SQL Injection Detection
                if "sql injection" in lower_line:
                    app_state.add_event("SQL_INJECTION")

                # Hydra / Brute Force Detection
                if "hydra" in lower_line or "login:" in lower_line:
                    app_state.add_event("BRUTE_FORCE")

                # Gobuster Directory Enumeration
                if "found:" in lower_line:
                    app_state.add_event("DIR_ENUM")

                # Email Enumeration (Harvester)
                if "@" in clean and "." in clean:
                    app_state.add_event("EMAIL_ENUM")

            process.wait()

            # Calculate risk after execution
            RiskEngine.calculate()

            # Generate suggestions
            SuggestionEngine.generate()

        except Exception as e:
            self.output_signal.emit(str(e))
            LogManager.log_output(str(e))

        self.finished_signal.emit()