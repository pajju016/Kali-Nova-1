from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer

from core.app_state import app_state


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.title = QLabel("Kalinova Dashboard")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size:22px; font-weight:bold;")

        self.ports_label = QLabel("Open Ports: None")
        self.ports_label.setStyleSheet("font-size:16px;")

        self.risk_label = QLabel("Risk Level: LOW")
        self.risk_label.setStyleSheet("font-size:16px;")

        self.suggestion_label = QLabel("Suggestions: None")
        self.suggestion_label.setWordWrap(True)
        self.suggestion_label.setStyleSheet("font-size:16px;")

        layout.addWidget(self.title)
        layout.addWidget(self.ports_label)
        layout.addWidget(self.risk_label)
        layout.addWidget(self.suggestion_label)
        layout.addStretch()

        self.setLayout(layout)

        # Auto refresh every 500ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dashboard)
        self.timer.start(500)

    def update_dashboard(self):

        # Open Ports
        if app_state.open_ports:
            ports_text = ", ".join(map(str, app_state.open_ports))
        else:
            ports_text = "None"

        self.ports_label.setText(f"Open Ports: {ports_text}")

        # Risk
        self.risk_label.setText(f"Risk Level: {app_state.global_risk}")

        # Suggestions
        self.suggestion_label.setText(f"Suggestions: {app_state.suggestion}")