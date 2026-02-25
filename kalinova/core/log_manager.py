import os
from datetime import datetime


class LogManager:

    LOG_DIR = "logs"

    @staticmethod
    def initialize():
        if not os.path.exists(LogManager.LOG_DIR):
            os.makedirs(LogManager.LOG_DIR)

    @staticmethod
    def log_command(command):
        LogManager.initialize()

        filename = datetime.now().strftime("%Y-%m-%d_session.txt")
        file_path = os.path.join(LogManager.LOG_DIR, filename)

        with open(file_path, "a") as f:
            f.write("\n")
            f.write("=" * 60 + "\n")
            f.write(f"Time: {datetime.now()}\n")
            f.write(f"Command: {command}\n")
            f.write("=" * 60 + "\n")

    @staticmethod
    def log_output(line):
        LogManager.initialize()

        filename = datetime.now().strftime("%Y-%m-%d_session.txt")
        file_path = os.path.join(LogManager.LOG_DIR, filename)

        with open(file_path, "a") as f:
            f.write(line + "\n")