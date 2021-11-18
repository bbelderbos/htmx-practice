import csv
from collections import defaultdict
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_data():
    cars = defaultdict(set)
    with open("MOCK_DATA.csv") as f:
        rows = csv.DictReader(f)
        for row in rows:
            cars[row["manu"]].add(row["model"])
    return cars


cars = get_data()


@app.get("/")
def home(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("index.html", context)


@app.get("/makers")
def get_makers(request: Request):
    context = {
        "request": request,
        "collection": sorted(cars.keys()),
    }
    return templates.TemplateResponse("_objects.html", context)


@app.get("/cars")
def get_cars(request: Request, makers: str):
    print(makers)
    print(request["query_string"])
    maker_cars = cars[makers]
    context = {
        "request": request,
        "collection": maker_cars,
    }
    return templates.TemplateResponse("_objects.html", context)
