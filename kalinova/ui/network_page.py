from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton,
    QComboBox, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal


class NetworkPage(QWidget):

    run_command = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Network Tools")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:22px; font-weight:bold;")

        layout.addWidget(title)

        # ========================
        # NETCAT SECTION
        # ========================

        netcat_group = QGroupBox("Netcat Utility")
        netcat_layout = QVBoxLayout()

        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Target IP")

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Port")

        self.mode_dropdown = QComboBox()
        self.mode_dropdown.addItems([
            "Connect to Target",
            "Listen Mode"
        ])

        self.netcat_btn = QPushButton("Run Netcat")
        self.netcat_btn.clicked.connect(self.build_netcat)

        netcat_layout.addWidget(self.target_input)
        netcat_layout.addWidget(self.port_input)
        netcat_layout.addWidget(self.mode_dropdown)
        netcat_layout.addWidget(self.netcat_btn)

        netcat_group.setLayout(netcat_layout)

        # ========================
        # WIRESHARK SECTION
        # ========================

        wireshark_group = QGroupBox("Wireshark Packet Analyzer")
        wireshark_layout = QVBoxLayout()

        self.wireshark_btn = QPushButton("Launch Wireshark")
        self.wireshark_btn.clicked.connect(self.launch_wireshark)

        wireshark_layout.addWidget(self.wireshark_btn)

        wireshark_group.setLayout(wireshark_layout)

        layout.addWidget(netcat_group)
        layout.addWidget(wireshark_group)
        layout.addStretch()

        self.setLayout(layout)

    # ========================
    # NETCAT COMMAND
    # ========================

    def build_netcat(self):
        target = self.target_input.text().strip()
        port = self.port_input.text().strip()
        mode = self.mode_dropdown.currentText()

        if not port:
            return

        if mode == "Connect to Target":
            if not target:
                return
            command = f"nc {target} {port}"
        else:
            command = f"nc -lvnp {port}"

        self.run_command.emit(command)

    # ========================
    # WIRESHARK LAUNCH
    # ========================

    def launch_wireshark(self):
        command = "wireshark"
        self.run_command.emit(command)