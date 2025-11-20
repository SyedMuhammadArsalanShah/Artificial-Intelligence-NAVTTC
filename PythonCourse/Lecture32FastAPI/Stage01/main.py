from fastapi import FastAPI, HTTPException
from models import Item


app = FastAPI()


items = []


@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return {"message": "Item Added", "Item": item}


@app.get("/items")
def get_all_items():

    return items


@app.get("/items/{item_id}")
def get_items_id(item_id: int):
    for item in items:
        if item.id == item_id:

            return item
    raise HTTPException("404", "NOT FOUND")


@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: Item):
    for i, item in enumerate(items):
        if item.id == item_id:
            items[i] = updated_item
            return {"message": "Item Updated", "Item": updated_item}
    raise HTTPException("404", "NOT FOUND")


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for i, item in enumerate(items):
        if item.id == item_id:
            items.remove(item)
            return {"message": "Item deleted"}
    raise HTTPException("404", "NOT FOUND")
