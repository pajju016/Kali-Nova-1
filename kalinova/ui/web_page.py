from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton,
    QComboBox, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal


class WebPage(QWidget):

    run_command = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Web Testing Tools")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:22px; font-weight:bold;")

        layout.addWidget(title)

        # ========================
        # NIKTO SECTION
        # ========================

        nikto_group = QGroupBox("Nikto Web Scanner")
        nikto_layout = QVBoxLayout()

        self.nikto_url = QLineEdit()
        self.nikto_url.setPlaceholderText("Enter Target URL (http://example.com)")

        self.ssl_option = QComboBox()
        self.ssl_option.addItems([
            "Auto Detect",
            "Force SSL"
        ])

        self.nikto_btn = QPushButton("Run Nikto")
        self.nikto_btn.clicked.connect(self.build_nikto)

        nikto_layout.addWidget(self.nikto_url)
        nikto_layout.addWidget(self.ssl_option)
        nikto_layout.addWidget(self.nikto_btn)

        nikto_group.setLayout(nikto_layout)

        # ========================
        # SQLMAP SECTION
        # ========================

        sqlmap_group = QGroupBox("SQLmap Injection Testing")
        sqlmap_layout = QVBoxLayout()

        self.sqlmap_url = QLineEdit()
        self.sqlmap_url.setPlaceholderText("Enter Target URL with parameter (http://site.com/page?id=1)")

        self.sqlmap_level = QComboBox()
        self.sqlmap_level.addItems([
            "Level 1 (Basic)",
            "Level 3 (Medium)",
            "Level 5 (Aggressive)"
        ])

        self.sqlmap_btn = QPushButton("Run SQLmap")
        self.sqlmap_btn.clicked.connect(self.build_sqlmap)

        sqlmap_layout.addWidget(self.sqlmap_url)
        sqlmap_layout.addWidget(self.sqlmap_level)
        sqlmap_layout.addWidget(self.sqlmap_btn)

        sqlmap_group.setLayout(sqlmap_layout)

        layout.addWidget(nikto_group)
        layout.addWidget(sqlmap_group)
        layout.addStretch()

        self.setLayout(layout)

    # ========================
    # NIKTO COMMAND
    # ========================
    def build_nikto(self):
        url = self.nikto_url.text().strip()
        if not url:
            return

        command = f"nikto -h {url}"

        if self.ssl_option.currentText() == "Force SSL":
            command += " -ssl"

        self.run_command.emit(command)

    # ========================
    # SQLMAP COMMAND
    # ========================
    def build_sqlmap(self):
        url = self.sqlmap_url.text().strip()
        if not url:
            return

        command = f"sqlmap -u \"{url}\" --batch"

        level = self.sqlmap_level.currentText()

        if "Level 3" in level:
            command += " --level=3"
        elif "Level 5" in level:
            command += " --level=5"

        self.run_command.emit(command)