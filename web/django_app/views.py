from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .utils import Database

db = "database/data.db"
table = "device"
columns = ["temp_fact", "temp_plan", "light", "security"]
id = 1


def index(request):
    data = Database.select(db=db, table=table, columns=columns, id=id)
    return render(request, "index.html", {"data": data})


def update(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "up" or action == "down":
            column = "temp_plan"
            value = Database.select(db=db, table=table, columns=[column], id=id)[1]
        elif action == "l-on" or action == "l-off":
            column = "light"
        elif action == "s-on" or action == "s-off":
            column = "security"
        if action == "up":
            value = value + 1
        elif action == "down":
            value = value - 1
        elif action == "l-on" or action == "s-on":
            value = 1
        elif action == "l-off" or action == "s-off":
            value = 0
        Database.update(db=db, table=table, columns=[column], values=[value], id=id)
    return redirect("index")


@api_view(http_method_names=["GET", "POST", "PUT", "PATCH", "DELETE"])
def api(request):
    if request.method == "GET":
        data = Database.select(db=db, table=table, columns=columns, id=id)
        return Response(data=dict(zip(["id"] + columns, data)))
    elif request.method == "POST":
        data = dict(request.data["data"])
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
        Database.update(
            db=db,
            table=table,
            columns=columns,
            values=[data[x] for x in columns],
            id=id,
        )
        return Response(data=data)
