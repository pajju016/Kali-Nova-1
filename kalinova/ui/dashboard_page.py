from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from core.app_state import app_state


class DashboardPage(QWidget):

    # Signal to notify MainWindow which tool to run
    run_suggested_signal = pyqtSignal(str)

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

        # 🔥 NEW: Next Tool Display
        self.next_tool_label = QLabel("Next Suggested Tool: None")
        self.next_tool_label.setStyleSheet("font-size:16px; font-weight:bold;")

        # 🔥 NEW: Run Suggested Tool Button
        self.run_suggested_btn = QPushButton("Run Suggested Tool")
        self.run_suggested_btn.setEnabled(False)
        self.run_suggested_btn.clicked.connect(self.run_suggested_tool)

        layout.addWidget(self.title)
        layout.addWidget(self.ports_label)
        layout.addWidget(self.risk_label)
        layout.addWidget(self.suggestion_label)
        layout.addWidget(self.next_tool_label)
        layout.addWidget(self.run_suggested_btn)
        layout.addStretch()

        self.setLayout(layout)

        # Auto refresh every 500ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dashboard)
        self.timer.start(500)

    # ========================
    # Update Dashboard
    # ========================

    def update_dashboard(self):

        # Open Ports
        if app_state.open_ports:
            ports_text = ", ".join(map(str, app_state.open_ports))
        else:
            ports_text = "None"

        self.ports_label.setText(f"Open Ports: {ports_text}")

        # Risk
        self.risk_label.setText(
            f"Risk Level: {app_state.global_risk} "
            f"(Score: {app_state.risk_score})"
        )

        # Suggestions
        self.suggestion_label.setText(
            f"Suggestions:\n{app_state.suggestion}"
        )

        # Next Tool
        if app_state.next_tool:
            self.next_tool_label.setText(
                f"Next Suggested Tool: {app_state.next_tool}"
            )
            self.run_suggested_btn.setEnabled(True)
        else:
            self.next_tool_label.setText(
                "Next Suggested Tool: None"
            )
            self.run_suggested_btn.setEnabled(False)

    # ========================
    # Run Suggested Tool
    # ========================

    def run_suggested_tool(self):
        if app_state.next_tool:
            self.run_suggested_signal.emit(app_state.next_tool)