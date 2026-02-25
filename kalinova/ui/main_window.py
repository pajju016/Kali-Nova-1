from PyQt6.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout
)

from ui.sidebar import Sidebar
from ui.workspace import Workspace
from ui.console import Console
from core.executor import CommandThread


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kalinova OS")
        self.setGeometry(100, 100, 1300, 800)

        # =========================
        # Central Layout
        # =========================
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        middle_layout = QHBoxLayout()

        # Sidebar
        self.sidebar = Sidebar()

        # Workspace (Pages)
        self.workspace = Workspace()

        middle_layout.addWidget(self.sidebar, 1)
        middle_layout.addWidget(self.workspace, 4)

        main_layout.addLayout(middle_layout)

        # Console
        self.console = Console()
        main_layout.addWidget(self.console)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # =========================
        # Navigation Connection
        # =========================
        self.sidebar.navigate.connect(self.workspace.switch_page)

        # =========================
        # Tool Execution Connections
        # =========================

        # Recon Page
        recon = self.workspace.pages["Recon"]
        recon.run_command.connect(self.execute)

        # Web Page
        web = self.workspace.pages["Web"]
        web.run_command.connect(self.execute)

        # (Future categories will connect here)

    # =========================
    # Command Execution
    # =========================
    def execute(self, command):

        self.thread = CommandThread(command)

        self.thread.output_signal.connect(self.console.log)

        self.thread.start()