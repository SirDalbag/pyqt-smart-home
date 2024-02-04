from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QMessageBox
import threading
from datetime import datetime
import time


class Ui(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("desktop/src/main.ui", self)
        self.__alive = True
        self.show()
        self.setup()
        self.thread(self.display_time)

    def setup(self):
        self.temperature_up.clicked.connect(lambda: self.update_temperature(1))
        self.temperature_down.clicked.connect(lambda: self.update_temperature(-1))

    def thread(self, func):
        thread = threading.Thread(target=lambda: self.exception(func))
        thread.start()

    def exception(self, func):
        try:
            func()
        except Exception as error:
            if self.ui.status:
                self.status.setText(f"Status: {str(error)}")

    def display_time(self):
        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.time.setText(f"{str(current_time)}")
            time.sleep(1)

    def update_temperature(self, value):
        temperature_value = int(self.temperature_plan.text()) + value
        self.temperature_plan.setText(
            f"+{temperature_value}" if temperature_value > 0 else f"{temperature_value}"
        )
