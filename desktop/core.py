import concurrent.futures
from model import Device

id = 1
db = "desktop/database/data.db"
table = "device"
columns = ["temp_fact", "temp_plan", "light", "security"]


def get_obj(obj: tuple) -> Device:
    return Device(obj[0], obj[1], obj[2], obj[3], obj[4])


def get_objs(objs: list[tuple]) -> list[Device]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for obj in objs:
            futures.append(executor.submit(get_obj, obj))
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results
