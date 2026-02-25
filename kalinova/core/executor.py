import subprocess
from PyQt6.QtCore import QThread, pyqtSignal

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
                PortParser.extract_ports(clean)

            process.wait()

            RiskEngine.calculate()
            SuggestionEngine.generate()

        except Exception as e:
            self.output_signal.emit(str(e))

        self.finished_signal.emit()