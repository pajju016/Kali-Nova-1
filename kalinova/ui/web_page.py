from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton,
    QComboBox, QGroupBox, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from core.app_state import app_state   # <-- moved to top (better practice)


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
        # NIKTO
        # ========================

        nikto_group = QGroupBox("Nikto Web Scanner")
        nikto_layout = QVBoxLayout()

        self.nikto_url = QLineEdit()
        self.nikto_url.setPlaceholderText("Enter Target URL (http://example.com)")

        self.ssl_option = QComboBox()
        self.ssl_option.addItems(["Auto Detect", "Force SSL"])

        self.nikto_btn = QPushButton("Run Nikto")
        self.nikto_btn.clicked.connect(self.build_nikto)

        nikto_layout.addWidget(self.nikto_url)
        nikto_layout.addWidget(self.ssl_option)
        nikto_layout.addWidget(self.nikto_btn)

        nikto_group.setLayout(nikto_layout)

        # ========================
        # SQLMAP
        # ========================

        sqlmap_group = QGroupBox("SQLmap Injection Testing")
        sqlmap_layout = QVBoxLayout()

        self.sqlmap_url = QLineEdit()
        self.sqlmap_url.setPlaceholderText(
            "Enter URL with parameter (http://site.com/page?id=1)"
        )

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

        # ========================
        # GOBUSTER
        # ========================

        gobuster_group = QGroupBox("Gobuster Directory Brute Force")
        gobuster_layout = QVBoxLayout()

        self.gobuster_url = QLineEdit()
        self.gobuster_url.setPlaceholderText("Enter Target URL (http://example.com)")

        self.wordlist_path = QLineEdit()
        self.wordlist_path.setPlaceholderText("Select Wordlist File")

        self.browse_btn = QPushButton("Browse Wordlist")
        self.browse_btn.clicked.connect(self.select_wordlist)

        self.gobuster_btn = QPushButton("Run Gobuster")
        self.gobuster_btn.clicked.connect(self.build_gobuster)

        gobuster_layout.addWidget(self.gobuster_url)
        gobuster_layout.addWidget(self.wordlist_path)
        gobuster_layout.addWidget(self.browse_btn)
        gobuster_layout.addWidget(self.gobuster_btn)

        gobuster_group.setLayout(gobuster_layout)

        layout.addWidget(nikto_group)
        layout.addWidget(sqlmap_group)
        layout.addWidget(gobuster_group)
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

        command = f"sqlmap -u \"{url}\""

        # Beginner Mode forces safe behavior
        if app_state.mode == "Beginner":
            command += " --batch --level=1"
        else:
            command += " --batch"

            level = self.sqlmap_level.currentText()

            if "Level 3" in level:
                command += " --level=3"
            elif "Level 5" in level:
                command += " --level=5"

        self.run_command.emit(command)

    # ========================
    # GOBUSTER COMMAND
    # ========================
    def build_gobuster(self):
        url = self.gobuster_url.text().strip()
        wordlist = self.wordlist_path.text().strip()

        if not url or not wordlist:
            return

        command = f"gobuster dir -u {url} -w {wordlist}"

        self.run_command.emit(command)

    def select_wordlist(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Wordlist",
            "",
            "Text Files (*.txt)"
        )

        if file_path:
            self.wordlist_path.setText(file_path)