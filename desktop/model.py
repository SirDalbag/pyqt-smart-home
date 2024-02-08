import sqlite3


class Device:
    def __init__(
        self,
        id: int,
        temp_fact: int,
        temp_plan: int,
        light: bool,
        security: bool,
    ):
        self.id = id
        self.temp_fact = temp_fact
        self.temp_plan = temp_plan
        self.light = light
        self.security = security

    def __repr__(self) -> str:
        return f"""
Temperature Fact: {self.temp_fact}°C | Temperature Plan: {self.temp_plan}°C
Light - {"On" if self.light else "Off"} | Security - {"On" if self.security else "Off"}
"""


class Database:
    @staticmethod
    def query(
        db: str, sql: str, args: tuple, many: bool = True
    ) -> list[tuple] or tuple:
        try:
            with sqlite3.connect(db) as connection:
                cursor = connection.cursor()
                cursor.execute(sql, args)
                if many:
                    return cursor.fetchall()
                return cursor.fetchone()
        except Exception as error:
            return error

    @staticmethod
    def create(
        db: str, table: str, columns: list[str], types: list[str]
    ) -> list[tuple] or tuple:
        return Database.query(
            db=db,
            sql="CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY AUTOINCREMENT, {}) ".format(
                table,
                ", ".join([f"{col} {type}" for col, type in list(zip(columns, types))]),
            ),
            args=(),
        )

    @staticmethod
    def select(
        db: str, table: str, columns: list[str], id: int = None
    ) -> list[tuple] or tuple:
        query = "SELECT id, {} FROM {}".format(", ".join(columns), table)
        if not id:
            return Database.query(db=db, sql=query, args=())
        return Database.query(
            db=db,
            sql=f"{query} WHERE id = ?",
            args=(id,),
            many=False,
        )

    @staticmethod
    def insert(
        db: str, table: str, columns: list[str], values: list[any]
    ) -> list[tuple]:
        return Database.query(
            db=db,
            sql="INSERT INTO {} ({}) VALUES ({})".format(
                table, ", ".join(columns), ", ".join(["?" for _ in values])
            ),
            args=values,
        )

    @staticmethod
    def update(
        db: str, table: str, columns: list[str], values: list[any], id: int
    ) -> list[tuple]:
        return Database.query(
            db=db,
            sql="UPDATE {} SET {} WHERE id = ?".format(
                table, ", ".join([f"{col} = ?" for col in columns])
            ),
            args=values + [id],
        )

    @staticmethod
    def delete(db: str, table: str, id: int) -> list[tuple]:
        return Database.query(
            db=db,
            sql="DELETE FROM {} WHERE id = ?".format(table),
            args=(id,),
        )
