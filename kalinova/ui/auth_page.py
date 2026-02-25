from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton,
    QComboBox, QGroupBox, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal


class AuthPage(QWidget):

    run_command = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Authentication Testing")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:22px; font-weight:bold;")

        layout.addWidget(title)

        # ========================
        # HYDRA SECTION
        # ========================

        hydra_group = QGroupBox("Hydra Brute Force")
        hydra_layout = QVBoxLayout()

        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Enter Target IP")

        self.service_dropdown = QComboBox()
        self.service_dropdown.addItems([
            "ssh",
            "ftp",
            "http-get",
            "http-post-form"
        ])

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_file = QLineEdit()
        self.password_file.setPlaceholderText("Select Password Wordlist")

        self.browse_btn = QPushButton("Browse Wordlist")
        self.browse_btn.clicked.connect(self.select_wordlist)

        self.hydra_btn = QPushButton("Run Hydra")
        self.hydra_btn.clicked.connect(self.build_hydra)

        hydra_layout.addWidget(self.target_input)
        hydra_layout.addWidget(self.service_dropdown)
        hydra_layout.addWidget(self.username_input)
        hydra_layout.addWidget(self.password_file)
        hydra_layout.addWidget(self.browse_btn)
        hydra_layout.addWidget(self.hydra_btn)

        hydra_group.setLayout(hydra_layout)

        # ========================
        # JOHN SECTION
        # ========================

        john_group = QGroupBox("John the Ripper - Hash Cracking")
        john_layout = QVBoxLayout()

        self.hash_file = QLineEdit()
        self.hash_file.setPlaceholderText("Select Hash File")

        self.john_wordlist = QLineEdit()
        self.john_wordlist.setPlaceholderText("Select Wordlist")

        self.browse_hash_btn = QPushButton("Browse Hash File")
        self.browse_hash_btn.clicked.connect(self.select_hash_file)

        self.browse_john_wordlist = QPushButton("Browse Wordlist")
        self.browse_john_wordlist.clicked.connect(self.select_john_wordlist)

        self.john_btn = QPushButton("Run John")
        self.john_btn.clicked.connect(self.build_john)

        john_layout.addWidget(self.hash_file)
        john_layout.addWidget(self.browse_hash_btn)
        john_layout.addWidget(self.john_wordlist)
        john_layout.addWidget(self.browse_john_wordlist)
        john_layout.addWidget(self.john_btn)

        john_group.setLayout(john_layout)

        layout.addWidget(hydra_group)
        layout.addWidget(john_group)
        layout.addStretch()

        self.setLayout(layout)

    # ========================
    # FILE SELECTORS
    # ========================

    def select_wordlist(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Wordlist", "", "Text Files (*.txt)"
        )
        if file_path:
            self.password_file.setText(file_path)

    def select_hash_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Hash File", "", "Text Files (*.txt)"
        )
        if file_path:
            self.hash_file.setText(file_path)

    def select_john_wordlist(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Wordlist", "", "Text Files (*.txt)"
        )
        if file_path:
            self.john_wordlist.setText(file_path)

    # ========================
    # HYDRA COMMAND
    # ========================

    def build_hydra(self):
        target = self.target_input.text().strip()
        service = self.service_dropdown.currentText()
        username = self.username_input.text().strip()
        wordlist = self.password_file.text().strip()

        if not target or not username or not wordlist:
            return

        command = f"hydra -l {username} -P {wordlist} {target} {service}"

        self.run_command.emit(command)

    # ========================
    # JOHN COMMAND
    # ========================

    def build_john(self):
        hash_file = self.hash_file.text().strip()
        wordlist = self.john_wordlist.text().strip()

        if not hash_file:
            return

        command = f"john {hash_file}"

        if wordlist:
            command += f" --wordlist={wordlist}"

        self.run_command.emit(command)