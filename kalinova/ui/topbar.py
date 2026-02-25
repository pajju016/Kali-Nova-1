from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import QTimer

from core.app_state import app_state


class TopBar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        self.title = QLabel("KALINOVA OS")
        self.title.setStyleSheet("font-size:18px; font-weight:bold;")

        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Beginner Mode", "Expert Mode"])
        self.mode_selector.currentIndexChanged.connect(self.change_mode)

        self.risk_label = QLabel("Global Risk: LOW")
        self.risk_label.setStyleSheet("color: green; font-weight:bold;")

        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.mode_selector)
        layout.addWidget(self.risk_label)

        self.setLayout(layout)

        # Auto update risk display every 500ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_risk_display)
        self.timer.start(500)

    def change_mode(self):
        selected = self.mode_selector.currentText()

        if "Beginner" in selected:
            app_state.set_mode("Beginner")
        else:
            app_state.set_mode("Expert")

    def update_risk_display(self):
        risk = app_state.global_risk

        if risk == "HIGH":
            self.risk_label.setStyleSheet("color: red; font-weight:bold;")
        elif risk == "MEDIUM":
            self.risk_label.setStyleSheet("color: orange; font-weight:bold;")
        else:
            self.risk_label.setStyleSheet("color: green; font-weight:bold;")

        self.risk_label.setText(f"Global Risk: {risk}")