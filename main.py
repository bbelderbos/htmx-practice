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
def read_root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)

@app.get("/makers")
def get_makers(request: Request):
    context = {
        "request": request,
        "makers": sorted(cars.keys()),
    }
    return templates.TemplateResponse("_makers.html", context)

@app.get("/cars/{item_id}")
def get_car(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
