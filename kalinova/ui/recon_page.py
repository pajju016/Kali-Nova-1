from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal

from core.app_state import app_state


class ReconPage(QWidget):

    run_command = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Reconnaissance Tools")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:22px; font-weight:bold;")
        layout.addWidget(title)

        # ========================
        # NMAP
        # ========================

        nmap_group = QGroupBox("Nmap Scan")
        nmap_layout = QVBoxLayout()

        self.nmap_target = QLineEdit()
        self.nmap_target.setPlaceholderText("Enter Target IP / Domain")

        self.scan_type = QComboBox()
        self.scan_type.addItems([
            "Quick Scan",
            "Service Detection",
            "Aggressive Scan"
        ])

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Custom Port (optional)")

        self.nmap_btn = QPushButton("Run Nmap")
        self.nmap_btn.clicked.connect(self.build_nmap)

        nmap_layout.addWidget(self.nmap_target)
        nmap_layout.addWidget(self.scan_type)
        nmap_layout.addWidget(self.port_input)
        nmap_layout.addWidget(self.nmap_btn)

        nmap_group.setLayout(nmap_layout)

        # ========================
        # WHOIS
        # ========================

        whois_group = QGroupBox("Whois Lookup")
        whois_layout = QVBoxLayout()

        self.whois_target = QLineEdit()
        self.whois_target.setPlaceholderText("Enter Domain (example.com)")

        self.whois_btn = QPushButton("Run Whois")
        self.whois_btn.clicked.connect(self.build_whois)

        whois_layout.addWidget(self.whois_target)
        whois_layout.addWidget(self.whois_btn)

        whois_group.setLayout(whois_layout)

        # ========================
        # theHarvester
        # ========================

        harvester_group = QGroupBox("theHarvester OSINT")
        harvester_layout = QVBoxLayout()

        self.harvester_domain = QLineEdit()
        self.harvester_domain.setPlaceholderText("Enter Domain")

        self.harvester_source = QComboBox()
        self.harvester_source.addItems([
            "google",
            "bing",
            "yahoo",
            "duckduckgo"
        ])

        self.harvester_btn = QPushButton("Run theHarvester")
        self.harvester_btn.clicked.connect(self.build_harvester)

        harvester_layout.addWidget(self.harvester_domain)
        harvester_layout.addWidget(self.harvester_source)
        harvester_layout.addWidget(self.harvester_btn)

        harvester_group.setLayout(harvester_layout)

        layout.addWidget(nmap_group)
        layout.addWidget(whois_group)
        layout.addWidget(harvester_group)
        layout.addStretch()

        self.setLayout(layout)

        # Apply current mode rules when page loads
        self.update_mode(app_state.mode)

    # ========================
    # MODE UPDATE FUNCTION
    # ========================

    def update_mode(self, mode):
        index = self.scan_type.findText("Aggressive Scan")

        if index != -1:
            item = self.scan_type.model().item(index)

            if mode == "Beginner":
                item.setEnabled(False)

                # If currently selected, reset to safe option
                if self.scan_type.currentText() == "Aggressive Scan":
                    self.scan_type.setCurrentIndex(0)

            else:
                item.setEnabled(True)

    # ========================
    # NMAP COMMAND
    # ========================

    def build_nmap(self):
        target = self.nmap_target.text().strip()
        if not target:
            return

        app_state.reset_scan()

        scan = self.scan_type.currentText()

        # Backend safety check
        if scan == "Aggressive Scan" and app_state.mode == "Beginner":
            print("Aggressive scan disabled in Beginner mode.")
            return

        command = "nmap "

        if scan == "Service Detection":
            command += "-sV "
        elif scan == "Aggressive Scan":
            command += "-A "

        port = self.port_input.text().strip()
        if port:
            command += f"-p {port} "

        command += target

        self.run_command.emit(command)

    # ========================
    # WHOIS COMMAND
    # ========================

    def build_whois(self):
        target = self.whois_target.text().strip()
        if not target:
            return

        command = f"whois {target}"
        self.run_command.emit(command)

    # ========================
    # HARVESTER COMMAND
    # ========================

    def build_harvester(self):
        domain = self.harvester_domain.text().strip()
        source = self.harvester_source.currentText()

        if not domain:
            return

        command = f"theHarvester -d {domain} -b {source}"
        self.run_command.emit(command)