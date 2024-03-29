from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QListWidgetItem
import threading
from core import get_objs, id, db, table, columns
from model import Database
import requests
import time


class Ui(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("desktop/src/main.ui", self)
        self.show()
        self.init()
        self.setup()
        self.thread(self.view)
        self.thread(self.get_web)
        self.thread(self.post_web)

    def setup(self):
        self.temp_up.clicked.connect(lambda: self.update("temp_plan", 1))
        self.temp_down.clicked.connect(lambda: self.update("temp_plan", -1))
        self.light_on.clicked.connect(lambda: self.update("light", True))
        self.light_off.clicked.connect(lambda: self.update("light", False))
        self.security_on.clicked.connect(lambda: self.update("security", True))
        self.security_off.clicked.connect(lambda: self.update("security", False))

    def thread(self, func):
        thread = threading.Thread(target=lambda: self.exception(func))
        thread.start()

    def exception(self, func):
        try:
            func()
        except Exception as error:
            self.device_view.clear()
            self.device_view.addItem(QListWidgetItem(str(error)))

    def init(self):
        Database.create(
            db=db,
            table=table,
            columns=columns,
            types=["INTEGER", "INTEGER", "BOOLEAN", "BOOLEAN"],
        )
        if (
            Database.query(
                db=db, sql=f"SELECT COUNT(*) FROM {table}", args=(), many=False
            )[0]
            == 0
        ):
            Database.insert(
                db=db, table=table, columns=columns, values=[0, 0, False, True]
            )
        self.thread(self.view)

    def view(self):
        for i in sorted(
            get_objs(Database.select(db=db, table=table, columns=columns)),
            key=lambda obj: obj.id,
        ):
            self.device_view.clear()
            self.device_view.addItem(QListWidgetItem(str(i)))

    def get(self, column):
        return Database.select(db=db, table=table, columns=[column], id=id)[1]

    def get_json(self):
        return dict(
            zip(
                ["id"] + columns,
                Database.select(db=db, table=table, columns=columns, id=id),
            )
        )

    def get_web(self):
        while True:
            response = requests.get(url="http://127.0.0.1:8000/api/")
            data = response.json()
            Database.insert(
                db=db,
                table=table,
                columns=["id"] + columns,
                values=[data[x] for x in columns],
            )
            self.thread(self.view)
            time.sleep(5)

    def post_web(self):
        while True:
            response = requests.post(
                url="http://127.0.0.1:8000/api/",
                json={"data": self.get_json()},
            )
            print(response.status_code)
            time.sleep(5)

    def update(self, column, value):
        if "temp" in column:
            value = self.get(column) + value
        Database.update(
            db=db,
            table=table,
            columns=[column],
            values=[value],
            id=id,
        )
        self.thread(self.view)
