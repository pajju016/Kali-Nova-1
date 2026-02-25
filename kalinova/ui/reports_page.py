import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QMessageBox,
    QListWidget, QTextEdit, QHBoxLayout
)
from PyQt6.QtCore import Qt

from core.report_generator import ReportGenerator


class ReportsPage(QWidget):

    LOG_DIR = "logs"

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        title = QLabel("Reports & Scan History")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:22px; font-weight:bold;")

        self.generate_btn = QPushButton("Generate PDF Report")
        self.generate_btn.clicked.connect(self.generate_report)

        main_layout.addWidget(title)
        main_layout.addWidget(self.generate_btn)

        # ========================
        # Split Layout
        # ========================

        content_layout = QHBoxLayout()

        # Left: Log list
        self.log_list = QListWidget()
        self.log_list.itemClicked.connect(self.load_log)

        # Right: Log viewer
        self.log_viewer = QTextEdit()
        self.log_viewer.setReadOnly(True)

        content_layout.addWidget(self.log_list, 1)
        content_layout.addWidget(self.log_viewer, 3)

        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

        self.load_log_files()

    # ========================
    # Load Log Files
    # ========================

    def load_log_files(self):
        self.log_list.clear()

        if not os.path.exists(self.LOG_DIR):
            return

        files = sorted(os.listdir(self.LOG_DIR), reverse=True)

        for file in files:
            self.log_list.addItem(file)

    # ========================
    # Load Selected Log
    # ========================

    def load_log(self, item):
        file_path = os.path.join(self.LOG_DIR, item.text())

        with open(file_path, "r") as f:
            content = f.read()

        self.log_viewer.setText(content)

    # ========================
    # Generate PDF
    # ========================

    def generate_report(self):

        filepath = ReportGenerator.generate()

        QMessageBox.information(
            self,
            "Report Generated",
            f"Report saved at:\n{filepath}"
        )

        # Refresh logs after generation
        self.load_log_files()