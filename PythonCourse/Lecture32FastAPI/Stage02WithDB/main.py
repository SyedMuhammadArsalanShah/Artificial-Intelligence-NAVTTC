from fastapi import FastAPI, HTTPException
from model import Item
from database import items_ref

app = FastAPI()

@app.post("/items")
def create_item(item: Item):
    doc_ref = items_ref.document()
    doc_ref.set(item.dict())
    return {"id": doc_ref.id, **item.dict()}

@app.get("/items")
def get_all_items():
    docs = items_ref.stream()
    return [{"id": d.id, **d.to_dict()} for d in docs]

@app.get("/items/{item_id}")
def get_item(item_id: str):
    doc = items_ref.document(item_id).get()
    if doc.exists:
        return {"id": doc.id, **doc.to_dict()}
    raise HTTPException(404, "Item not found")

@app.put("/items/{item_id}")
def update_item(item_id: str, item: Item):
    doc = items_ref.document(item_id)
    if doc.get().exists:
        doc.update(item.dict())
        return {"id": item_id, **item.dict()}
    raise HTTPException(404, "Item not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    doc = items_ref.document(item_id)
    if doc.get().exists:
        doc.delete()
        return {"message": "Item deleted"}
    raise HTTPException(404, "Item not found")