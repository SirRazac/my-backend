from fastapi import FastAPI
from pydantic import BaseModel, Field
from enum import Enum

items = [
    {"name": "Computer", "preis": 1000, "typ": "hardware"},
    {"name": "Monitor", "preis": 800, "typ": "hardware"},
    {"name": "Diablo 3", "preis": 50, "typ": "software"},
    {"name": "Windows", "preis": 90, "typ": "software"},
]

class Type(Enum):
    hardware = "hardware"
    software = "software"

class Item(BaseModel):
    name: str
    preis: int = Field(100, gt=0, lt=2500)
    typ: Type

app = FastAPI()

@app.get("/items/")
async def hello():
    return items

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return items(item_id)